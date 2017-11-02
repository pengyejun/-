# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from organization.models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite



# Create your views here.

class OrgListView(View):
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        citys_num=all_citys.count()
        key_word = request.GET.get('keyword', '')
        if key_word:
            all_orgs = all_orgs.filter(Q(name__icontains=key_word) | Q(desc__icontains=key_word))
        #城市排名函数
        hot_orgs=all_orgs.order_by('-click_nums')[:5]

        #城市筛选函数
        city_id=request.GET.get('city','')
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))

        #学习人数排名
        sort=request.GET.get('sort','')
        if sort:
            if sort=='students':
                all_orgs=all_orgs.order_by('-student_nums')
            elif sort=='courses':
                all_orgs=sorted(all_orgs,key=CourseOrg.get_course_num,reverse=True)
        #机构类别筛选函数
        ctg=request.GET.get('ctg','')
        if ctg:
            all_orgs=all_orgs.filter(catgory=ctg)
        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5,request=request)

        orgs = p.page(page)
        org_nums = len(all_orgs)
        return render(request, "org-list.html",{"all_orgs":orgs, "org_nums":org_nums, "hot_orgs": hot_orgs,
                    "sort":sort, "ctg": ctg, "all_citys":all_citys,"citys_num": citys_num, "city_id":city_id,'key_word':key_word})


class AddUserAskView(View):
    #用户添加咨询
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        res = dict()
        if userask_form.is_valid():
            userask_form.save(commit=True)
            res['status'] = 'success'
        else:
            res['status'] = 'fail'
            res['msg'] = userask_form.errors['mobile']

        return HttpResponse(json.dumps(res), content_type='application/json')

class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        all_course = [teacher.course_set.all() for teacher in all_teachers]
        all_courses = [cour for course in all_course for cour in course]
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 2,request=request)
        all_courses = p.page(page)
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class OrgHomeView(View):
    def get(self,request,org_id):
        current_page='home'
        course_org=CourseOrg.objects.get(id=int(org_id))
        #django ORM外键的特殊用法
        all_teachers=course_org.teacher_set.all()
        all_course=[teacher.course_set.all() for teacher in all_teachers]
        all_courses=[cour for course in all_course for cour in course][:3]
        #判断是否收藏
        has_fav=False
        course_org.click_nums += 1
        course_org.save()
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=int(org_id),fav_type=2):
                has_fav=True
        return render(request,'org-detail-homepage.html',{
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class OrgDescView(View):
    def get(self,request,org_id):
        current_page='desc'
        course_org=CourseOrg.objects.get(id=int(org_id))
        #django ORM外键的特殊用法
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page='teacher'
        course_org=CourseOrg.objects.get(id=int(org_id))
        #django ORM外键的特殊用法
        all_teachers=course_org.teacher_set.all()
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        return render(request,'org-detail-teachers.html',{
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class AddFavView(View):
    def post(self,request):
        fav_id=request.POST.get('fav_id',0)
        fav_type=request.POST.get('fav_type',0)
        res=dict()
        if not request.user.is_authenticated():
            res['status'] = 'fail'
            res['msg']=u'用户未登录'
            return HttpResponse(json.dumps(res),content_type='application/json')
        exist_records=UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            #取消收藏
            exist_records.delete()
            res['status'] = 'fail'
            res['msg'] = u'收藏'
            if int(fav_type) == 1:
                #课程
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                course.save()
            elif int(fav_type) == 2:
                #机构
                course = CourseOrg.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                course.save()
            else:
                #讲师
                course = Teacher.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                course.save()
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite(user_id=request.user.id,fav_id=int(fav_id),fav_type=int(fav_type))
                user_fav.save()
                res['status']='success'
                res['msg']=u'已收藏'
                if int(fav_type) == 1:
                    # 课程
                    course=Course.objects.get(id=int(fav_id))
                    course.fav_nums+=1
                    course.save()
                elif int(fav_type) == 2:
                    # 机构
                    course = CourseOrg.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                else:
                    # 讲师
                    course = Teacher.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
            else:
                res['status']='fail'
                res['msg']=u'收藏出错'

        return HttpResponse(json.dumps(res), content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teachers=Teacher.objects.all()
        #讲师排行
        hot_teacher=all_teachers.order_by('-fav_nums')[:5]
        key_word=request.GET.get('keyword','')
        if key_word:
            all_teachers = all_teachers.filter(name__icontains=key_word)
        #人气排行
        sort=request.GET.get('sort','')
        if sort:
            all_teachers=all_teachers.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 5,request=request)

        teachers = p.page(page)
        teacher_nums = all_teachers.count()
        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'teacher_num':teacher_nums,
            'hot_teacher':hot_teacher,
            'sort':sort,
            'key_word':key_word,
        })


class TeacherDetailView(View):
    def get(self, request,teacher_id):
        all_teachers = Teacher.objects.all()
        # 讲师排行
        hot_teacher = all_teachers.order_by('-fav_nums')[:5]
        teacher=Teacher.objects.get(id=int(teacher_id))
        all_course=Course.objects.filter(teacher_id=teacher_id)
        org=teacher.jigou
        has_fav_teacher=False
        has_fav_org=False
        teacher.click_nums += 1
        teacher.save()
        if UserFavorite.objects.filter(fav_type=3,fav_id=int(teacher_id)):
            has_fav_teacher=True
        if UserFavorite.objects.filter(fav_type=2,fav_id=int(teacher_id)):
            has_fav_org=True
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_course':all_course,
            'hot_teacher':hot_teacher,
            'org':org,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
        })

