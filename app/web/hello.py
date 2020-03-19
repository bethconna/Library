# -*- coding:utf-8 -*-
from flask import jsonify, render_template, flash

from app.web.blueprint import web


@web.route('/hello/')
def hello():
    return 'hello'


# # html模板+data渲染
# @web.route('/ts_model/')
# def test_model():
#     r = {
#         'user': 'beth',
#         'age': 18,
#         'grade': 13,
#         'signature': 'i love ai'
#     }
#     flash('hello beth', category='public')
#     flash('hello hennes', category='secret')
#     return render_template('test.html', data=r)






