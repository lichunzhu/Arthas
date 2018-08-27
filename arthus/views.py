# -*- coding:utf-8 -*-
# user    :chauncylee     
# time    :18-8-26 下午5:59
# filename:views.py
# IDE     :PyCharm

from arthus import app


@app.route('/')
def index():
    return 'Hello'
