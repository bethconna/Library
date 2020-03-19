# -*- coding:utf-8 -*-

from app.libs.httper import HTTP
from flask import current_app


class Book(object):
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        res = HTTP.get(url)
        # book = query_from_mysql(isbn)
        # if book:
        #     return book
        # else:
        #     save(res)
        self.__fill_single(res)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
        res = HTTP.get(url)
        self.__fill_collection(res)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
