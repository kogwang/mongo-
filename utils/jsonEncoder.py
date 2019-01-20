# -*- coding:utf-8 -*-
import json
from decimal import Decimal
from datetime import datetime

"""
json序列化的时候 有的对象不能序列化，需要用到encoder。
以下是一些可能会用到的encoder,具体可以看项目再写新的。

usage:
        json.dumps(page_data, cls=CustomizedJSONEncoder, ensure_ascii=False)
"""


class DatetimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        super(DatetimeEncoder, self).default(o)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


class CustomizedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, datetime):
            return o.isoformat()
        super(CustomizedJSONEncoder, self).default(o)

