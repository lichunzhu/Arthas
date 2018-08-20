# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, redirect, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = 'newcoder'


@app.route('/')
@app.route('/index/')
def index():
    res = ''
    for msg in get_flashed_messages():
        res = res + msg + '<br>'
    res += 'hello'
    return res


@app.route('/profile/<int:uid>/', methods=['GET', 'POST'])
def profile(uid):
    colors = ('red', 'green', 'black')
    return render_template('profile.html', uid=uid, colors=colors)


@app.route('/request')
def request_demo():
    res = request.args.get('key', 'defaultKey') + '<br>'
    for property in dir(request):
        res = res + str(property) + '|==|<br>' + str(eval('request.' + property)) + '<br>'
    return res


@app.route('/newpath')
def newpath_demo():
    return "new path"


@app.route('/re/<int:code>')
def redirect_demo(code):
    return redirect('/newpath', code=code)


@app.errorhandler(404)
def page_not_found(error):
    print error
    return render_template('not_found.html', url=request.url), 404


@app.route('/login')
def login():
    flash('登陆成功')
    return 'ok'
    # return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run()
