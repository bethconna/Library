# -*- coding:utf-8 -*-
import json
from flask import jsonify, request, render_template, flash
from flask_login import current_user
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.book import Book
from app.libs.helper import is_isbn_or_key
from app.view_models.book import BookViewModel, BooksViewModel
from app.view_models.trade import TradeInfo
from app.web.blueprint import web
from app.forms.view import SearchForm


# 视图函数里面的代码要简洁易读
# 加<>识别为参数
# API
# @web.route('/book/search/<q>')
# def search(q):
#     """
#         q : 普通关键字 ISBN关键字
#     """
#     isbn_or_key = is_isbn_or_key(q)
#     if isbn_or_key == 'isbn':
#         res = Book.search_by_isbn(q)
#     else:
#         res = Book.search_by_keyword(q)
#     # jsonify代替response封装
#     return jsonify(res)


@web.route('/book/search')
def search():
    """
        q : 普通关键字 ISBN关键字
        page : 页码
        /search?q=&page=
    """
    # flask的request代理模式
    # flask视图函数中的request才是request对象，否则可能成为本地代理格式
    # q = request.args['q']
    # page = request.args['page']
    # to_dict()不可变字典转变成为可变字典
    # a = request.args.to_dict()

    # 验证层：参数校验
    form = SearchForm(request.args)
    books = BooksViewModel()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = Book()
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            # res = Book.search_by_isbn(q)
            # res = BookViewModel.package_single(res, q)
        else:
            yushu_book.search_by_keyword(q, page)
            # res = Book.search_by_keyword(q, page)
            # res = BookViewModel.package_collection(res, q)
        books.fill(yushu_book, q)

        # 代码解释权反转：default调用内置函数使json序列化
        # 类似的：dumps sorted filter
        # return json.dumps(books, default=lambda obj: obj.__dict__, ensure_ascii=False)

        # jsonify代替response封装
        # return jsonify(books)

    else:
        # return jsonify(form.errors)
        flash('搜索的关键字不符合要求，请重新输入关键字')

    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 书籍详情
    yushu_book = Book()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(isbn=isbn, uid=current_user.id, launched=False).first():
            has_in_gifts = True
        elif Wish.query.filter_by(isbn=isbn, uid=current_user.id, launched=False).first():
            has_in_wishes = True

    # wishes
    trade_wished = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_wished_model = TradeInfo(trade_wished)
    # gifts
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book, wishes=trade_wished_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
