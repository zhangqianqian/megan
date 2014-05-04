#-*- coding:utf-8 -*-
import random
import hashlib
from myapp import app
from flask import render_template,request,flash,redirect,url_for
from myapp.models.user_model import *
from myapp.utils.sendmail import send_regist_mail
@app.route('/regist',methods=['POST','GET'])
def regist():
	return render_template('regist.html')
@app.route('/register',methods=['POST','GET'])
def welcome():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        email = request.form['email'].strip()
        userquery=UserRegistQuery()
        user = userquery.get_by_email(email)
        if user:
            flash(u'该邮件已经注册')
        else:
            code = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',20))
            regist_result = send_regist_mail(email, code)
            if regist_result:
                UserRegist.create(email, code)
                return render_template('password.html',email=email)
            else:
                flash(u'发送失败，请重试')
                return redirect(url_for('regist'))
@app.route('/init-password', methods=['GET','POST'])
def init_password():
    if request.method == 'POST':
        new_email = request.form['email']
        password = request.form['password']
        new_salt = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',20))
        print '1 salt:',new_salt
        en_password=hashlib.md5(password+new_salt).hexdigest()
        print '1 en_password:',en_password
        username=new_email.split('@')[0]
        new_user = User.create(salt=new_salt,email=new_email, password=en_password, create_time=datetime.now(),status='1',username=username)
        #return render_template('login.html',email=new_email)
        return redirect(url_for('login'))
    else:
        flash(u"密码初始化失败……")
@app.route('/init-user',methods=['POST','GET'])
def init_user():
    if request.method == "GET":
        email = request.args.get('email')
        code = request.args.get('code')
        r_user = User.user_query.get_by_email(email)
        if r_user:
            r_user.set_status('1')
            return redirect(url_for('login'))
        else:
            return render_template('password.html', email=email)
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        email = request.args.get('email')
        return render_template('login.html',email=email)
    elif request.method == 'POST':
        email = request.form['email']
        check_password = request.form['password']
        r_user = User.user_query.get_by_email(email)
        origin_salt=r_user.salt
        print '2 salt:',origin_salt
        origin_pass=r_user.password
        print '2 en pass',origin_pass
        en_password=hashlib.md5(check_password+origin_salt).hexdigest()
        print '3 en pass',en_password
        if en_password == origin_pass:
            return redirect(url_for('write'))
        else:
            return redirect(url_for('login'))

@app.route('/write', methods=['GET','POST'])
def write():
    return 'login sussessfully'
