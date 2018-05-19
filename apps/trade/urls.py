# _*_ encoding:utf-8 _*_
from django.conf.urls import url
from .views import *
__author__ = 'YZF'
__date__ = '2018/4/5,20:20'

urlpatterns =[
    url(r'^list/',FightListView.as_view(),name='fight_list'),
    url(r'^class/(?P<fight_id>.*)/', FightDetailView.as_view(), name='fight_class'),
    url(r'^addcart/',AddCartView.as_view(), name='fight_addcart'),
    url(r'^removecart/',DeleteCartFightView.as_view(), name='fight_remove'),
    url(r'^cart/',CartView.as_view(), name='fight_cart'),
    url(r'^order/', OrderDetailView.as_view(), name='fight_order'),
    url(r'^comfirm/', ConfirmOrderView.as_view(), name='fight_confirm'),
    url(r'^myorder/', MyOrderDetailView.as_view(), name='myorder'),
    url(r'^gopay/(?P<order_id>.*)/', PayFightDetailView.as_view(), name='fight_gopay'),
    url(r"^pay/" ,AliPayView.as_view(),name="fight_alipay"),
]