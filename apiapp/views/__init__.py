#!/usr/bin/python3
# coding: utf-8
from flask import request, jsonify


def validate_json():
    if not request.get_json():
        return jsonify({
            'state': 1,
            'msg': '未提供json格式数据'
        })


def validate_params(*param):
    k1 = ','.join(sorted(list(param)))
    k2 = ','.join(sorted(request.get_json().keys()))
    print(k1, k2)
    if not k1 == k2:
        return jsonify({
            "state": 2,
            "msg": "POST请求的json数据参数不完整"
        })