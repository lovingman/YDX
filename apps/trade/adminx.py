# _*_ encoding:utf-8 _*_
import xadmin
from .models import Order, OrderDetail, Cart

__author__ = 'YZF'
__date__ = '2018/4/5,12:44'


class OrderAdmin:
    pass


class OrderDetailAdmin:
    pass


class CartAdmin:
    pass


xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(OrderDetail, OrderDetailAdmin)
xadmin.site.register(Cart, CartAdmin)
