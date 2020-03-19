#! -*- coding:utf-8 -*-


# 标准定义类
class BookViewModel(object):
    """
        单book属性
    """
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.price = book['price']
        self.image = book['image'] or ''
        self.summary = book['summary']
        self.author = '、'.join(book['author'])
        self.isbn = book['isbn']
        self.pubdate = book['pubdate'] or ''
        self.binding = book['binding'] or ''

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BooksViewModel(object):
    """
        books属性组
    """
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, books, keyword):
        self.total = books.total
        self.books = [BookViewModel(book) for book in books.books]
        self.keyword = keyword


class _BookViewModel(object):

    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'keyword': keyword,
            'total': 0
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'keyword': keyword,
            'total': 0
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'] or '',
            'pages': data['pages'] or '',
            'price': data['price'] or '',
            'image': data['image'] or '',
            'summary': data['summary'] or '',
            'author': '、'.join(data['author']) or ''
        }
        return book