#!/usr/bin/python3
# coding: utf-8

import requests

from unittest import TestCase

HOST = 'localhost'
PORT = 5000

base_url = f'http://{HOST}:{PORT}'

data = {
    'phone': '17602931841'
}


class TestUserApi(TestCase):
    def test_a_send_code(self):
        url = base_url + f'/api/code/?phone={data["phone"]}'
        resp = requests.get(url)
        print(resp.json())

    def test_b_regist(self):
        url = base_url + '/api/regist/'
        resp = requests.post(url, json={
            'name': 'zhiwen888',
            'phone': data['phone'],
            'code': '3408',
            'auth_str': '123456'  # 密文要求（前端）：需要使用hash算法
        })
        print(resp.json())
