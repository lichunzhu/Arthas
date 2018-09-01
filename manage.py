# -*- coding:utf-8 -*-
# user    :chauncylee     
# time    :18-8-26 下午6:01
# filename:manager.py
# IDE     :PyCharm

import random

from flask_script import Manager
from arthus import app, db
from arthus.models import User, Image, Comment
from sqlalchemy import or_, and_

manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    # create
    for i in range(0, 100):
        db.session.add(User('User' + str(i + 1), 'a' + str(i)))
        for j in range(0, 3):
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('This is a comment' + str(k), 1 + 3 * i + j, i + 1))
    db.session.commit()

    # modify
    for i in range(50, 100, 2):
        user = User.query.get(i)
        user.username = '[New1]' + user.username
    User.query.filter_by(id=51).update({'username': 'New2'})
    db.session.commit()

    # delete
    for i in range(50, 100, 2):
        comment = Comment.query.get(i + 1)
        db.session.delete(comment)
    db.session.commit()

    # query
    print 1, User.query.all()
    print 2, User.query.get(3)
    print 3, User.query.filter_by(id=5).first()
    print 4, User.query.order_by(User.id.desc()).offset(1).limit(2).all()
    print 5, User.query.filter(User.username.endswith('0')).limit(3).all()
    print 6, User.query.filter(or_(User.id == 88, User.id == 99)).all()
    print 7, User.query.filter(and_(User.id > 88, User.id < 93)).all()
    print 8, User.query.filter(and_(User.id > 88, User.id < 93)).first_or_404()
    print 9, User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items
    user = User.query.get(1)
    print 10, user.images.all()
    image = Image.query.get(1)
    print 11, image.user


@manager.option('-n', '--name', dest='name', default='world')
def hello(name):
    """say hello world"""
    print 'hello %s' % name


if __name__ == '__main__':
    manager.run()

