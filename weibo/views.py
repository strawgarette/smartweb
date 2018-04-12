#!/usr/bin/python
#coding=utf-8

"""
view 层
"""


import random
import string

from flask import Flask, request, Response
import jsonpickle
import numpy as np




from weibo.mysql import MoonMysql
from flask import jsonify


import json,requests
from datetime import datetime
from flask import render_template, redirect, flash, url_for, request, abort
from flask_login import login_required, login_user, logout_user,\
    UserMixin, current_user


from weibo.forms import LoginForm, RegistForm, WeiboForm, WeiboCommentForm,control_form,DateForm
from weibo import login_manager, db, app
from weibo.models import User, Weibo, Topic, WeiboRelTopic, Comment, Role, FACE
from weibo.decorators import staff_perms_required
from weibo import constants




@login_manager.user_loader
def load_user(user_id):
    """ 登录回调"""
    return User.query.get(user_id)

'''
@app.route('/', methods=['GET', 'POST'])
@app.route('/page/<int:page>/')
def index(page=None):
    """ 主页 """
    form = WeiboForm()
    print(form)
    if form.validate_on_submit():
        # 判断用户是否已经登录
        if current_user.is_authenticated:
            # 保存微博
            form.publish(user=current_user)
            # 提示消息
            flash("发布成功！")
            # 跳转到首页
            return redirect(url_for('index'))
        else:
            flash('请先登录')
            return redirect(url_for('login'))
    if page is None:
        page = 1
    page_data = Weibo.query.filter_by(is_valid=1)\
        .order_by   (Weibo.created_at.desc())\
        .paginate(page=page, per_page=10)
    print(page_data)
    return render_template('home/index.html',
        form=form,
        page_data=page_data)
'''

@app.route('/', methods=['post','get'])
@app.route('/page/<int:page>/')
def index(page=None):
    #print(1)

    return render_template('watermelon/watermelon.html')


@app.route('/user/login/', methods=['GET', 'POST'])
def login():
    """ 登录 """
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=data['username']).first()
        # 判断用户名是否存在
        flash('用户不存在')
        if user is None:
            return redirect(url_for('login'))
        # 判断密码是否正确
        if not user.check_password(data['password']):
            flash('密码不正确')
            return redirect(url_for('login'))
        # 登录用户
        login_user(user)
        # 保存用户的最后登录时间
        user.loast_login = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("欢迎您: %s" % user.nickname)
        next_url = request.args.get('next')
        return redirect(next_url or url_for('index'))
    return render_template("user/login.html", form=form)


@app.route('/user/logout/', methods=['GET', 'POST'])
def logout():
    """ 退出登录 """
    logout_user()
    flash("感谢您的访问")
    return redirect(url_for('index'))


@app.route('/user/regist/', methods=['GET', 'POST'])
def regist():
    """ 注册 """
    form = RegistForm()
    if form.validate_on_submit():
        user = form.regist()
        # 登录用户
        login_user(user)
        # 消息提示
        flash('注册成功')
        # 跳转到首页
        return redirect(url_for('index'))
    return render_template('user/regist.html', form=form)


@app.route('/user/profile/')
#@login_required
def profile():
    """ 个人用户详细信息 """
    #个人打卡信息
    print(current_user)
    return render_template('user/profile.html')


@app.route('/user/<nickname>/')
@app.route('/user/<nickname>/page/<int:page>/')
def user_detail(nickname, page=None):
    """ 根据用户的昵称查看用户的信息 """
    user = User.query.filter_by(nickname=nickname).first_or_404()
    # 该用户的所有微博
    # 方式一
    # page_data = Weibo.query.filter_by(
    #     user=user, is_valid=1
    #     ).order_by(Weibo.created_at.desc())\
    #     .paginate(page=page, per_page=10)

    # 方式二
    # 模型中需要添加 lazy='dynamic'
    page_data = user.weibos.filter(
        Weibo.is_valid==1
        ).order_by(Weibo.created_at.desc())\
        .paginate(page=page, per_page=10)
    return render_template('home/user.html',
        user=user,
        page_data=page_data)


@app.route('/topic/detail/<name>/')
@app.route('/topic/detail/<name>/page/<int:page>/')
def topic_detail(name, page=None):
    """ 根据话题名称查看详情 """
    form = WeiboForm(data={'content': "#%s#" % name})
    if page is None:
        page = 1
    topic = Topic.query.filter_by(name=name).first_or_404()
    page_data = Weibo.query.join(WeiboRelTopic).filter(
            WeiboRelTopic.topic_id==Topic.id,
            Weibo.is_valid==1,
            Topic.id==topic.id
        ).order_by(Weibo.created_at.desc())\
        .paginate(page=page, per_page=10)
    return render_template('home/topic_detail.html',
        topic=topic,
        page_data=page_data,
        form=form)


