# -*- coding: utf-8 -*-
__date__ = '2017/10/20 17:16'
from django.conf.urls import url

from .views import OrgListView,AddUserAskView,OrgCourseView,OrgHomeView,OrgDescView,OrgTeacherView,AddFavView,TeacherListView,TeacherDetailView

urlpatterns = [
#课程机构首页
    url(r'^list/$',OrgListView.as_view(),name="org_list"),
    url(r'^add_ask/$',AddUserAskView.as_view(),name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name="org_desc"),
    url(r'^teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name="org_teacher"),
    #机构收藏
    url(r'^add_fav/$',AddFavView.as_view(),name="add_fav"),
    #讲师列表页
    url(r'^teacher/list/$',TeacherListView.as_view(),name="teacher_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$',TeacherDetailView.as_view(),name="teacher_detail"),
]