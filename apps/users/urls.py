# -*- coding: utf-8 -*-
__date__ = '2017/10/27 17:32'
from django.conf.urls import url,include
from .views import UserInfoView,UploadImageView,ModifyPwdInfoView,SendEmailView,\
    UpdateEmailView,UserInfoCourseView,UserFavOrgView,UserFavTeacherView,UserFavCourseView,UserMessageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(),name='info'),
    #用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(),name='image_upload'),
    #个人中心修改密码
    url(r'^update/pwd/$', ModifyPwdInfoView.as_view(),name='update_pwd'),
    #发送邮箱验证码
    url(r'^send_code/$', SendEmailView.as_view(),name='send_code'),
    #修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    #我的课程
    url(r'^mycourse/$', UserInfoCourseView.as_view(), name='mycourse'),
    #我的收藏
    url(r'^fav/org/$', UserFavOrgView.as_view(), name='fav_org'),
    url(r'^fav/teacher/$', UserFavTeacherView.as_view(), name='fav_teacher'),
    url(r'^fav/course/$', UserFavCourseView.as_view(), name='fav_course'),
    #我的消息
    url(r'^message/$', UserMessageView.as_view(), name='message'),
]