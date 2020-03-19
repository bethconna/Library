# -*- coding:utf-8 -*-

def is_isbn_or_key(keyword):
    """
    判断关键字类型（普通关键字？ISBN关键字？）
    """
    # ISBN13 13个0-9的数字
    # ISBN10 10个0-9的数字 + '-'
    isbn_or_key = 'key'
    if len(keyword) == 13 and keyword.isdigit():
        isbn_or_key = 'isbn'
    elif '-' in keyword and len(keyword.replace('-', '')) == 10 and keyword.replace('-', '').isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key