# -*- coding:utf-8 -*-
# user    :chauncylee     
# time    :18-8-26 下午6:00
# filename:__init__.py
# IDE     :PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
app.secret_key = 'nowcoder'         # for flash
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = '/regloginpage/'

from arthas import views, models
