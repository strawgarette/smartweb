#!/usr/bin/python
#coding=utf-8

"""

参考文档：
https://pypi.python.org/pypi/Flask-SQLAlchemy
http://flask-sqlalchemy.pocoo.org/2.1/
http://www.pythondoc.com/flask-sqlalchemy/config.html

此文件重要定义数据库的结构

"""
import re
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, login_user, logout_user,\
    UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from weibo.constants import FriendEnum, PermsEnum, UserStatusEnum
from weibo import constants
from weibo import db


class User(UserMixin, db.Model):
    """ 用户 """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nickname = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    head_img = db.Column(db.String(200))

    status = db.Column(db.Enum(UserStatusEnum))
    is_valid = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime)
    updateed_at = db.Column(db.DateTime)
    loast_login = db.Column(db.DateTime, doc="最后登录时间")

    weibos = db.relationship('Weibo', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def set_password(self, password):
        """  设置用户的hash密码 """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ 验证用户的password """
        return check_password_hash(self.password, password)

    def get_weibo_count(self):
        """ 发送信息的条数 """
        return Weibo.query.filter_by(user=self).count()

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    """ 角色 """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    perms = db.Column(db.Enum(PermsEnum))

    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    updateed_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#这一句话非常重要

    def __repr__(self):
        return '<Role %r>' % self.name




class Weibo(db.Model):
    """ wb """
    __tablename__ = 'weibo'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(160), nullable=False)

    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#又是外键

    at_users = db.relationship('WeiboAtUser', backref='weibo')
    rel_topics = db.relationship('WeiboRelTopic', backref='weibo')
    comments = db.relationship('Comment', backref='weibo', lazy='dynamic')

    def get_comments_count(self):
        """ 获取评论次数 """
        return self.comments.count()

    def get_content(self):
        """ 替换@和话题 """
        content = self.content
        # 替换@
        def replace_at(match_obj):
            return '<a href="%s">%s</a>' % (
                url_for('user_detail', nickname=match_obj.group(1)),
                match_obj.group(0))
        content = re.sub(constants.AT_USER_PATTEN, replace_at, content)
        # 替换话题
        def replace_topic(match_obj):
            return '<a href="%s">%s</a>' % (
                url_for('topic_detail', name=match_obj.group(1)),
                match_obj.group(0))
        content = re.sub(constants.TOPIC_PATTEN, replace_topic, content)
        return content

    def __repr__(self):
        return '<Weibo %r>' % self.content


# weibo_topic = db.Table('weibo_topic',
#     db.Column('weibo_id', db.Integer, db.ForeignKey('weibo.id')),
#     db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'))
# )


class Topic(db.Model):
    """ 话题 """
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), unique=True, nullable=False)
    desc = db.Column(db.String(160))
    head_img = db.Column(db.String(200))

    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)

    rel_weibos = db.relationship('WeiboRelTopic', backref='topic')

    # weibos = db.relationship('Weibo', secondary=weibo_topic,
    #     backref=db.backref('weibos', lazy='dynamic'))

    def __repr__(self):
        return '<Topic %r>' % self.name


class WeiboAtUser(db.Model):
    """ wb@用户 """
    __tablename__ = 'weibo_at_user'
    id = db.Column(db.Integer, primary_key=True)
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibo.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class WeiboRelTopic(db.Model):
    """ wb讨论话题 """
    __tablename__ = 'weibo_rel_topic'
    id = db.Column(db.Integer, primary_key=True)
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibo.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))


class Comment(db.Model):
    """ 评论 """
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(160), nullable=False)

    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)

    weibo_id = db.Column(db.Integer, db.ForeignKey('weibo.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Weibo %r>' % self.name


class Friend(db.Model):
    """ 好友/关注 """
    __tablename__ = 'friend'
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum(FriendEnum))
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Friend %r>' % self.id




class FACE(db.Model):
    """ 新闻评论 """
    __tablename__ = 'FACE'
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer)
    user_name = db.Column(db.String(200), nullable=False)
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    

    def __repr__(self):
        return '<News %r>' % self.content
