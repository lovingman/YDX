# _*_ encoding:utf-8 _*_
from django.conf.urls import url
from courses.views import CourseProgessView,SearchView,FightDetailView,CourseListView,CourseDetailView,AddFavoriteView,VideoPlayView,CommentsView,AddCommentsView
__author__ = 'YZF'
__date__ = '2018/3/26,9:09'
urlpatterns =[
    url(r'^list',CourseListView.as_view(),name="courser_list"),
    url(r'^detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
    url(r'^fightdetail/(?P<course_id>\d+)/',FightDetailView.as_view(), name='fight_detail'),
    url(r'^addfav/',AddFavoriteView.as_view(),name="addfav_course"),
    url(r'^video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video"),
    url(r'^progess/', CourseProgessView.as_view(), name="progess"),
    url(r'^comments/(?P<course_id>\d+)/',CommentsView.as_view(), name="comments"),
    url(r'^addcomments/',AddCommentsView.as_view(), name="addcomments"),
    url(r'^search/',SearchView.as_view(), name="search"),


]