@app.route('/weibo/comment/<int:pk>/', methods=['GET', 'POST'])
def weibo_comment(pk):
    """ 微博评论 """
    form = WeiboCommentForm()
    weibo = Weibo.query.filter_by(id=pk).first()
    if weibo is None:
        return '404'
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # 执行评论操作
            form.add_comment(weibo, current_user)
        else:
            return '401'
    # 取前条评论数据
    comment_list = Comment.query.filter_by(weibo_id=weibo.id, is_valid=1).limit(5)
    return render_template('moudule/weibo_comments.html',
        form=form,
        weibo=weibo,
        comment_list=comment_list)


@app.route('/user/friend/nickname/', methods=['GET', 'POST'])
def user_friend(nickname):
    """ 微博关注 """
    # 查找用户
    to_user = User.query.filter_by(nickname=nickname).first()
    if to_user is None:
        return '404'
    if not current_user.is_authenticated:
        return '401'
    # 查找是否已经关注
    rel = Friend.query.filter_by(from_user_id=current_user.id, to_user_id=to_user.id).first()
    if rel is not None:
        return '402'   # 已经关注
    rel_obj = Friend(
        from_user_id=current_user.id,
        to_user_id=to_user.id,
        created_at=datetime.now()
    )
    db.session.add(rel_obj)
    db.session.commit()
    return '201'



@app.route('/admin/')
#@login_required
# #@staff_perms_required
def admin_index():
    """ 后台管理首页 """
    return render_template('admin/index.html',
        menu_no='index')



@app.route('/admin/user/')
@app.route('/admin/user/page/<int:page>/')
#@login_required
#@staff_perms_required
def admin_users(page=None):
    """ 用户管理 """
    if page is None:
        page = 1
    page_data = User.query.filter_by(is_valid=1).paginate(
        page=page, per_page=10)
    return render_template('admin/users.html',
        page_data=page_data,
        menu_no='users')


@app.route('/admin/user/manage/<int:pk>/<int:status>/', methods=['POST'])
def admin_manage_user(pk, status):
    user = User.query.filter_by(id=pk, is_valid=1).first()
    if user is None:
        return '404'
    if not current_user.is_authenticated:
        return '401'

    # 设置用户的状态
    if int(status) == 1:
        user.status = constants.UserStatusEnum.NORMAL
    else :
        user.status = constants.UserStatusEnum.LIMIT
    db.session.add(user)
    db.session.commit()
    return '201'


@app.route('/admin/user/roles/<int:pk>/', methods=['GET', 'POST'])
#@login_required
def admin_user_role(pk):
    """ 管理用户的角色 """
    user = User.query.filter_by(id=pk, is_valid=1).first_or_404()
    perms = constants.PermsEnum
    roles = Role.query.filter_by(user_id=user.id, is_valid=1)
    # 已经存在的角色
    has_roles = list(map(lambda n: n.perms.name, roles))
    if request.method == 'POST':
        # 删除所有的角色
        roles.delete()
        # for item in roles:
        #     item.is_valid = 0
        #     db.session.add(item)
        for name in request.form.getlist('perms'):
            enum_perm = getattr(constants.PermsEnum, name, None)
            role_obj = Role(
                user_id=user.id,
                perms=enum_perm,
                name=enum_perm.name,
                )
            db.session.add(role_obj)
        db.session.commit()
        flash('编辑成功')
        return redirect(url_for('admin_user_role', pk=pk))
    return render_template('admin/user_role.html',
        user=user,
        perms=perms,
        has_roles=has_roles,
        menu_no='users')


@app.route('/admin/weibo/')
@app.route('/admin/weibo/page/<int:page>/')
#@login_required
#@staff_perms_required
def admin_weibos(page=None):
    """ 微博管理 """
    if page is None:
        page = 1
    page_data = Weibo.query.filter_by(is_valid=1).paginate(
        page=page, per_page=3)
    return render_template('admin/weibos.html',
        page_data=page_data,
        menu_no='weibos')


