# -*- coding:utf-8 -*-
# user    :chauncylee     
# time    :18-8-26 下午6:01
# filename:manager.py
# IDE     :PyCharm

from flask_script import Manager
from arthus import app

manager = Manager(app)


@manager.option('-n', '--name', dest='name', default='world')
def hello(name):
    """say hello world"""
    print 'hello %s' % name


if __name__ == '__main__':
    manager.run()

