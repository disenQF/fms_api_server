#!/usr/bin/python3
# coding: utf-8
import hashlib
import uuid
from datetime import datetime

import os
from flask import Blueprint, Response
from flask import request, jsonify
from sqlalchemy import or_, and_, not_

import settings
from db import session
from apiapp.models import TUser
from common import code_, cache_, token_, oss_
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
        head_url = ''
        if user.head:
            head_url = cache_.get_head_url(user.head)
            if not head_url:
                head_url = oss_.get_oss_img_url(user.head)
                cache_.save_head_url(user.head, head_url)

        resp: Response = jsonify({
            'state': 0,
            'msg': '登录成功',
            'token': token,
            'head': head_url
        })

        # 设置响应对象的cookie，向客户端响应cookie
        resp.set_cookie('token', token)
        resp.set_cookie('head', head_url)

        return resp
    except Exception as e:
        print(e)

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


@blue.route('/upload_head/', methods=["POST"])
def upload_head():
    # 前端上传图片的两种方式（文件对象上传， base64字符串上传）
    # FileStorage:  'content_length', 'content_type', 'filename', 'headers', 'mimetype', 'save',
    upload_file = request.files.get('head')
    token = request.cookies.get('token')  # 1. 从请求参数中获取  2. 从请求头的Cookie中获取

    print(upload_file.filename, upload_file.content_type, upload_file.mimetype)

    user_id = cache_.get_user_id(token)
    file_name = upload_file.filename

    save_file_path = os.path.join(settings.TEMP_DIR, file_name)
    # 保存上传的文件到临时的目录中
    upload_file.save(save_file_path)

    # 将临时的文件上传到oss服务器中， 并获取到缩小后的图片URL
    head_url = oss_.upload_head(user_id, file_name, save_file_path)

    # 将head_url保存到用户的表中
    user = session.query(TUser).get(user_id)
    user.head = f'{user_id}-{file_name}'  # 存储oss上的key对象
    session.add(user)
    session.commit()

    # 将头像的URL 存到 redis中
    cache_.save_head_url(user.head, head_url)

    return jsonify({
        'state': 0,
        'msg': '上传成功',
        'head': head_url
    })


@blue.route('/head/', methods=["GET"])
def get_head():
    token = request.cookies.get('token')  # 1. 从请求参数中获取  2. 从请求头的Cookie中获取

    user_id = cache_.get_user_id(token)

    user = session.query(TUser).get(user_id)

    head_url = cache_.get_head_url(user.head)
    if not head_url:
        head_url = oss_.get_oss_img_url(user.head)
        cache_.save_head_url(user.head, head_url)

    return jsonify({
        'state': 0,
        'head': head_url
    })
