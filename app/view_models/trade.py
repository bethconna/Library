#! -*- coding:utf-8 -*-
# from collections import namedtuple
from app.view_models.book import BookViewModel


class TradeInfo(object):

    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知时间'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


# MyTrade = namedtuple('MyTrade', ['id', 'book', 'trades_count'])

# class MyTrade(object):
#
#     def __init__(self):
#         pass


class MyTrades(object):
    # 不建议在方法中修改实例属性
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        # my_trade = MyTrade(trade.id, BookViewModel(trade.book), count)
        # 未给trade定义单体类
        my_trade = {
            'wishes_count': count,
            'id': trade.id,
            'book': BookViewModel(trade.book)
        }
        return my_trade

