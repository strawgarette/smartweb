    # -*- coding: utf-8 -*-

#!/usr/bin/python
#coding=utf-8

from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# 设置邮箱的配置信息
app.config['MAIL_USERNAME'] = 'moonstarcompany@163.com'
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PASSWORD']  = 'moonstar1234'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True

# 初始化邮箱实例
mail = Mail(app)

class mail():
    def mail_send():
        # 邮件消息对象
        msg = Message(
            "成功设置 @004 - mail | 邮件",
            body="之后把所有的邮件全部弄到这个inbox体系中",
            sender="moonstarcompany@163.com",
            recipients=["hu983267850.e705329@m.yinxiang.com"]
        )
        # 发送邮件
        #return('sending')True
        mail.send(msg)
        return "Send Success!"

@app.route("/wechat")
def wechat():
    return "请扫描二维码，登陆微信"


@app.route("/")
def index():
    return "欢迎来到《基于云网络的学科竞赛日常交互系统》"
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)