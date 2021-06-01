import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is secret-key'
    RECAPTCHA_PUBLIC_KEY = '6LdGIf4aAAAAACjWJ5B251jD8mUtiZWk7czxhfFG'
    RECAPTCHA_PRIVATE_KEY = '6LdGIf4aAAAAADaB4ZyzHNbjcuirI1YslxY50yxe'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
