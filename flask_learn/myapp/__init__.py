#-*- coding:utf-8 -*-

from flask import Flask 
from myapp.utils.util import get_user_id

app = Flask("myapp")
app.config.from_object('myapp.app_config')

app.jinja_env.globals.update(static='/static')
app.jinja_env.globals.update(get_user_id=get_user_id)

#from myapp.views.register import regist
import views
