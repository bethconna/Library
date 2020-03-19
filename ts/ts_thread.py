#! -*- coding:utf-8 -*-
# 多线程
# 异步编程
import threading
import time


def func():
    t = threading.current_thread()
    time.sleep(3)
    print('threading1：'+t.getName())


# func()
new_t1 = threading.Thread(target=func, name='new_thread')
new_t1.start()

t = threading.current_thread()
print('threading2：'+t.getName())

#--------------------------------------------------------
# GIL：全局解释器锁 global interpreter lock
# IO密集型程序：数据库查询、请求网络资源、读写文件
# CPU密集型程序：大量计算程序

# 线程隔离：每个线程的唯一标识
# 数据操作：werkzeug库 local模块 Local对象 字典

from werkzeug.local import Local


class A(object):
    a = 1


# obj = A()
obj = Local()
obj.a = 1


def worker():
    # time.sleep(3)
    obj.a = 2
    print('threading3：'+str(obj.a))


new_t2 = threading.Thread(target=worker, name='new_thread')
new_t2.start()
time.sleep(3)
print('threading4：'+str(obj.a))
