#!/usr/bin/python
#coding=utf-8

"""
模板变量
"""

from flask import Flask, render_template

from forms import LoginForm

app = Flask(__name__)


@app.route('/')
def login():
    """ 访问首页 """
    form = LoginForm()
    return render_template("index2.html", form=form)


app.config['SECRET_KEY'] = 'a random string'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True) 