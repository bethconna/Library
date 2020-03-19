# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

# 蓝图 blueprint
# blueprint静态文件夹：默认static_folder = 'statics'
web = Blueprint('web', __name__)


# 蓝图自带的监听装饰器（flask.app也有同样的监听装饰器）
@web.app_errorhandler(404)
def not_found():
    # AOP：面向切片编程（集中编程）
    return render_template('404.html')
