# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"城市"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name=models.CharField(max_length=50,verbose_name=u"机构名称")
    catgory=models.CharField(default="pxjg", choices=(("pxjg", u"培训机构"),("gx", u"高校"),("gr", u"个人")),max_length=4,verbose_name=u"机构类别")
    tag=models.CharField(max_length=10, verbose_name=u'标签', default=u'全国知名')
    desc=models.TextField(verbose_name=u"机构描述")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    img = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    city = models.ForeignKey(CityDict,verbose_name=u"所在城市")
    student_nums = models.IntegerField(default=0, verbose_name=u"学习人数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"课程机构"
        verbose_name_plural=verbose_name

    def get_teacher_num(self):
        #获取机构教师数量
        return self.teacher_set.all().count()

    def get_course_num(self):
        #获取机构课程数量
        return self.course_set.all().count()

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    jigou=models.ForeignKey(CourseOrg,verbose_name=u"所属机构")
    name=models.CharField(max_length=20, verbose_name=u"教师名称")
    age=models.IntegerField(default=0,verbose_name=u"教师年龄")
    teacher_img = models.ImageField(upload_to="org_teather/%Y/%m", verbose_name="photo", max_length=100,null=True,blank=True)
    work_years=models.IntegerField(default=0,verbose_name=u"工作年限")
    work_company=models.CharField(max_length=50,verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"工作职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    class Meta:
        verbose_name=u"教师"
        verbose_name_plural=verbose_name

    def get_course(self):
        return self.course_set.count()

    def __unicode__(self):
        return self.name