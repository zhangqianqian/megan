# -*- coding:utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from myapp import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/user_db'
db = SQLAlchemy(app)

