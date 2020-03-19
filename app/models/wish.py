#! -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, desc, func
from app.models.base import Base, db
from sqlalchemy.orm import relationship
from app.spider.book import Book


class Wish(Base):

    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)
    isbn = Column(String(15), nullable=False)

    # User数据库<->Gift数据库<->Book数据库
    # relationship：sqlalchemy.orm数据库关系模型
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
    def get_user_wishes(cls, uid):
        # 用户礼物列表
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        # 用户礼物列表对应的心愿单数量
        # filter(条件表达式):in_ or_
        # db.session.query查询：跨模型查询表或数据
        # func.count + group_by 分组统计
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(Gift.launched == False,
                                      Gift.isbn.in_(isbn_list),
                                      Gift.status == 1).group_by(Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

