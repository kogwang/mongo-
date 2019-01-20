# -*- coding:utf-8 -*-
# from flask import request, abort, jsonify
# import functools
# import json
# import jwt
# from flask import current_app as app


# def token(func):
#     """
#     这个使用JWT的token
#     """
#     @functools.wraps(func)
#     def wrapper(*args, **kw):
#         body = request.get_json()
#         if 'token' in body:
#             token = body['token']
#             try:
#                 token = jwt.decode(token, app.config['TOKEN_SECRET'], algorithms=['HS256'])
#             except jwt.exceptions.InvalidTokenError:
#                 # abort(401)
#                 return jsonify({'code': 100, 'err': '无效token'})
#             if token:
#                 userinfo = {
#                     'username': token['username'],
#                     'uid': token['uid']
#                 }
#                 setattr(request, 'userInfo', userinfo)
#             return func(*args, **kw)
#         else:
#             return jsonify({'code': 100, 'err': '无效token'})
#
#     return wrapper


import functools
from flask import request
from systemConfig import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
import redis
import logging
import json
from common.result import ERROR

red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)

def token(func):
    """
    这个是用redis等实现的token
    """

    @functools.wraps(func)
    def wrapper(*args, **kw):
        body = request.get_json()
        if body.has_key('token') and body['token'] != None:
            token = body['token']
            user_info = red.get(token)
            if user_info is None:
                return ERROR(100, "登录信息失效，请重新登录")
            logging.info(user_info)
            user_info = json.loads(user_info)
            setattr(request, 'userInfo', user_info)
            result = func(*args, **kw)
            return result
        else:
            return ERROR(100, "登录信息失效，请重新登录")

    return wrapper
