# -*- coding: utf-8 -*-
__date__ = '2017/10/23 14:19'
from django.conf.urls import url

from .views import CourseListView,CourseDetailView,CourseLessonView,CourseCommentView,AddCommentView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name="detail"),
    url(r'^video/(?P<course_id>\d+)$', CourseLessonView.as_view(), name="video"),
    url(r'^comment/(?P<course_id>\d+)$', CourseCommentView.as_view(), name="comment"),
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
]