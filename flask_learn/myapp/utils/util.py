#-*- coding:utf-8 -*-
from flask import session
def get_user_id():
    if session.has_key("user_id"):
        return session["user_id"]
    else:
        return 0
