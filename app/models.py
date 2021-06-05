from flask import current_app
from app import db, login
from flask_login import UserMixin
from datetime import datetime
import jwt


@login.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


# 定义数据库模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 主建
    username = db.Column(db.String(20), unique=True, nullable=False)  # 不可重复，非空
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 创建User表和Post表联系
    posts = db.relationship('Post', backref=db.backref('author'), lazy=True)    # lazy懒加载，不用就不加载

    def __repr__(self):
        return f'<User {self.username}>'

    # 定义找回密码加密函数
    def generate_reset_password_token(self):
        return jwt.encode({"id": self.id}, current_app.config['SECRET_KEY'], algorithm="HS256")

    # 定义找回密码解密函数
    @staticmethod  # 静态方法
    def check_reset_password_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])  # 对token进行解密
            return User.query.filter_by(id=data['id']).first()  # 根据解密出的值，返回指定用户数据
        except Exception as e:
            print(e)
            return


# 定义邮件数据库模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140),nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'文章:{self.body}'
