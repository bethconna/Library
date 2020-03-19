#! -*- coding:utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from app import mail
from flask_mail import Message


# 异步发送email
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e


def send_mail(to, subject, template, **kw):
    # msg = Message('测试邮件', sender='', body='test', recipients=[''])
    msg = Message('[鱼书]' + '' + subject,
                  sender=current_app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.html = render_template(template, **kw)
    # mail.send(msg)

    # flask真实核心对象
    app = current_app._get_current_object()
    # 异步线程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

