# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify, session
from bson.json_util import dumps
import mdbCollection

admin = Blueprint('admin', __name__)


@admin.route('/admin/login', methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    admin = mdbCollection.ADMIN_USER.find_one({
        'username': username,
        'password': password
    })

    if admin is None:
        result = {
            'code': 100,
            'errorMessage': '账号或密码错误'
        }
    else:
        session['admin'] = dumps(admin)
        result = {
            'code': 0
        }
    return jsonify(result)
