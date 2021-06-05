from flask import render_template, flash, request, redirect, url_for
from app import app, bcrypt, db
from flask_login import login_user, login_required, current_user, logout_user

from app.forms import RegisterForm, LoginForm, PasswordResetRequestForm, ResetPasswordForm, PostTweetForm
from app.models import User, Post
from app.email import send_reset_password_mail


@app.route('/', methods=['GET', 'POST'])
@login_required  # 重定向到登录页面
def index():
    form = PostTweetForm()  # 创建文章表单实例
    if form.validate_on_submit():  # 判断表单是否填写完整
        text = form.text.data  # 获取表单中文本框填写的内容
        post = Post(body=text)  # 创建一个post对象
        print(current_user)
        print(current_user.posts)
        current_user.posts.append(post)  # 将当前登录的用户的数据库中的posts写入body的内容
        db.session.commit()  # 数据库提交更改
        flash('发表成功！', category='info')  # 文章发表成功提示信息
    return render_template('index.html', form=form)


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # 判断用户登录状态
        return redirect(url_for('index'))  # 重定向到index主页
    form = RegisterForm()  # 创建表单对象
    if request.method == 'POST':  # 判断请求是否POST
        if form.validate_on_submit():  # 是否通过表单验证
            username = form.username.data  # 获取表单中的username
            email = form.email.data  # 获取表单中的email
            password = bcrypt.generate_password_hash(form.password.data)  # 获取表单中的password并加密
            user = User(username=username, email=email, password=password)  # 创建User类对象
            db.session.add(user)  # 将获取的数据添加到数据库
            db.session.commit()  # 将添加的数据提交
            flash('注册成功！', category='success')  # 提示注册成功
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


# 登录功能 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # 判断用户登录状态
        return redirect(url_for('index'))  # 重定向到index
    form = LoginForm()  # 创建实例
    if form.validate_on_submit():  # 判断是否通过表单验证
        username = form.username.data  # 获取表单填写的数据
        password = form.password.data
        remember = form.remember.data
        print(remember)
        # 用户名和密码是否能和数据库中的数据匹配上
        user = User.query.filter_by(username=username).first()  # 查询登录的用户名是否存在
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash("登录成功！", category='success')
            if request.args.get('next'):
                next_args = request.args.get('next')
                return redirect(next_args)
            return redirect(url_for('index'))
        flash('用户名或密码错误！', category='info')
    return render_template('login.html', form=form)


# 退出登录
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    # 判断用户是否成功登录，若登录就不会来到找回密码的页面，即使通过网址输入方式，也直接跳转到主页
    if current_user.is_authenticated:  # 判断用户登录状态
        return redirect(url_for('index'))  # 重定向到index主页
    form = PasswordResetRequestForm()  # 创建表单实例
    if form.validate_on_submit():  # 若表单填写正确
        email = form.email.data  # 获取表单中填写的email
        user = User.query.filter_by(email=email).first()  # 获取email对应的用户在数据库中的数据
        token = user.generate_reset_password_token()  # 生成token
        send_reset_password_mail(user, token)  # 进行发邮件的操作
        flash('密码重置请求邮件已发送，请检查您的邮箱', category='info')
    return render_template('send_password_reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:  # 判断用户登录状态
        return redirect(url_for('index'))  # 重定向到index主页
    form = ResetPasswordForm()  # 创建重置密码实例
    if form.validate_on_submit():  # 判断表单是否填写完整
        user = User.check_reset_password_token(token)  # 解密token返回用户数据
        if user:  # 判断根据token解密出来的用户是否存在
            user.password = bcrypt.generate_password_hash(form.password.data)  # 更改用户的密码，将用户填写的密码加密
            db.session.commit()  # 密码发重置后提交到数据库，这样数据库中的内容才会真正发生改变
            flash('密码已重置，您现在可以用您的新密码重新登录了！', category='info')
            return redirect(url_for('login'))
        else:
            flash('用户不存在', category='info')  # 当用户不存在，提示用户不存在
            return redirect(url_for('login'))  # 返回到login页面

    return render_template('reset_password.html', form=form)
