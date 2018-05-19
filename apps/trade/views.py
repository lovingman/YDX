import time
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import *
from courses.models import *
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mymixin import LoginRequiredMixin
from YDX.settings import private_key_path, ali_pub_key_path
from operation.models import UserCourse

from utils.alipay import AliPay


# Create your views here.
class FightListView(View):
    def get(self, request):
        category_code = request.GET.get('category_code', '')
        all_course = Course.objects.filter(is_fight=True).all();
        category_type1 = Category.objects.filter(category_type=1)
        category_type2 = Category.objects.filter(category_type=2)

        category_parent_code = ''
        if category_code:
            category_type = Category.objects.filter(code=category_code).filter(category_type=1)
            category_parent_id = Category.objects.get(code=category_code).parent_category_id
            category_parent_code = Category.objects.get(code=category_code).parent_category
            if category_type:
                category_type2 = category_type2.filter(parent_category__code=category_code)
                all_course = all_course.filter(course_category__parent_category__code=category_code)
            else:
                all_course = all_course.filter(course_category__code=category_code)
                category_type2 = category_type2.filter(parent_category=category_parent_id)
        sort = request.GET.get('sort', "")
        fights = []
        if request.user.is_authenticated:
               my_courses=UserCourse.objects.filter(user=request.user)
               courses = [couser.course for couser in my_courses]

               for fight in courses:
                   if fight.is_fight:
                       fights.append(fight)
        if sort:
            if sort == "last":
                all_course = all_course.order_by("-add_time")
            elif sort == "pop":
                all_course = all_course.order_by("-students")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从all_course中取五个出来，每页显示5个
        p = Paginator(all_course, 12, request=request)
        all_course = p.page(page)


        return render(request, "shizhan/shizhan-list.html",
                      {
                          'category_type1': category_type1,
                          'category_type2': category_type2,
                          'courses': all_course,
                          'sort': sort,
                          'category_code': category_code,
                          'parent_code': category_parent_code,
                          'fights':fights
                      }
                      )


class FightDetailView(View):
    def get(self, request, fight_id):
        fight = Course.objects.get(id=fight_id)
        has_buy_fight = False
        if request.user.is_authenticated:
            if UserCourse.objects.filter(user=request.user,course=fight):
                has_buy_fight = True
        return render(request, 'shizhan/class.html', {
            'finght': fight,
            'has_buy_fight': has_buy_fight
        })


class OrderDetailView(View):
    def get(self, request):

        fight_id = request.GET.get('fight_id', '')
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("users:login"))
        if fight_id:
            fight = Course.objects.get(id=fight_id)

        return render(request, "shizhan/confirm.html", {
            'fight': fight
        })

    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class ConfirmOrderView(View):
    def get(self, reqeust):
        return render(reqeust, 'shizhan/pay.html')

    def post(self, reqeust):

        fight_ids = reqeust.POST.getlist("fight_ids", )
        fights = [];
        total_price = 0
        for id in fight_ids:
            del_cart = Cart.objects.filter(course_id=id);
            if del_cart:
                del_cart.delete();

            fight = Course.objects.get(id=id);
            fights.append(fight);
            total_price += fight.price;

        user = reqeust.user
        order = Order()
        local_time = time.localtime(time.time());
        order_id = str(local_time.tm_year) + str(local_time.tm_mon) + str(local_time.tm_mday) + str(
            local_time.tm_hour) + str(local_time.tm_min) + str(local_time.tm_sec) + str(local_time.tm_sec);
        order.order_id = order_id
        order.user = user
        order.price = total_price
        order.save()
        for fight in fights:
            order_detail = OrderDetail()
            order_detail.order = order
            order_detail.course = fight
            order_detail.save()
            # 从购物车中删除
            cart = Cart.objects.filter(user=user, course=fight);
            if cart:
                cart.delete();

        return HttpResponseRedirect(reverse('fights:fight_gopay', kwargs={'order_id': order.order_id}));


class AddCartView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        fight_id = request.POST.get('fight_id', 0)
        if (int(fight_id) > 0):
            fight = Course.objects.get(id=int(fight_id));
            if not (Cart.objects.filter(user=request.user, course=fight)):
                cart = Cart();
                cart.user = request.user;
                cart.course = fight;
                cart.save();
                return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class CartView(LoginRequiredMixin, View):

    redirect_field_name = 'next'

    def get(self, request):
        # 购物车中的课程
        cart_fights = Cart.objects.filter(user=request.user);
        fights = [fight.course for fight in cart_fights];
        price = 0
        for fight in fights:
            price += fight.price
        fight_num = len(fights);
        return render(request, 'shizhan/cart.html', {
            "fights": fights,
            'fight_num': fight_num,
            'price': price
        })


