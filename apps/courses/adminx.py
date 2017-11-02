# -*- coding: utf-8 -*-
__date__ = '2017/10/14 18:07'

import xadmin

from courses.models import Video,Course,Lesson,CourseResources


class CourseAdmin(object):
    list_display = ['course_name', 'desc', 'detail', 'degree','learn_time','learn_stu','fav_nums','img','click_nums','add_time']  # 列表字段
    search_fields = ['course_name', 'desc', 'detail', 'degree','learn_stu','fav_nums','img','click_nums']  # 搜索字段,无法对时间search
    list_filter = ['course_name', 'desc', 'detail', 'degree','learn_time','learn_stu','fav_nums','img','click_nums','add_time']  # 筛选字段


class LessonAdmin(object):
    list_display = ['course', 'chapter_name', 'add_time']  # 列表字段
    search_fields = ['course', 'chapter_name']   # 搜索字段,无法对时间search
    list_filter = ['course__course_name', 'chapter_name', 'add_time']   # 筛选字段  #course__course_name 外键字段筛选


class VideoAdmin(object):
    list_display = ['lesson', 'video_name', 'add_time']  # 列表字段
    search_fields = ['lesson', 'video_name']   # 搜索字段,无法对时间search
    list_filter = ['lesson__chapter_name', 'video_name', 'add_time']   # 筛选字段


class CourseResourcesAdmin(object):
    list_display = ['course', 'resource_name', 'add_time','download']  # 列表字段
    search_fields = ['course', 'resource_name','download']   # 搜索字段,无法对时间search
    list_filter = ['course__course_name', 'resource_name', 'add_time','download']   # 筛选字段


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResources, CourseResourcesAdmin)

