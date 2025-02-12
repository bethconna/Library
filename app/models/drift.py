#! -*- coding:utf-8 -*-
from app.libs.enums import PendingStatus
from app.models.base import Base
from sqlalchemy import Column, Integer, String, SmallInteger


class Drift(Base):
    """
    交易模型
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # 交易记录（历史记录）一般不更改，不建议使用关联模型
    # requester = relationship('User')
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

    # 交易状态
    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
