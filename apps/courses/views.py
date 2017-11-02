# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course,CourseResources
from operation.models import UserFavorite,UserCourse,CourseComments
# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_course=Course.objects.all().order_by('-add_time')
        #热门课程推荐
        hot_course=all_course.order_by('-click_nums')[:3]
        sort=request.GET.get('sort','')
        key_word=request.GET.get('keyword','')
        if key_word:
            all_course=all_course.filter(Q(course_name__icontains=key_word)|Q(detail__icontains=key_word)
                                         |Q(desc__icontains=key_word))
        if sort:
            if sort == 'hot':
                #热门课程排序
                all_course=all_course.order_by('-click_nums')
            elif sort == 'students':
                #参加人数排序
                all_course=all_course.order_by('-learn_stu')
            else:
                return render(request,"404.html",{})
        course_num=all_course.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 9,request=request)

        all_course = p.page(page)
        return  render(request,"course-list.html",{
            'hots':hot_course,
            'courses':all_course,
            'sort':sort,
            'key_word':key_word,
            'course_num': course_num
        })

class CourseDetailView(View):
    def get(self,request,course_id):
        try:
            course=Course.objects.get(id=int(course_id))
        except:
            return render(request,'404.html',{})
        #增加课程点击数
        course.click_nums += 1
        course.save()
        tag=course.tag
        has_fav_cours=False
        has_fav_org=False
        if request.user.is_authenticated():
            has_fav_cours=UserFavorite.objects.filter(user=request.user,fav_id=int(course_id),fav_type=1)
            has_fav_org=UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2)
        if tag:
            commend=Course.objects.filter(tag=tag).exclude(course_name=course)[:2]
        else:
            commend=[]
        #获取该学生以外的学习该课程的学生
        stus=course.usercourse_set.filter(course_id=course).exclude(user_id=request.user.id)
        return render(request,'course-detail.html',{
            'courses':course,
            'commend':commend,
            'has_fav_org':has_fav_org,
            'has_fav_cours':has_fav_cours,
            'students':stus
        })


class CourseLessonView(View):
    def get(self, request, course_id):
        try:
            course=Course.objects.get(id=int(course_id))
        except:
            return render(request,'404.html',{})
        #保存到用户学习课程
        if request.user.is_authenticated():
            if not UserCourse.objects.filter(course_id=course_id,user_id=request.user.id):
                user_stu=UserCourse(course_id=course_id,user_id=request.user.id)
                user_stu.course_id=course_id
                user_stu.user_id=request.user.id
                user_stu.save()
                # 增加学习人数
                course.learn_stu += 1
                course.save()
            user_course=UserCourse.objects.filter(course_id=course_id)
            user_ids=[user_cours.user_id for user_cours in user_course]
            other_course = UserCourse.objects.filter(user_id__in=user_ids).exclude(course_id=course_id)
            other_course = set(other_cours.course for other_cours in other_course)
            other_course=list(other_course)[:3]
        else:
            return render(request,'login.html',{})
        all_resource=CourseResources.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course':course,
            'all_resource':all_resource,
            'other_courses': other_course,
        })

class CourseCommentView(View):
    def get(self,request,course_id):
        all_comments=CourseComments.objects.filter(course_id=course_id).order_by('-add_time')
        course=Course.objects.get(id=course_id)
        all_resource = CourseResources.objects.filter(course=course)
        user_course = UserCourse.objects.filter(course_id=course_id)
        user_ids = [user_cours.user_id for user_cours in user_course]
        other_course = UserCourse.objects.filter(user_id__in=user_ids).exclude(course_id=course_id)
        other_course = set(other_cours.course for other_cours in other_course)
        other_course = list(other_course)[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_comments, 8, request=request)
        all_comments = p.page(page)
        return render(request,'course-comment.html',{
            'active': 'course',
            'course_id': course_id,
            'all_comments':all_comments,
            'course':course,
            'all_resource': all_resource,
            'other_courses': other_course,
        })

class AddCommentView(View):
    def post(self,request):
        res = dict()
        if not request.user.is_authenticated():
            res['status'] = 'fail'
            res['msg'] = u'用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')
        course_id=request.POST.get('course_id',0)
        comment=request.POST.get('comments','')
        if course_id > 0 and comment:
            course_comment=CourseComments(course_id=course_id,user=request.user,comments=comment)
            course_comment.save()
            res['status'] = 'success'
            res['msg'] = u'发表成功'
        else:
            res['status']='fail'
            res['msg']=u'评论出错'
        return HttpResponse(json.dumps(res), content_type='application/json')





