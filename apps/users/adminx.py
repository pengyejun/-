# -*- coding: utf-8 -*-
__date__ = '2017/10/14 15:57'

import xadmin
from xadmin import views

from users.models import EmailVerifyCode,Banner


class BaseSetting(object):
    enable_themes=True  #主题设置
    # use_bootswatch=True


class GlobalSettings(object):
    site_title=u"慕学后台管理系统" #左上角标题
    site_footer=u"慕学在线教育网" #页脚
    menu_style="accordion"  #收起左侧APP栏

class EmailVerifyCodeAdmin(object):
    list_display = ['code','email','send_type','send_time']   #列表字段
    search_fields=['code','email','send_type'] #搜索字段,无法对时间search
    list_filter = ['code','email','send_type','send_time']   #筛选字段


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']  # 列表字段
    search_fields = ['title', 'image', 'url', 'index']  # 搜索字段,无法对时间search
    list_filter = ['title', 'image', 'url', 'index','add_time']  # 筛选字段


xadmin.site.register(EmailVerifyCode,EmailVerifyCodeAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)


