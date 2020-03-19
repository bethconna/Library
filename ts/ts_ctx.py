#! -*- coding:utf-8 -*-

# 应用上下文 对象 Flask
# 请求上下文 对象 Request

from flask import Flask, current_app

app = Flask(__name__)

# AppContext封装 app 入栈   （current_app栈顶）
# RequestContext封装 Request 入栈 （request栈顶）

# Request在flask请求时入栈，会判定app栈是否为空，若为空则flask自动app入栈

ctx = app.app_context()
ctx.push()

a = current_app

# 请求结束 出栈
ctx.pop()

# with语句
# 对实现上下文协议的对象（上下文管理器：__enter__ __exit__）使用with：对push pop的封装
# 对with语句返回上下文管理器
with app.app_context():
    # f是__enter__函数的返回值
    a = current_app


class A(object):

    def __enter__(self):
        a = 1
        return a

    def __exit__(self, exc_type, exc_val, exc_tb):
        a = 2


with A() as obj_A:
    print(obj_A)


class MyResource(object):

    def __enter__(self):
        print('connect to resource')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('process exception')
        else:
            print('no exception')
        print('close resource connection')
        # 默认False：外部抛出异常
        # True：内部处理异常，外部不抛出异常
        return True

    def query(self):
        print('query data')


with MyResource() as resource:
    resource.query()


# 装饰器实现上下文管理器
class MyResource2(object):

    def query(self):
        print('query data')


from contextlib import contextmanager


@contextmanager
def make_resource():
    print('connect to resource')
    yield MyResource2()  # return MyResource2()
    print('close resource connection')


with make_resource() as r:
    r.query()