class DeleteCartFightView(LoginRequiredMixin, View):

    redirect_field_name = 'next'

    def get(self, request):
        # 购物车中的课程
        fight_id = request.GET.get('fight_id', 0)
        if fight_id:
            fight = Course.objects.get(id=int(fight_id));
            cart_fights = Cart.objects.filter(user=request.user, course=fight);
            cart_fights.delete()
        return HttpResponseRedirect(reverse("fights:fight_cart"))


class PayFightDetailView(View):
    def get(self, request, order_id):
        #print(order_id)
        order = Order.objects.get(order_id=order_id);
        order_detail = OrderDetail.objects.filter(order=order);
        fights = []
        for detail in order_detail:
            fights.append(detail.course);
        #print(fights)
        return render(request, 'shizhan/pay.html', {
            'order': order,
            'order_detail': order_detail
        })

    def post(self, request, order_id):
        order = Order.objects.get(order_id=order_id);
        order_detail = OrderDetail.objects.filter(order=order);
        body = "购买了"
        for detail in order_detail:
            body = body + detail.course.name

        if order:
            alipay = AliPay(
                appid="2016091100485762",
                app_notify_url="http://47.104.201.172/fights/pay/",
                app_private_key_path=private_key_path,
                alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                debug=True,  # 默认False,
                return_url="http://47.104.201.172/fights/pay/"
            )
            query_params = alipay.direct_pay(
                subject="购买课程",
                out_trade_no=order.order_id,
                body=body,
                total_amount=order.price
            )

            pay_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=query_params)
            return HttpResponseRedirect(pay_url)


class AliPayView(View):
    def get(self, request):
        """
                处理支付宝的return_url返回
                :param request:
                :return:
        """

        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)
        alipay = AliPay(
            appid="2016091100485762",
            app_notify_url="http://47.104.201.172/fights/pay/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.104.201.172/fights/pay/"
        )
        #print(processed_dict)
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_id = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status',"TRADE_SUCCESS")
            existed_orders = Order.objects.filter(order_id=order_id)


            for existed_order in existed_orders:
                order_details = OrderDetail.objects.filter(order=existed_order)
                for order_detail in order_details:
                    course = order_detail.course

                    if course:
                        # 加入到我的课程
                        existed_course = UserCourse.objects.filter(course=course, user=existed_order.user)
                        if not existed_course:
                            usercourse = UserCourse()
                            usercourse.course = course
                            usercourse.user = existed_order.user
                            usercourse.save()
                            course.students+=1
                            course.save()
                    #print(trade_status)
                    existed_order.is_pay = trade_status
                    existed_order.trade_no = trade_no
                    existed_order.pay_time = datetime.now()
                    existed_order.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))

    pass

    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)
        alipay = AliPay(
            appid="2016091100485762",
            app_notify_url="http://47.104.201.172/fights/pay/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.104.201.172/fights/pay/"
        )
        #print(processed_dict)
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_id = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', "")
            existed_orders = Order.objects.filter(order_id=order_id)
            #print("post" + trade_status)
            for existed_order in existed_orders:
                order_details = OrderDetail.objects.filter(order=existed_order)
                for order_detail in order_details:
                    course = order_detail.course
                    if course:
                        # 加入到我的课程
                        existed_course = UserCourse.objects.filter(course=course, user=existed_order.user)
                        if not existed_course:
                            usercourse = UserCourse()
                            usercourse.course = course
                            usercourse.user = existed_order.user
                            usercourse.save()

                existed_order.is_pay = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            return HttpResponse("success")

class MyOrderDetailView(LoginRequiredMixin,View):

    redirect_field_name = 'next'
    def get(self,request):
        type=request.GET.get('type','')
        has_buy_fights= UserCourse.objects.filter(course__is_fight=True,user=request.user);#删除订单里已经买到的课程
        has_buy =[fight.course for fight in has_buy_fights]
        orders=Order.objects.filter(user=request.user)
        print(request.user)
        if type=="1":
            orders = orders.filter(is_pay="TRADE_SUCCESS")
            #print(orders.count())
        if type=="2":
            orders = orders.filter(is_pay="paying")

        # for myorder in orders:
        #     print(myorder.trade_no)

        order_details=[]
        for order in orders:
            details=[]
            order_detail = OrderDetail.objects.filter(order=order)
            for detail in order_detail:

                if order.is_pay=="paying":
                    if detail.course in has_buy:
                        print("删除")
                        order.price-=detail.course.price
                        order.save()
                        detail.delete()
                    details.append(detail)
                elif order.is_pay=="TRADE_SUCCESS":
                    print("成功")
                    details.append(detail)
            order_details.append(details)
        return render(request,"shizhan/myorder.html",{
            "order_details":order_details,
            'type':type
        })


    def post(self,request):
        order_id = request.POST.get("order_id","")
        if order_id:
            order =Order.objects.get(order_id=order_id)
            order_details=OrderDetail.objects.filter(order=order);
            order_details.delete()
            order.delete()
            return  HttpResponseRedirect(reverse("fights:myorder"))
        return HttpResponseRedirect(reverse("fights:myorder"))

