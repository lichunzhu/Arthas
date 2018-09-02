# -*- coding:utf-8 -*-
# user    :chauncylee     
# time    :18-8-26 下午5:59
# filename:views.py
# IDE     :PyCharm

from arthus import app
from flask import render_template, redirect
from models import User, Image


@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10)
    return render_template('index.html', images=images)


@app.route("/image/<int:image_id>")
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route("/profile/<int:user_id>")
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    return render_template('profile.html', user=user)
