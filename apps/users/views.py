# _*_ encoding:utf-8 _*_
import json

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile,EmailVerifyCode,Banner
from .forms import LoginForm,RegisterForm,ForgetForm,ResetPwdForm,UploadImageForm,UpdateUserForm
from utils.email_send import send_register_email
from utils.LoginRequired import LoginRequiredMixin
from operation.models import UserCourse,UserFavorite,UserMessage
from courses.models import Course
from organization.models import CourseOrg,Teacher
# Create your views here.


class CustomBackend(ModelBackend):             #自定义authenticate
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username)) #数据库中取用户名
            if user.check_password(password):     #数据库中检查密码是否正确
                return user
        except Exception as e:
            return None
#________________________________________________________________________________________________________
#
# def user_login(request):
#     if request.method == "POST":
#         user_name=request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user=authenticate(username=user_name, password=pass_word)   #认证用户名和密码  认证成功返回user对象，失败为None
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {"msg":u"用户名或密码错误!!!"})
#     elif request.method == "GET":
#         return render(request, "login.html",{})


#___________________________________________________________________________________________________分隔符
#基于类实现登录
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user=authenticate(username=user_name, password=pass_word)   #认证用户名和密码  认证成功返回user对象，失败为None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"login_form": login_form,"msg": u"用户未激活!"})
            else:
                return render(request, "login.html", {"login_form": login_form, "msg": u"用户名或密码错误!!!"})
        else:
            return render(request, "login.html", {"login_form":login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


#用户注册
class RegisterView(View):
    def get(self, request):
        next=request.GET.get('next','/')
        register_form=RegisterForm()
        return render(request, "register.html", {"register_form":register_form, 'next':next})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email=request.POST.get("email","")
            if UserProfile.objects.filter(email=email):
                return render(request, "register.html", {"register_form": register_form,"msg": "用户已经存在!"})
            pass_word=request.POST.get("password","")
            user=UserProfile(username=email,email=email,password=make_password(pass_word))
            user.save()
            #写入欢迎注册信息
            user_message=UserMessage()
            user_message.user=user.id
            user_message.message="欢迎注册慕学在线网"
            user_message.save()
            send_register_email(email,"register")
            return render(request, "login.html",{})
        else:
            return render(request, "register.html", {"register_form": register_form})


#激活用户
class ActiveUserView(View):
    #get只返回一个记录，filter返回一个记录集，而且如果没有找到记录的话，get会raise一个异常，filter只是返回一个空列表
    def get(self, request,active_code):
        all_records=EmailVerifyCode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
                EmailVerifyCode.objects.filter(code=active_code).delete()
                return render(request, "active_true.html")
        else:
            return render(request, "code_false.html")



#忘记密码
class FogetPwdView(View):
    def get(self, request):
        forget_form=ForgetForm()
        return render(request, "forgetpwd.html",{"forget_form":forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get("email","")
            if UserProfile.objects.filter(email=email):
                send_register_email(email, "find_passwd")
                return render(request,"send_success.html")
            else:
                return render(request,"forgetpwd.html",{"forget_form": forget_form,"msg": "邮箱不存在,请重新输入!"})
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetPwdView(View):
    def get(self, request,active_code):
        all_records=EmailVerifyCode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                return render(request, "password_reset.html", {"email": email,"code":active_code})
        else:
            return render(request,"code_false.html")


class ModifyPwdView(View):
    def post(self, request):
        reset_pwd=ResetPwdForm(request.POST)
        if reset_pwd.is_valid():
            pwd1=request.POST.get("password1")
            pwd2=request.POST.get("password2")
            email=request.POST.get("email","")
            code=request.POST.get("code","")
            if pwd1 == pwd2:
                user=UserProfile.objects.get(email=email)
                user.password=make_password(pwd1)
                user.save()
                EmailVerifyCode.objects.filter(code=code).delete()
                return render(request, "login.html")
            else:
                return render(request,"password_reset.html",{"msg":"两次输入的密码不一致","email":email})
        else:
            email = request.POST.get("email", "")
            return render(request,"password_reset.html",{"reset_pwd": reset_pwd, "email":email})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html',{})
        return render(request, 'usercenter-info.html',{
            'user' : request.user,
        })

    def post(self, request):
        user_form=UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            print json.dumps(user_form.errors)
            return HttpResponse(json.dumps(user_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        #文件类型放在request.FILES
        image_form=UploadImageForm(request.POST, request.FILES,instance=request.user)
        res = dict()
        if image_form.is_valid():
            image_form.save()
            res['status'] = 'success'
            res['msg'] = u'头像修改成功'
        else:
            res['status'] = 'fail'
            res['msg'] = u'头像修改出错'
        return HttpResponse(json.dumps(res), content_type='application/json')


class ModifyPwdInfoView(LoginRequiredMixin, View):

    #用户中心修改密码
    def post(self, request):
        res = dict()
        reset_pwd=ResetPwdForm(request.POST)
        if reset_pwd.is_valid():
            pwd1=request.POST.get("password1")
            pwd2=request.POST.get("password2")
            if pwd1 == pwd2:
                user=request.user
                user.password=make_password(pwd1)
                user.save()
                res['status'] = 'success'
                res['msg'] = '密码修改成功'
            else:
                res['status'] = 'fail'
                res['msg'] = u'密码不一致'
        else:
            res['status'] = 'fail'
            res['msg'] = u'密码格式不对'
        return HttpResponse(json.dumps(res), content_type='application/json')


class SendEmailView(LoginRequiredMixin, View):
    def get(self, request):
        email=request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        else:
            send_register_email(email,'update_email')
            return HttpResponse('{"status":"success"}', content_type='application/json')

class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code=request.POST.get('code','')
        exist=EmailVerifyCode.objects.filter(email=email,code=code,send_type='update_email')
        if exist:
            request.user.email=email
            request.user.save()
            exist.delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class UserInfoCourseView(LoginRequiredMixin, View):
    def get(self, request):
        all_course=UserCourse.objects.filter(user_id=request.user.id)
        all_ids=[course.course_id for course in all_course]
        all_course=Course.objects.filter(id__in=all_ids)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 8,request=request)

        all_course = p.page(page)
        return render(request,'usercenter-mycourse.html',{
            'courses': all_course,
        })


class UserFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        fav_org = UserFavorite.objects.filter(user_id=request.user.id,fav_type=2)
        org_ids=[org.fav_id for org in fav_org]
        fav_org=CourseOrg.objects.filter(id__in=org_ids)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(fav_org, 5,request=request)

        fav_org = p.page(page)
        return render(request, 'usercenter-fav-org.html', {
            'all_org': fav_org,
        })


class UserFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        fav_teacher = UserFavorite.objects.filter(user_id=request.user.id, fav_type=3)
        teacher_ids=[org.fav_id for org in fav_teacher]
        fav_teacher=Teacher.objects.filter(id__in=teacher_ids)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(fav_teacher, 5, request=request)

        fav_teacher = p.page(page)
        return render(request, 'usercenter-fav-teacher.html', {
            'all_teacher': fav_teacher,
        })


class UserFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        fav_course = UserFavorite.objects.filter(user_id=request.user.id, fav_type=1)
        course_ids=[org.fav_id for org in fav_course]
        fav_course=Course.objects.filter(id__in=course_ids)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(fav_course, 8, request=request)

        fav_course = p.page(page)
        return render(request, 'usercenter-fav-course.html', {
            'all_course': fav_course,
        })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_message=UserMessage.objects.filter(user=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 8, request=request)

        all_message = p.page(page)
        #未读数据标记为已读
        messages=UserMessage.objects.filter(user=request.user.id)
        for message in messages:
            message.has_read=True
            message.save()
        return render(request,'usercenter-message.html', {
            'messages': all_message,
        })


class IndexView(View):
    def get(self, request):
        all_banner=Banner.objects.all().order_by('index')
        banner_course=Course.objects.filter(is_banner=True)[:3]
        hot_course=Course.objects.all().order_by('-click_nums')[:6]
        hot_org=CourseOrg.objects.all().order_by('-click_nums')[:15]
        return render(request, 'index.html',{
            'all_banner': all_banner,
            'banner_course': banner_course,
            'hot_courses': hot_course,
            'hot_orgs': hot_org,
        })
