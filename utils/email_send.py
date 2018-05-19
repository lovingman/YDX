# _*_ encoding:utf-8 _*_
from random import Random
from  users.models import EmailVerifyRecord
# 导入Django自带的邮件模块
from django.core.mail import send_mail,EmailMessage
# 导入setting中发送邮件的配置
from YDX.settings import EMAIL_FROM
# 发送html格式的邮件:
from django.template import loader
__author__ = 'YZF'
__date__ = '2018/3/15,14:33'

# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    if send_type == "update":
        code = random_str(4)
    elif send_type == "forget":
        code = random_str(8)
    else:
        code = random_str(6)

    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 定义邮件内容:
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "欢迎云导学 注册激活链接"
        email_body=""
        email_body = loader.render_to_string(
            "usercenter/email_register.html",  # 需要渲染的html模板
            {
                "active_code": code  # 参数
            }
        )

        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        # send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功


    elif send_type == 'forget':
        email_title = "忘记密码的验证码"
        email_body = "你的验证码是{0}".format(code)
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        send_status = msg.send()
    if send_status:
        return True
    else:
        return False





