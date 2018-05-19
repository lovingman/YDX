"""YDX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.static import serve
# from django.contrib import admin
from  YDX.settings import MEDIA_ROOT
from users.views import IndexView
from otherapps import xadmin
from users.views import LoginView

urlpatterns = [
  url(r'^admin/', xadmin.site.urls),
  url(r'^login/', LoginView.as_view(), name='login'),
  url(r'index/',IndexView.as_view(),name="index"),
  url("users/", include('users.urls', namespace="users")),
  url("courses/", include('courses.urls', namespace="courses")),
  url("teachers/", include('teachers.urls', namespace="teachers")),
  url(r'^captcha/', include('captcha.urls')),
  url('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),
  url('fights/',include('trade.urls',namespace='fights'))
]
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'