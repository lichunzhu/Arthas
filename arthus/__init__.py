# -*- coding:utf-8 -*-
# user    :chauncylee     
# time    :18-8-26 下午6:00
# filename:__init__.py
# IDE     :PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('app.conf')
db = SQLAlchemy(app)

from arthus import views, models
