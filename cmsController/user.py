# -*- coding:utf-8 -*-
from flask import Blueprint, request, session
from common.result import SUCCESS, ERROR
import mdbCollection
import logging

cmsUser = Blueprint('cmsUser', __name__)


@cmsUser.before_request
def before_user():
    if 'admin' in session and session['admin'] != None:
        pass
    else:
        return ERROR("登录信息失效，请重新登录", 100)


@cmsUser.route('/cmsUser/list', methods=['POST'])
def getTotalUserCount():
    body = request.get_json()
    page = body.get('page', 1)
    perPage = body.get('perPage', 10)
    skip = perPage * (page - 1)
    limit = perPage
    userList = list(mdbCollection.USER.find({}, {'password': 0}).skip(skip).limit(limit))
    logging.info(userList)
    totalCount = mdbCollection.USER.count()
    result = {
        'totalCount': totalCount,
        'list': userList
    }
    return SUCCESS(result)
