# -*- coding: utf-8 -*-
__date__ = '2017/10/14 18:23'

import xadmin

from operation.models import UserAsk,UserCourse,UserFavorite,UserMessage,CourseComments

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course', 'add_time']  # 列表字段
    search_fields = ['name', 'mobile', 'course']   # 搜索字段,无法对时间search
    list_filter = ['name', 'mobile', 'course', 'add_time'] # 筛选字段


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']  # 列表字段
    search_fields = ['user', 'course', 'comments']  # 搜索字段,无法对时间search
    list_filter = ['user__nike_name', 'course__course_name', 'comments', 'add_time']  # 筛选字段


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']  # 列表字段
    search_fields = ['user', 'fav_id', 'fav_type']  # 搜索字段,无法对时间search
    list_filter = ['user__nike_name', 'fav_id', 'fav_type', 'add_time']  # 筛选字段


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']  # 列表字段
    search_fields = ['user', 'message', 'has_read']  # 搜索字段,无法对时间search
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 筛选字段


class UserCourseAdmin(object):
    list_display = ['user', 'course','add_time']  # 列表字段
    search_fields = ['user', 'course']  # 搜索字段,无法对时间search
    list_filter = ['user__nike_name', 'course__course_name','add_time']  # 筛选字段


xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)