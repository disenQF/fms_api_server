#!/usr/bin/python3
# coding: utf-8

from flask import Flask
from flask_cors import CORS

import settings

app = Flask(__name__,
            static_folder=settings.STATIC_DIR,
            static_url_path='/s/')

app.config['ENV'] = 'developement'  # production
app.config['DEBUG'] = True

CORS(app)  # 全局方式支持跨域请求（前端服务器和后端API服务器分开部署）
