# _*_ encoding:utf-8 _*_
import xadmin
from .models import UserFavorite,UserCourse,CourseComments
__author__ = 'YZF'
__date__ = '2018/3/14,14:14'


class UserFavoriteAdmin:
    pass


class UserCourseAdmin:
    pass


class CourseCommentsAdmin:
    pass






xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
