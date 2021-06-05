from threading import Thread
from app import mail, app
from flask_mail import Message
from flask import current_app, render_template


def send_async_mail(app, msg):      # 真正去发送邮件
    try:
        with app.app_context():
            mail.send(msg)
    except Exception as e:
        print(e)
        return


def send_reset_password_mail(user, token):      # 配置发送邮件内容
    msg = Message("重置你的Flask App密码",
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email],
                  html=render_template('reset_password_mail.html', user=user, token=token))
    # mail.send(msg)     # 发送邮件
    Thread(target=send_async_mail, args=(app, msg,)).start()        # 让另一个线程来发送邮件
