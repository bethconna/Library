#! -*- coding:utf-8 -*-
from flask import current_app
from math import floor
from sqlalchemy import Column, Integer, String, Boolean, Float
from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.book import Book
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# flask_login的get_user装饰器返回User(id)实例化对象
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


class User(UserMixin, Base):

    id = Column(Integer, primary_key=True)
    _password = Column('password', String(128), nullable=False)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    # 方法变属性：读取
    @property
    def password(self):
        return self._password

    # 方法变属性：赋值
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # # 方法变属性：只读属性
    # @password.setter
    # def password(self, raw):
    #     return 'password不可以被写入'

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    # # UserMixin基类函数
    # # flask-login的login_user固定函数名称
    # def get_id(self):
    #     return self.id

    def can_save_to_list(self, isbn):
        """
        1、isbn不符合规则
        2、网站搜索不到该isbn的书
        3、用户赠送列表中已经存在
        4、用户索要列表中已经存在
        """
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = Book()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    # token:1、过期时间 2、加密
    # expiration:token过期时间(默认600s)
    # Serializer:flask自带token加密模块
    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            # get查询模型主键值
            user = User.query.get(uid)
            if user:
                user.password = new_password
                return True
        return False

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )



