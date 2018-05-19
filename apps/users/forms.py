# _*_ encoding:utf-8 _*_
from django import forms
from .models import UserProfile
from captcha.fields import CaptchaField

__author__ = 'YZF'
__date__ = '2018/3/14,17:14'


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)
    # 密码不能小于5位
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ResetPWViewForm(forms.Form):

    cord = forms.CharField(required=True)
    # 密码不能小于5位
    password1= forms.CharField(required=True, min_length=5)
    password2= forms.CharField(required=True, min_length=5)
    # 密码不能小于5位

class FindPWCordForm(forms.Form):
    email = forms.EmailField()
    change_captcha = forms.CharField(required=True)

class NickNameForm(forms.Form):
    nick_name= forms.CharField(required=True)



class WorkNameForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['work_name']

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']