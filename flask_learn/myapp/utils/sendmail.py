# -*- coding:utf-8 -*-

import re
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from myapp.app_config import MAIL_HOST, MAIL_USERNAME, MAIL_PASSWORD

def send_regist_mail(mail_to , code):
    def __generate_regist_url():
        f = open('/root/megan/flask_learn/myapp/utils/regist_mail.tpl','r')
        body = f.read()
        base_url = 'http://192.168.122.235:5000/init-user?email=%s&code=%s'
        body_url = base_url %(mail_to, code)
        return body.format(body_url)
    try:
        title = '欢迎注册funtyping'
        body = __generate_regist_url()
        send_mail(mail_to, title, body)
        return True
    except:
        return False
def send_mail(mail_to, title, body):
    # 构造邮件消息格式
    message =  MIMEText(body,'html','utf-8')
    message['From'] = MAIL_USERNAME
    message['To'] = mail_to
    message['Subject'] = title

    # 连接到服务器 
    mail_server = smtplib.SMTP()
    mail_server.connect(MAIL_HOST)
    # 登录到邮件服务器
    mail_server.login(MAIL_USERNAME, MAIL_PASSWORD)
    # 发送邮件
    mail_server.sendmail(MAIL_USERNAME, mail_to, message.as_string())
    # 退出
    mail_server.close()
