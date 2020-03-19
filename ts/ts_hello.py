# # -*- coding:utf-8 -*-
# """
# 最小化Flask
# """
# from flask import Flask
# # from flask import make_response
#
# app = Flask(__name__)
#
#
# # 视图函数（单函数无法继承，复用效果不好）
# # 注册路由1：路由装饰器
# # 重定向保证：唯一URL
# # 重定向：{'location'url:,'status code':301永久重定向/308永久重定向}
# # 308永久重定向之后 可以 清除浏览器记录
# # flask通过('/hello/')重定向兼容'/hello'和'/hello/'地址
# @app.route('/hello/')
# def hello():
#     # status code
#     # content-type = text/html
#     # headers = {
#     #     'content-type': 'text/plain',
#     #     'content-type': 'application/json',
#     #     'location': 'https://cn.bing.com/',
#     # }
#     # return '<html></html>', 301, headers
#     # response = make_response('<html></html>', 200)
#     # response.headers = headers
#     # return response
#     return 'hello'
#
#
# # 基于类的视图（即插视图）
# # 注册路由2：add注册路由
# # view_func指定注册路由的函数
# # app.add_url_rule('/hello/', view_func=hello, endpoint=)
#
# app.run()