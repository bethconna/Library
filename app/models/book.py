#! -*- coding:utf-8 -*-
# sqlalchemy数据库模型
from sqlalchemy import Column, Integer, String
# 使用flask_sqlalchemy封装sqlalchemy数据库模型
from app.models.base import Base


# Code First（代码创建数据库）：业务驱动 创建数据模型
# ORM（对象关系映射）：数据库数据操作

# 模型层：MVC的M层
# 自定义的数据库继承SQLALchemy模型
class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    autor = Column(String(30), default='未名')
    isbn = Column(String(15), nullable=False, unique=True)
    price = Column(String(20))
    binding = Column(String(20))
    publisher = Column(String(50))
    pages = Column(Integer)
    summary = Column(String(100))
    image = Column(String(50))
    pubdate = Column(String(20))
