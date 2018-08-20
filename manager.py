from flask_script import Manager
from app import app

manager = Manager(app)


@manager.option('-n', '--name', dest='name', default='world')
def hello(name):
    """say hello world"""
    print 'hello %s' % name


if __name__ == '__main__':
    manager.run()

