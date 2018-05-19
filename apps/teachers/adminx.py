# _*_ encoding:utf-8 _*_
import xadmin
from .models import Teacher
__author__ = 'YZF'
__date__ = '2018/3/14,14:11'


class TeacherAdmin:
    pass

xadmin.site.register(Teacher,TeacherAdmin)
