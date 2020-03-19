#! -*- coding:utf-8 -*-
from app.libs.enums import PendingStatus


class DriftViewModel(object):
    """
    单个Drift数据处理模型
    """
    def __init__(self, drift, current_user_id):
        self.data = {}

        self.data = self.__parse(drift, current_user_id)

    def __parse(self, drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'recipient_name': drift.recipient_name,
            'address': drift.address,
            'message': drift.message,
            'mobile': drift.mobile,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'status': drift.pending,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'operator': drift.gifter_nickname if you_are == 'requester' else drift.requester_nickname,
            'status_str': pending_status,
        }
        return r

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are


class DriftCollection(object):
    """
    一组Drift数据处理模型
    """
    def __init__(self, drifts, current_user_id):
        self.data = []

        self.data = self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        r = [DriftViewModel(drift, current_user_id).data for drift in drifts]
        return r
