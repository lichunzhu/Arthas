# -*- coding:utf-8 -*-
# user    :chauncylee     
# time    :18-8-26 下午6:01
# filename:manager.py
# IDE     :PyCharm

import random

from flask_script import Manager
from arthus import app, db
from arthus.models import User, Image, Comment

manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('User' + str(i), 'a' + str(i)))
        for j in range(0, 3):
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('This is a comment' + str(k), 1 + 3 * i + j, i + 1))
    db.session.commit()


@manager.option('-n', '--name', dest='name', default='world')
def hello(name):
    """say hello world"""
    print 'hello %s' % name


if __name__ == '__main__':
    manager.run()

