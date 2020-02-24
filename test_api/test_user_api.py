#!/usr/bin/python3
# coding: utf-8

import requests

from unittest import TestCase

HOST = 'localhost'
PORT = 5000

base_url = f'http://{HOST}:{PORT}'


class TestUserApi(TestCase):
    def test_regist(self):
        url = base_url + '/api/regist/'
        resp = requests.post(url, json={
            'name': 'rose',
            'phone': '17791692099',
            'code':  '9022',
            'auth_str': '123456'  # 密文要求（前端）：需要使用hash算法
        })
        print(resp.json())