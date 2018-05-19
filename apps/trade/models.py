from datetime import datetime

from django.db import models
from users.models import UserProfile
from courses.models import Course


# Create your models here.
class Order(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "等待支付"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "交易未创建"),

    )
    order_id = models.BigIntegerField(primary_key=True, verbose_name=u"订单号");
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name=u"交易号")
    user = models.ForeignKey(UserProfile, verbose_name=u"用户");
    price = models.IntegerField(default=0, verbose_name=u"总金额");
    is_pay = models.CharField(choices=ORDER_STATUS, default="paying", verbose_name=u"是否支付",max_length=20);
    pay_way = models.CharField(choices=(('wx', u"微信"), ('zfb', u"支付宝")), default='zfb', max_length=3,
                               verbose_name=u"支付方式");
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    add_date = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间");

    class Meta:
        verbose_name = u"订单";
        verbose_name_plural = verbose_name;

    def __str__(self):
        return str(self.order_id);


class OrderDetail(models.Model):
    """
    订单详细
    """
    order = models.ForeignKey(Order, verbose_name=u"订单");
    course = models.ForeignKey(Course, verbose_name=u"课程");
    add_date = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间");

    class Meta:
        verbose_name = u"订单详情";
        verbose_name_plural = verbose_name;

    def __str__(self):
        return str(self.order.order_id);


class Cart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(UserProfile, verbose_name=u"用户");
    course = models.ForeignKey(Course, verbose_name=u"实战");
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间");
    class Meta:
        verbose_name = u"购物车";
        verbose_name_plural = verbose_name;

    def __str__(self):
        return str(self.order.order_id);


