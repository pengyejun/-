# -*- coding: utf-8 -*-
__date__ = '2017/10/14 19:21'

import xadmin
from organization.models import CourseOrg,CityDict,Teacher


class CityDictAdmin(object):
    list_display = ['name','add_time']  # 列表字段
    search_fields = ['name']  # 搜索字段,无法对时间search
    list_filter = ['name','add_time']  # 筛选字段


class CourseOrgAdmin(object):
    list_display = ['name','desc','click_nums','fav_nums','img','address','city', 'add_time']  # 列表字段
    search_fields = ['name','desc','click_nums','fav_nums','img','address','city']  # 搜索字段,无法对时间search
    list_filter = ['name','desc','click_nums','fav_nums','img','address','city__name','add_time']  # 筛选字段


class TeacherAdmin(object):
    list_display = ['jigou', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums','fav_nums', 'add_time']  # 列表字段
    search_fields = ['jigou', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums','fav_nums'] # 搜索字段,无法对时间search
    list_filter = ['jigou__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums','fav_nums','add_time']  # 筛选字段


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)