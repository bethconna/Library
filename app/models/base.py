#! -*- coding:utf-8 -*-
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLALchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer
from contextlib import contextmanager


class SQLALchemy(_SQLALchemy):

    @contextmanager
    def auto_commit(self):
        # 事务：保证数据库数据的一致性（数据同时提交）
        try:
            yield
            self.session.commit()
        except Exception as e:
            # 回滚
            self.session.rollback()
            raise e


# 重写flask_sqlalchemy的BaseQuery类的filter_by
class Query(BaseQuery):

    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


# Query传入SQLALchemy实例
db = SQLALchemy(query_class=Query)


class Base(db.Model):
    # __abstract__ = True：此为数据库基类模型，并不需要创建此表
    __abstract__ = True
    # 类变量是在程序类创建时生成的
    status = Column(SmallInteger, default=1)
    create_time = Column('create time', Integer)

    # 实例变量是在实例化对象时创建的
    def __init__(self):
        # 自动化生成时间戳
        self.create_time = int(datetime.now().timestamp())

    # python动态赋值
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0

