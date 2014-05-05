#-*- coding:utf-8 -*-
import random
import hashlib
from myapp import app
from flask import render_template,request,flash,redirect,url_for,session
from myapp.models.user_model import *
from myapp.models.blog import *
from myapp.utils.util import get_user_id
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
        #email = request.args.get('email')
        #return render_template('login.html',email=email)
        return render_template('login.html')
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
            session["user_id"] = r_user.id
            print 'user_id from session:%s'%session["user_id"]
            return render_template('write.html')
        else:
            return redirect(url_for('login'))

@app.route('/write', methods=['GET','POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')
    elif request.method == 'POST':
        note_date = request.form['note_date']
        note_content = request.form['note_content']
        #写入数据库：user_id, time, content, update_time=time
        user_id = get_user_id()
        note = Blog.create(user_id, content=note_content, time=note_date)
        return render_template('note.html', note=note)

@app.route('/logout')
def logout():
    if "user_id" in session:
        del session["user_id"]
    return redirect(url_for('login'))
@app.route('/latest')
def latest():
    if get_user_id():
        user_id = get_user_id()
        note = Blog.blog_query.get_recent_blog_by_user(user_id)
        if not note:
            return redirect(url_for('no_notes'))
        note.weekday = note.time.strftime('%A')
        note.time = note.time.date()

    else:
        return redirect(url_for('login'))
    return render_template('note.html', note=note)

@app.route('/no_notes')
def no_notes():
    return render_template('no_notes.html')

@app.route('/notes/<datenum>')
@app.route('/notes')
def notes(datenum=None):
    date_list=[]
    user_id = get_user_id()
    notes = Blog.blog_query.get_blog_by_author(user_id)
    if datenum is None:
        datenum = ''
    elif datenum:
        for note in notes:
            times = note.time.date()
            if times.strftime('%Y%m')==datenum:
                date_list = list(set(date_list))
    else:
        for note in notes:
            times = note.time.date()
            date_list.append(note.strftime('%Y%m'))
            date_list = list(set(date_list))
    for nn in notes:
        nn.weekday = nn.time.strftime('%A')
        nn.time = nn.time.strftime('%Y-%m-%d')
    return render_template('note_list.html', notes = notes, date_list = date_list, datenum = datenum)

@app.route('/setting/password',methods=['GET','POST'])
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')
    elif request.method == 'POST':
        user_id = get_user_id()
        old_password = request.form['old']
        new_password = request.form['new']
        confirm_password = request.form['confirm']
        if new_password != confirm_password or new_password =='':
            flash(u'两次输入的密码不一致')
            return redirect(url_for('setpasswd'))
        user = User.user_query.get_by_id(user_id)
        salt = user.salt
        oldold_password = hashlib.md5(old_password+salt).hexdigest()
        if oldold_password == user.password:
            user.set_password(new_password,salt)
            flash(u'密码已修改')
        else:
            flash(u'原密码输入错误')
        return render_template('change_password.html')


