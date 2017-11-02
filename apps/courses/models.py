# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher

# Create your models here.


class Course(models.Model):
    course_name=models.CharField(max_length=50,verbose_name=u"课程名称")
    course_org=models.ForeignKey(CourseOrg,verbose_name=u"所属机构",null=True,blank=True)
    is_banner=models.BooleanField(default=False,verbose_name=u'是否轮播')
    teacher=models.ForeignKey(Teacher,verbose_name=u"课程教师",null=True,blank=True)
    course_need=models.CharField(max_length=300,verbose_name=u"课程须知",null=True,blank=True)
    teacher_speak=models.CharField(max_length=300,verbose_name=u"老师告诉",default='')
    category=models.CharField(max_length=20,verbose_name=u"课程类别",default=u"开发")
    desc=models.CharField(max_length=300,verbose_name=u"课程描述")
    detail=models.TextField(verbose_name=u"课程详情")
    degree=models.CharField(choices=(("primary", "初级"), ("middle", "中级"), ("high", "高级")), verbose_name=u"课程难度", max_length=10)
    learn_time=models.IntegerField(default=0,verbose_name=u"学习时长(分钟)")
    learn_stu=models.IntegerField(default=0,verbose_name=u"学习人数")
    fav_nums=models.IntegerField(default=0,verbose_name=u"收藏人数")
    img=models.ImageField(upload_to="course/%Y/%m",verbose_name=u"封面图",max_length=70)
    click_nums=models.IntegerField(default=0,verbose_name=u"点击数")
    tag=models.CharField(max_length=10,default='',verbose_name=u"课程标签")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"课程"
        verbose_name_plural=verbose_name

    def get_lesson(self):
        #获取课程章节数
        return self.lesson_set.all().count()

    def get_course_lesson(self):
        # 获取课程章节
        return self.lesson_set.all()


    def __unicode__(self):
        return self.course_name


class Lesson(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程")
    chapter_name=models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"章节"
        verbose_name_plural=verbose_name

    def get_lesson_video(self):
        #获取视频信息
        return self.video_set.all()

    def __unicode__(self):
        return self.chapter_name

class Video(models.Model):
    lesson=models.ForeignKey(Lesson,verbose_name=u"章节")
    video_name = models.CharField(max_length=100, verbose_name=u"视频名称")
    url=models.CharField(max_length=200,verbose_name=u"访问链接",default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"视频"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.video_name


class CourseResources(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程")
    resource_name = models.CharField(max_length=100, verbose_name=u"名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    download=models.FileField(upload_to="course/%Y/%m",verbose_name=u"下载地址",max_length=100)


    class Meta:
        verbose_name=u"课程资源"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.resource_name