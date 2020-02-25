#!/usr/bin/python3
# coding: utf-8
import hashlib
import uuid
from datetime import datetime

from flask import Blueprint, Response
from flask import request, jsonify
from sqlalchemy import or_, and_, not_

from db import session
from apiapp.models import TUser
from common import code_, cache_, token_
from . import validate_json, validate_params

blue = Blueprint('user_api', __name__)


@blue.route('/code/', methods=['GET'])
def get_code():
    phone = request.args.get('phone')
    if phone:
        code_.send_code(phone)
        return jsonify({
            'state': 0,
            'msg': '验证码已发送'
        })

    return jsonify({
        'state': 1,
        'msg': '手机号不能为空'
    })


@blue.route('/regist/', methods=['POST'])
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
        if not code_.valid_code(data['phone'], data['code']):
            return jsonify({
                'state': 2,
                'msg': '验证码输入错误，请确认输入的验证码'
            })

        user = TUser()
        user.name = data.get('name')
        user.phone = data.get('phone')
        user.auth_string = data.get('auth_str')
        user.create_time = datetime.now()

        session.add(user)
        session.commit()

        # 向前端返回信息中，包含一个与用户匹配的token(有效时间为一周)
        # 1. 基于uuid+user_id生成token
        # 2. 将token和user_id保存到缓存（cache_.save_token(token, user_id)）
        # JWT 单点授权登录
        token = token_.gen_token(user.user_id)
        cache_.add_token(token, user.user_id)
    else:
        return jsonify({
            'state': 1,
            'msg': '参数不完速，详情请查看接口文档'
        })

    return jsonify({
        'state': 0,
        'msg': '注册并登录成功',
        'token': token
    })


@blue.route('/login/', methods=['POST'])
def login():
    resp = validate_json()
    if resp: return resp

    resp = validate_params('phone', 'auth_str')
    if resp: return resp

    data = request.get_json()
    try:
        user = session.query(TUser).filter(or_(TUser.phone == data['phone'],
                                               TUser.name == data['phone']),
                                           TUser.auth_string == data['auth_str']).one()

        token = token_.gen_token(user.user_id)
        cache_.add_token(token, user.user_id)

        resp: Response = jsonify({
            'state': 0,
            'msg': '登录成功',
            'token': token
        })

        # 设置响应对象的cookie，向客户端响应cookie
        resp.set_cookie('token', token)
        return resp
    except:
        pass

    return jsonify({
        'state': 4,
        'msg': '用户名或口令输入错误',
    })


@blue.route('/modify_auth/', methods=['POST'])
def modify_auth():
    resp = validate_json()
    if resp: return resp

    resp = validate_params('new_auth_str', 'auth_str', 'token')
    if resp: return resp

    data = request.get_json()

    try:
        user_id = cache_.get_user_id(data['token'])
        if not user_id:
            jsonify({
                'state': 3,
                'msg': '登录已期，需要重新登录并获取新的token',
            })

        user = session.query(TUser).get(int(user_id))
        if user.auth_string == data['auth_str']:
            user.auth_string = data['new_auth_str']
            session.add(user)
            session.commit()

            return jsonify({
                'state': 0,
                'msg': '修改成功'
            })
        return jsonify({
            'state': 4,
            'msg': '原口令不正确'
        })
    except:
        pass

    return jsonify({
        'state': 3,
        'msg': 'token已无效，尝试重新登录',
    })
