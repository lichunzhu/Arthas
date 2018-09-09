# -*- coding:utf-8 -*-
# user    :chauncylee     
# time    :18-8-26 下午5:59
# filename:views.py
# IDE     :PyCharm

from arthus import app, db
from flask import render_template, redirect, request, flash, get_flashed_messages
from models import User, Image
from flask_login import login_user, logout_user, current_user, login_required
import random
import hashlib
import json


@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10)
    return render_template('index.html', images=images)


@app.route("/image/<int:image_id>/")
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route("/profile/<int:user_id>/")
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3, error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


# 不够restful, 后续要改成get形式
@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id': image.id, 'url': image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)


@app.route("/regloginpage/")
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter='reglogin'):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.values.get('next'))


def redirect_with_msg(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/login/', methods={'post', 'get'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    print username, password
    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名和密码不能为空', 'reglogin')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect_with_msg('/regloginpage/', u'用户名不存在', 'reglogin')

    m = hashlib.md5()
    m.update(password + user.salt)
    if m.hexdigest() != user.password:
        return redirect_with_msg('/regloginpage/', u'密码错误', 'reglogin')

    login_user(user)

    next_page = request.values.get('next')  # 在存在next_page的时候直接引向next page
    print(next_page)
    if next_page is not None and next_page.startswith('/'):  # 检查next_page字段是否合法
        return redirect(next_page)

    return redirect('/')                   # 其余情况跳转到首页


@app.route("/reg/", methods={'post', 'get'})
def reg():
    # request.args
    # request.form
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名和密码不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return redirect_with_msg('/regloginpage/', u'用户名已存在', 'reglogin')

    # 更多的条件判断

    salt = '.'.join(random.sample('01234567890abcdefgABCDEFG', 10))  # 密码加盐, 增加破解难度
    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)

    next_page = request.values.get('next')
    print(next_page)
    if next_page is not None and next_page.startswith('/'):
        return redirect(next_page)

    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')
