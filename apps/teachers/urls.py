# _*_ encoding:utf-8 _*_

__author__ = 'YZF'
__date__ = '2018/4/1,15:08'
# _*_ encoding:utf-8 _*_
from django.conf.urls import url
from teachers.views import TeacherDetailView

urlpatterns =[
    url(r'^detail/(?P<teacher_id>\d+)/',TeacherDetailView.as_view(), name="teacher_detail"),
]