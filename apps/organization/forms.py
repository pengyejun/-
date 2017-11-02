# -*- coding: utf-8 -*-
__date__ = '2017/10/20 17:08'
import re
from django import forms

from operation.models import UserAsk

class UserAskForm(forms.ModelForm):
    class Meta:
        model=UserAsk
        fields=['name', 'mobile', 'course']

    #验证手机号码
    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        match_mobile="^1[358]\d{9}$|^147\d{8}$"
        p=re.compile(match_mobile)
        if p.match(mobile):
            if UserAsk.objects.filter(mobile=mobile):
                raise forms.ValidationError(u'手机号码已经被注册',code="mobile_exist")
            else:
                return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code="mobile_invalid")