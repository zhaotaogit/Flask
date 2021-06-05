from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from config import Config


app = Flask(__name__)   # 配置Flask实例
app.config.from_object(Config)      # 引用数据库config

bootstrap = Bootstrap(app)      # 配置Bootstrap实例
db = SQLAlchemy(app)        # 配置SQLAlchemy实例
bcrypt = Bcrypt(app)    # 配置Bcrypt实例
login = LoginManager(app)      # 配置LoginManager实例
mail = Mail(app)        # 配置Mail实例

login.login_view = 'login'      # 视图名称
login.login_message = '你必须登录才能进入此页面！'       # 设置提示信息
login.login_message_category = 'info'       # 设置消息分类


from app.routes import *