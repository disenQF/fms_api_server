#!/usr/bin/python3
# coding: utf-8
from datetime import datetime

from flask import Blueprint
from flask import request, jsonify

from db import session
from apiapp.models import TUser

blue = Blueprint('user_api', __name__)


@blue.route('/regist/', methods=['GET', 'POST'])
def regist():
    # 要求JSON数据格式：
    valid_fields = {"name", "phone", "code", "auth_str"}
    data = request.get_json()  # 获取上传的json数据
    if data is None:
        return jsonify({
            'state': 4,
            'msg': '必须提供json格式的参数'
        })


    # 验证参数的完整性
    if set(data.keys()) == valid_fields:

        # 验证输入的验证码是否正确

        user = TUser()
        user.name = data.get('name')
        user.phone = data.get('phone')
        user.auth_string = data.get('auth_str')
        user.create_time = datetime.now()

        session.add(user)
        session.commit()

    else:
        return jsonify({
            'state': 1,
            'msg': '参数不完速，详情请查看接口文档'
        })

    return jsonify({
        'state': 0,
        'msg': '注册成功',
        'data': data
    })
