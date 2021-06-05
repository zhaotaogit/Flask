from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User


# 定义注册页面表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20)])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    # re = RecaptchaField()     # 注册验证码
    submit = SubmitField('注册')

    # 当用户名已存在时提示错误
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('此用户名已存在！')

    # 当邮箱已存在时提示错误
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('此邮箱已存在！')


# 定义登录页面表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('记住密码')
    submit = SubmitField('登录')


# 定义找回密码页面表单
class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('确定')

    # 当邮箱不存在时提示错误
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('此邮箱不存在！')


# 重置密码表单
class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20)])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('重置密码')


# 文章表单
class PostTweetForm(FlaskForm):
    text = TextAreaField('写点什么吧...', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('提交')
