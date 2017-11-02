# -*- coding: utf-8 -*-
__date__ = '2017/10/16 13:57'
import re
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username=forms.CharField(required=True,min_length=5)
    password=forms.CharField(required=True,max_length=20,min_length=6)


class RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=20, min_length=6)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, max_length=20, min_length=6)
    password2 = forms.CharField(required=True, max_length=20, min_length=6)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['image']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['nike_name','birth','gender','address','mobile']

    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        match_mobile="^1[358]\d{9}$|^147\d{8}$"
        p=re.compile(match_mobile)
        if p.match(mobile):
            if UserProfile.objects.filter(mobile=mobile):
                raise forms.ValidationError(u'手机号码已经被注册',code="mobile_exist")
            else:
                return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code="mobile_invalid")