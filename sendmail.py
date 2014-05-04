#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib
from email.mime.text import MIMEText

# 定义发送列表 
mailto_list=["475859443@qq.com","baiyueliang@yeah.net",""]
# 设置服务器名称、用户名、密码以及邮件后缀 
mail_host = "smtp.yeah.net" 
mail_user = "mailtestmail" 
mail_pass = "123qwe" 
mail_postfix="yeah.net" 

# 发送邮件函数 
def send_mail(to_list, sub, context): 
    '''
    to_list: 发送给谁
    sub: 主题
    context: 内容
    send_mail("xxx@126.com","sub","context")
    ''' 
    me = mail_user + "<"+mail_user+"@"+mail_postfix+">" 
    msg = MIMEText(context) 
    msg['Subject'] = sub 
    msg['From'] = me 
    msg['To'] = ";".join(to_list) 
    try: 
        send_smtp = smtplib.SMTP() 
        send_smtp.connect(mail_host) 
        send_smtp.login(mail_user, mail_pass) 
        send_smtp.sendmail(me, to_list, msg.as_string()) 
        send_smtp.close() 
        return True
    except (Exception, e): 
        print(str(e)) 
        return False

if __name__ == '__main__': 
    if (True == send_mail(mailto_list,"zhangqianqian","context")): 
        print ("测试成功")
    else: 
        print ("测试失败") 
