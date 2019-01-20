# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify
from datetime import datetime
import requests
import json
from systemConfig import APPID, SECRET
import logging
import mdbCollection
import uuid
from redClient import Redis
from shouqianba import client
from common.result import SUCCESS

user = Blueprint('user', __name__)

red = Redis().red


def wxLogin(code):
    appid = APPID
    secret = SECRET
    params = {
        'grant_type': 'authorization_code',
        'appid': appid,
        'secret': secret,
        'js_code': code
    }
    res = requests.get(url='https://api.weixin.qq.com/sns/jscode2session', params=params)
    response = json.loads(res.text)
    return response


@user.route('/login/', methods=['POST'])
def login():
    body = request.get_json()
    wx_code = body['code']
    # headImgUrl = body['headImgUrl']
    # nickname = body['nickname']
    login_response = wxLogin(wx_code)
    if login_response.has_key('errcode'):
        result = {
            'code': 400,
            'errorMessage': login_response['errmsg']
        }
    else:
        open_id = login_response['openid']
        userObj = mdbCollection.USER.find_one({"openId": open_id})
        if userObj is None:
            logging.info('====new user=====')
            new_user = {
                'openId': open_id,
                'applyStatus': 100,
                'createdAt': datetime.now(),
            }
            user_id = mdbCollection.USER.insert_one(new_user).inserted_id
        else:
            logging.info('====old user=====')
            user_id = userObj['_id']

        user_info = {
            'openId': open_id,
            'sessionKey': login_response['session_key'],
            'userId': str(user_id)
        }
        token = uuid.uuid1()
        red.set(token, json.dumps(user_info))

    return SUCCESS(str(token))

@user.route('/tttt', methods=['POST'])
# @token
def tttt():
    body = request.get_json()
    amount = body.get('amount', 0)
    c = client.ShouqianbaClient()
    re = c.precreate(amount, "3")
    # re={}
    return SUCCESS(re)


