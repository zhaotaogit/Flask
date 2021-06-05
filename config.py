import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 定义数据库配置
class Config(object):
    # SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is secret-key'
    # RECAPTCHA_PUBLIC_KEY
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or '6LdGIf4aAAAAACjWJ5B251jD8mUtiZWk7czxhfFG'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or '6LdGIf4aAAAAADaB4ZyzHNbjcuirI1YslxY50yxe'
    # DATABASE_CONFIGURATION
    SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # FLASK_GMAIL
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True,
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
