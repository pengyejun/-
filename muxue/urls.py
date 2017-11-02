# _*_ encoding:utf-8 _*_
"""muxue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.generic import TemplateView
import xadmin

from users.views import LoginView,RegisterView,ActiveUserView,FogetPwdView,ResetPwdView,ModifyPwdView,LogoutView,IndexView
from muxue.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),   #处理静态文件
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$',FogetPwdView.as_view(),name="forget_pwd"),
    url(r'^resetpwd/(?P<active_code>.*)/$',ResetPwdView.as_view(),name="reset_pwd"),
    url(r'^modify/$',ModifyPwdView.as_view(),name="modify_pwd"),
    #课程机构url配置
    url(r'^org/', include('organization.urls',namespace="org")),
    #公开课url配置
    url(r'^course/', include('courses.urls',namespace="course")),
    #用户相关配置
    url(r'^users/', include('users.urls',namespace="user")),
    #处理上传文件的处理函数
    url(r'^media/(?P<path>.*)$', serve,{"document_root": MEDIA_ROOT}),
]
