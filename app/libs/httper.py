# -*- coding:utf-8 -*-

# urllib
# requests

import requests


class HTTP(object):

    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        # 三元表达式 简化代码
        if r.status_code != 200:
            return {} if return_json else ''
        else:
            return r.json() if return_json else r.text