@app.route('/admin/weibo/<int:pk>', methods=['POST'])
#@login_required
#@staff_perms_required
def admin_weibo_manage(pk):
    """ 管理微博 """
    weibo = Weibo.query.filter_by(id=pk, is_valid=1).first()
    if weibo is None:
        return '404'
    weibo.is_valid = 0
    db.session.add(weibo)
    db.session.commit()
    return '201'





@app.route('/admin/face_record/')
@app.route('/admin/face_record/page/<int:page>/')
#@login_required
#@staff_perms_required
def face_record(page=None):
    """ 微博管理 """
    if page is None:
        page = 1
    page_data = FACE.query.paginate(page=page, per_page=3)
    return render_template('admin/face_record.html',
        page_data=page_data,
        menu_no='face_record')
    
    # page_data = Weibo.query.filter_by(is_valid=1).paginate(
    #     page=page, per_page=3)    
        
    # return render_template('admin/face_record.html',
    #     page_data=page_data,
    #     menu_no='weibos')





@app.route('/control/', methods=['GET', 'POST'])
#@login_required
#@staff_perms_required
def control():
    #希望之后可以在网页端添加所要发送的机器人怎么办呢？
    form = control_form()
    #if form.validate_on_submit():#检测是不是POST请求
    #if True:
    if request.method == 'POST':
        
        print(form.language.data)

        app_write = MoonMysql
        app_write.update_control_data(NAME_DATA='DOOR1',STATUS_DATA=form.language.data)
    return render_template("control.html", form=form)


@app.route('/control_new/')
def control_new():
    return render_template("control_new.html")


@app.route('/test/<data>')
def test(data):
    data=data
    return render_template("test.html",data=data)



@app.route('/smart/',methods=['GET', 'POST'])
def smart():
    #print(time)

    return render_template("smart.html")



@app.route('/sendAjax2', methods=['POST'])
def sendAjax2():
    # password = request.form.get('password')
    # username = request.args.get('username')
 
    data = json.loads(requests.get('data'))
    a = request.form
    print(a)



    username = data['username']
    password = data['username']
    print (username)
    print (password)
    return 4535





@app.route('/dateform', methods=['post','get'])
def home():
    #print(1)
    form = DateForm()
    if form.validate_on_submit():
        #print(1)
        print(form.dt.data)
        #return form.dt.data.strftime('%x')
        print(form.dt_1.data)
    return render_template('vort.html', form=form)






@app.route('/mydict', methods=['GET', 'POST'])
def mydict():
    print('post')
    if request.method == 'POST':
        a = request.form['mydata']
        a = request.form['youdata']
        a=request.form
        print(a)
    d = {'name': 'xmr', 'age': 18}
    return jsonify(d)   





"所有前端到后端的控制数据全部走下面这个路由"

@app.route('/control_data', methods=['GET', 'POST'])
def control_data():
    #print('post')
    if request.method == 'POST':
        NAME = request.form['NAME']
        print(NAME)
        STATUS = request.form['STATUS']
        print(STATUS)

        #app_write = MoonMysql
        #app_write.update_control_data(NAME_DATA=NAME,STATUS_DATA=STATUS)
      #  app_write.update_control_data(NAME_DATA='CHANGE',STATUS_DATA=NAME)        
    d = {'name': 'xmr', 'age': 18}
    return jsonify(d)   






@app.route('/homepage', methods=['post','get'])
def home_page():
    #print(1)

    return render_template('watermelon/watermelon.html')



@app.route('/strawberry', methods=['post','get'])
#@login_required
#@staff_perms_required
def strawberry():
    #print(1)

    return render_template('strawberry.html')

@app.route('/helicopter', methods=['post','get'])
#@login_required
#@staff_perms_required
def helicopter():
    #print(1)

    return render_template('helicopter.html')





@app.route('/door_system', methods=['post','get'])
#@login_required
#@staff_perms_required
def door_system():
    #print(1)
    app=MoonMysql
    result=app.get_control_status(NAME_DATA='DOOR1')
    results=result[0]
    rand_num=random.randint(1,10000)+random.randint(1,1000)+random.randint(1,1000000)
    rand_str=str(rand_num)
    link='http://lab120.moonstarwisdow.com/static/img/camera/now.jpg?'+rand_str+results['STATUS']
    print(link)
    return render_template('door_system.html',link=link)

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def image_rec():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("./weibo/static/img/camera/now.jpg",img)
    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")




@app.route('/camera/')
#@login_required
#@staff_perms_required
def camera():
    """ 后台管理首页 """
    return render_template('camera.html')