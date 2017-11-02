# -*- coding: utf-8 -*-
__date__ = '2017/10/12 13:30'
from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyCode
from muxue.settings import EMAIL_FROM


def random_str(randomlength=8):
    str=''
    a = ''.join(map(chr, range(65, 91)))
    b = a.lower()
    c = '0123456789'
    chars=''
    for i in range(26):
        chars=chars+a[i]+b[i]
    chars=chars+c
    length=len(chars)-1
    random=Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

def send_register_email(email, send_type="register"):
    email_code=EmailVerifyCode()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code=random_str(8)
    email_code.code=code
    email_code.email=email
    email_code.send_type=send_type
    email_code.save()

    email_title=''
    email_body=''

    if send_type == "register":
        email_title="欢迎注册慕学在线网"
        email_body="请点击如下链接激活您的账号:http://127.0.0.1:8000/active/{0}".format(code)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == "find_passwd":
        email_title="慕学在线网密码重置链接"
        email_body="点击如下链接重置密码：http://127.0.0.1:8000/resetpwd/{0}".format(code)
        send_status=send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title="慕学在线邮箱修改验证码"
        email_body="你的邮箱验证码：{0}".format(code)
        send_status=send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
