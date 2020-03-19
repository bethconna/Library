from flask import render_template, redirect
from flask_login import login_required
from app.models.gift import Gift
from app.view_models.book import BookViewModel
from app.web.blueprint import web


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
@login_required
def personal_center():
    return '个人空间'


# # 判断USER积分是否可以获取static静态文件
# @web.route('/download')
# def download():
#     if user:
#         send_static_file()
