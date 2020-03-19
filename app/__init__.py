# -*- coding:utf-8 -*-
from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()


def create_app():
    # app：flask全局只有一个
    # flask静态文件夹：默认static_folder = 'statics'
    app = Flask(__name__)

    # 导入配置文件
    # from_object导入的配置文件要求：大写字母
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 注册蓝图
    register_blueprint(app)

    # LoginManager初始化
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请登录或注册'

    # 注册Mail
    mail.init_app(app)

    # 数据库初始化
    db.init_app(app)
    # 手动将app推入栈中：current.app
    with app.app_context():
        db.create_all()

    return app


def register_blueprint(app):
    from app.web.blueprint import web
    app.register_blueprint(web)
