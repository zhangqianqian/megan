from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/user_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)
    code = db.Column(db.String(100))
    
    def __init__(self, username, password, code):
        self.username = username
        self.password = password
        self.code = code

    def __repr__(self):
        return '<User %r>' % self.username

#db.create_all()
'''
admin = User("shq","123","assdfasdfasdfs")
db.session.add(admin)
db.session.commit()
'''

#users=User.query.all()
#print users

class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String(80), unique=True)
    addr = db.Column(db.String(120), unique=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    userquery = db.relationship('User', backref=db.backref('uq',lazy='dynamic'))
    
    def __init__(self, phone_num, addr, userid):
        self.phone_num = phone_num
        self.addr = addr
        self.userid = userid

    def __repr__(self):
        return '<User_info %r>' % self.phone_num


#db.create_all()
uq = Userinfo(1)
db.session.add(uq)
db.session.commit()
uq.userquery()
'''
admininfo = Userinfo("12345","beijing","1")
db.session.add(admininfo)
db.session.commit()
'''
