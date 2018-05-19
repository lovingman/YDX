import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.views.generic.base import View
from django.urls import reverse
from users.models import UserProfile, EmailVerifyRecord, Banner
from users.forms import LoginForm, RegisterForm, ResetPWViewForm, NickNameForm, WorkNameForm, UploadImageForm
from courses.models import *
from teachers.models import Teacher
from operation.models import UserCourse, UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.email_send import send_email
from utils.mymixin import LoginRequiredMixin


# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                record.delete()
                return render(
                    request,
                    'usercenter/login.html',
                )
        else:
            render(request, 'usercenter/login.html', {
                'msg': "激活码错误，激活失败"
            })


class LoginView(View):
    def get(self, request):
        redirect_url = request.GET.get('next', '')
        return render(request, "usercenter/login.html", {
            'redirect_url': redirect_url
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    # 跳转到首页 user request会被带回到首页
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(
                        request, "usercenter/login.html", {
                            "msg": "用户名未激活! 请前往邮箱进行激活"})
            return render(request, 'usercenter/login.html', {'msg': '用户名或者密码错误！'})
        return render(request, 'usercenter/login.html', {'form_help': login_form.errors, })


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(
            request, "usercenter/register.html", {
                'register_form': register_form})

    def post(self, request):

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name, is_active=True):
                return render(
                    request, "usercenter/register.html", {
                        "register_form": register_form, "msg": "用户已存在"})
            pass_word = request.POST.get("password", "")

            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            # 默认激活状态为false
            user_profile.is_active = False

            # 加密password进行保存
            user_profile.password = make_password(pass_word)

            sm = send_email(user_name, send_type='register')
            if sm:
                user_profile.save()
            else:
                return render(
                    request,
                    "usercenter/register.html",
                    {
                        'register_form': register_form,
                        'register_form_errors': register_form.errors,

                    }
                )

            return render(request, "usercenter/login.html", )
        else:
            return render(
                request,
                "usercenter/register.html",
                {
                    'register_form': register_form,
                    'register_form_errors': register_form.errors,

                }
            )


class ForgetPWView(View):
    def get(self, request):
        resetpw_form = ResetPWViewForm()
        return render(request, 'usercenter/changepassword.html', {
        })

    def post(self, request):
        resetpw_form = ResetPWViewForm(request.POST)
        email = request.POST.get("email", "")

        if resetpw_form.is_valid():
            code = request.POST.get("cord", "")
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return render(request, 'usercenter/changepassword.html',
                              {
                                  'email': email,
                                  'resetpw_form': resetpw_form.errors,
                                  'msg': '密码不一样'
                              })

            all_records = EmailVerifyRecord.objects.filter(code=code)
            if all_records:
                for record in all_records:
                    if record.email == email:
                        user = UserProfile.objects.get(email=email)
                        user.password = make_password(password2)
                        user.save()
                        return HttpResponseRedirect(reverse("users:login"))
            return render(request, 'usercenter/changepassword.html',
                          {
                              'email': email,
                              'resetpw_form': resetpw_form.errors,
                              'msg': '验证码不一样'
                          })
        return render(request, 'usercenter/changepassword.html', {
            'email': email,
            'resetpw_form': resetpw_form.errors
        })

        # return HttpResponse('{"status":"success"}', content_type='application/json')
        # else:
        # return HttpResponse('{"status":"fail"}', content_type='application/json')


# 获得验证码

class FindPWCordView(View):
    def get(self, request):
        return render(request, 'usercenter/findpassword.html')

    def post(self, request):
        email = request.POST.get("email", "")
        user = UserProfile.objects.filter(email=email)
        if user:
            send_email(email, 'forget')
            # return HttpResponseRedirect(reverse("users:forget",kwargs={'email':email}))
            return render(request, 'usercenter/changepassword.html',
                          {
                              'email': email
                          })
        return render(request, 'usercenter/findpassword.html',
                      {
                          'email': email,
                          'msg': '用户不存在'
                      })


class LogoutView(View):
    def get(self, request):
        # django自带的logout
        logout(request)
        # 重定向到首页,
        return HttpResponseRedirect(reverse("index"))


class UserInfoView(LoginRequiredMixin, View):

    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'accountcenter/accountcenter-info.html', {
        })


