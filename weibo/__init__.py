#!/usr/bin/python
#coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('settings')#配置文档
db = SQLAlchemy(app)#ORM对象
login_manager = LoginManager()#登录管理
login_manager.init_app(app)#登录管理初始化
login_manager.login_view = 'login'#登录模块

from weibo import views, models

