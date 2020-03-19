#! -*- coding:utf-8 -*-
from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, desc, func
from app.models.base import Base, db
from sqlalchemy.orm import relationship
from app.spider.book import Book


class Gift(Base):

    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)
    isbn = Column(String(15), nullable=False)

    # User数据库<->Gift数据库<->Book数据库
    # （读取模型时使用）relationship：sqlalchemy.orm数据库关系模型
    # 模型关联的信息是实时的
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))

    @property
    def book(self):
        book = Book()
        book.search_by_isbn(self.isbn)
        return book.first

    @classmethod
    def get_user_gifts(cls, uid):
        # 用户礼物列表
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 用户礼物列表对应的心愿单数量
        # filter条件表达式
        # db.session.query查询：跨模型查询表或数据
        # func.count + group_by 分组统计
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                      Wish.isbn.in_(isbn_list),
                                      Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    # Gift()是一个礼物，类方法recent()是对一组礼物的操作
    @classmethod
    def recent(cls):
        """
        最近上传
        """
        # 链式调用：主体Query + 子函数 + 调用all()
        # group_by(Gift.isbn).distinct() 分组去重
        # order_by(Gift.create_time) 时间排序
        # limit(current_app.config['RECENT_BOOK_COUNT']) 书籍展示数量限制
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).distinct().order_by(
            desc(Gift.create_time)).limit(current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gift

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