class NickNameView(LoginRequiredMixin, View):
    # login_url = '/login/'
    redirect_field_name = 'next'
    def post(self, request):
        nick_name_form = NickNameForm(request.POST)
        if nick_name_form.is_valid():
            user = request.user
            nick_name = request.POST.get('nick_name')
            user.nick_name = nick_name
            user.save()
            return HttpResponseRedirect(reverse("users:user_info"))
        return HttpResponseRedirect(reverse("users:user_info"))


class WorkNameView(LoginRequiredMixin, View):
    # login_url = '/login/'
    redirect_field_name = 'next'
    def post(self, request):
        work_name_form = WorkNameForm(request.POST, instance=request.user)
        if work_name_form.is_valid():
            work_name_form.save()
            return HttpResponseRedirect(reverse("users:user_info"))
        return HttpResponseRedirect(reverse("users:user_info"))

class MyPhoneView(LoginRequiredMixin, View):
    # login_url = '/login/'
    redirect_field_name = 'next'
    def post(self, request):
        phone=request.POST.get("iphone")
        if phone:
            user=request.user
            user.mobile=phone
            user.save()
            return HttpResponseRedirect(reverse("users:user_info"))
        return HttpResponseRedirect(reverse("users:user_info"))

class UploadImageView(LoginRequiredMixin, View):
    # login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponseRedirect(reverse("users:user_info"))
        return HttpResponseRedirect(reverse("users:user_info"))


class MyCourseView(LoginRequiredMixin, View):
    redirect_field_name = 'next'
    def get(self, request):
        category = request.GET.get('category', '')
        user_courses = UserCourse.objects.filter(user=request.user)

        my_courses = [cours.course for cours in user_courses]
        all_courses = []
        if category == 'fight':
            for cours in my_courses:
                if cours.is_fight:
                    all_courses.append(cours)
        elif category == 'free':
            for cours in my_courses:
                if not cours.is_fight:
                    all_courses.append(cours)
        else:
            all_courses = my_courses
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从all_course中取五个出来，每页显示5个
        p = Paginator(all_courses, 2, request=request)
        all_courses = p.page(page)

        return render(request, 'accountcenter/accountcenter-coures.html', {
            'all_courses': all_courses,
            'category': category
        })


class DeleteMyCourseView(LoginRequiredMixin, View):
    # login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, course_id):
        course = UserCourse.objects.filter(course_id=course_id)

        course.delete()

        return HttpResponseRedirect(reverse("users:info_courses"))


class MyFavCouresView(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    def get(self, request):
        user_courses = UserFavorite.objects.filter(user=request.user).filter(fav_type=1)
        fav_id = [user_course.fav_id for user_course in user_courses]
        all_courses = Course.objects.filter(id__in=fav_id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从all_course中取五个出来，每页显示5个
        p = Paginator(all_courses, 2, request=request)
        all_courses = p.page(page)

        return render(request, 'accountcenter/accountcenter-favcoures.html', {
            'user_courses': all_courses,

        })


class MyFavTeacherView(LoginRequiredMixin, View):

    redirect_field_name = 'next'

    def get(self, request):
        user_courses = UserFavorite.objects.filter(user=request.user).filter(fav_type=2)
        fav_id = [user_course.fav_id for user_course in user_courses]
        all_teacher = Teacher.objects.filter(id__in=fav_id)
        return render(request, 'accountcenter/accountcenter-teacher.html', {
            'all_teacher': all_teacher,
        })


class IndexView(View):
    def get(self, request):
        teachers = Teacher.objects.all().order_by("click_nums")[:5]
        courses = Course.objects.filter(is_fight=False).order_by("students")[:5]
        fights = Course.objects.filter(is_fight=True).order_by("students")[:5]
        category = Category.objects.filter(category_type=1)

        banner_courses = Banner.objects.all().order_by("index")[:3]
        return render(request, "index.html",
                      {
                          "courses": courses,
                          "teachers": teachers,
                          "category": category,
                          'fights': fights,
                          "banner": banner_courses
                      });


# 全局 404 处理函数
def page_not_found(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


# 全局 500 处理函数
def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
