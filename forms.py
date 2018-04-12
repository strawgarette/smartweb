#!/usr/bin/python
#coding=utf-8



from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class LoginForm(FlaskForm):
    """ 登录表单 """
    username = StringField(label='用户名', validators=[DataRequired("请输入用户名")],
        description="请输入用户名",
        render_kw={"required": "required", "class": "form-controal"})
    password = PasswordField(label='密码', validators=[DataRequired("请输入密码")],
        description="请输入密码",
        render_kw={"required": "required", "class": "form-controal"})
    submit = SubmitField('登录', render_kw={
            'class': 'btn btn-info'
        })

    def check_user(self):
        """ 检测用户 """
        from weibo import User
        data = self.data
        user = User.query.filter_by(username=data['username']).first()
        return user


class RegistForm(FlaskForm):
    """ 用户注册 """
    def __init__(self, db, *args, **kwargs):
        super(RegistForm, self).__init__(*args, **kwargs)
        self.db = db

    username = StringField(label="用户名", validators=[DataRequired()],
        render_kw={"required": 'required', "placeholder": "请输入用户名"},
        description="输入用用户邮箱注册")

    nickname = StringField(label="昵称", validators=[DataRequired()],
        render_kw={"required": 'required', "placeholder": "请输入昵称"},
        description="输入用户昵称")
    password = PasswordField('密码', validators=[DataRequired("请输入密码")])
    submit = SubmitField('注册', render_kw={
            'class': 'btn btn-info'
        })

    def validate_password(self, field):
        password = field.data
        if len(password) != 6:
            raise ValidationError("密码必须是6位")
        return password

    def validate_username(self, field):
        from weibo import User
        username = field.data.lower()
        # 判断改用户名是否已经存在
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise ValidationError("该用户已经注册")
        return username

    def validate_nickname(self, field):
        from weibo import User
        nickname = field.data.strip()
        # 判断改用户名是否已经存在
        exists_user = User.query.filter_by(nickname=nickname).count()
        if exists_user > 0:
            raise ValidationError("该用户昵称注册")
        return nickname

    def regist(self):
        """ 注册用户 """
        from weibo import User
        data = self.data
        user = User(
            username=data['username'],
            password=data['password'],
            nickname=data['nickname'],
            )
        self.db.session.add(user)
        self.db.session.commit()
        # 保存用户数据
        # 返回用户
        return user