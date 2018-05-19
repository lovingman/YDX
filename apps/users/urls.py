# _*_ encoding:utf-8 _*_
from django.conf.urls import url
from users.views import LoginView,LogoutView,RegisterView,ActiveUserView,IndexView\
    ,ForgetPWView,FindPWCordView,UserInfoView,NickNameView,WorkNameView,UploadImageView,MyCourseView,\
    DeleteMyCourseView,MyFavCouresView,MyFavTeacherView,MyPhoneView
__author__ = 'YZF'
__date__ = '2018/3/14,16:26'
urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^register/',RegisterView.as_view(),name='register'),
    # url(r'forget/(?P<email>.*)*/',ForgetPWView.as_view(),name='forget'),
    url(r'^forget/', ForgetPWView.as_view(), name='forget'),
    url(r'^logout/',LogoutView.as_view(),name='logout'),
    url(r'^forget_cord/',FindPWCordView.as_view(),name='forgetcord'),
    # 激活用户url
    url('^active/(?P<active_code>.*)/', ActiveUserView.as_view(), name= "user_active"),
    url('^info/', UserInfoView.as_view(), name="user_info"),
    url('^nickname/', NickNameView.as_view(), name="info_nickname"),
    url('^phone/', MyPhoneView.as_view(), name="info_phone"),
    url('^workname/', WorkNameView.as_view(), name="info_workname"),
    url(r'^mycourses/', MyCourseView.as_view(), name='info_courses'),
    url(r'^favteacher/', MyFavTeacherView.as_view(), name='fav_teacher'),
    url(r'^myfav/', MyFavCouresView.as_view(), name='info_myfav'),
    url('^delete/(?P<course_id>.*)/', DeleteMyCourseView.as_view(), name= "course_delete"),
    url(r'^uploadoimg/', UploadImageView.as_view(), name='image_upload'),


]