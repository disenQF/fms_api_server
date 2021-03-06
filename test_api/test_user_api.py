#!/usr/bin/python3
# coding: utf-8

import requests

from unittest import TestCase

HOST = '119.3.170.97'
PORT = 9000

base_url = f'http://{HOST}:{PORT}'

data = {
    'phone': '17791692095',
    'token': '8fd538150b73efaf0d8da6e8234c25b3'
}


class TestUserApi(TestCase):
    def test_a_send_code(self):
        url = base_url + f'/api/code/?phone={data["phone"]}'
        resp = requests.get(url)
        print(resp.json())

    def test_b_regist(self):
        url = base_url + '/api/regist/'
        resp = requests.post(url, json={
            'name': 'disen888',
            'phone': data['phone'],
            'code': '3582',
            'auth_str': '123456'  # 密文要求（前端）：需要使用hash算法
        })
        print(resp.json())

    def test_c_login(self):
        url = base_url + '/api/login/'
        resp = requests.post(url, json={
            'phone': data['phone'],
            'auth_str': '123456'
        })
        resp_data = resp.json()
        print(resp_data)
        if resp_data['state'] == 0:
            data['token'] = resp_data['token']


    def test_d_login(self):
        url = base_url + '/api/modify_auth/'
        resp = requests.post(url, json={
            'token': data['token'],
            'auth_str': '123456',
            'new_auth_str': '123458',
        })
        resp_data = resp.json()
        print(resp_data)

    def test_e_upload_head(self):
        url = base_url+"/api/upload_head/"
        resp = requests.post(url, files={
            'head': ('mm6.jpg', open('mm6.jpg', 'rb'), 'image/jpeg')
        }, cookies={'token': data['token']})

        print(resp.json())

