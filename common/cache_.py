#!/usr/bin/python3
# coding: utf-8
from common import rd


def save_code(phone, code):
    rd.set(phone, code, ex=120)   # 两分钟有效时间


def get_code(phone):
    return rd.get(phone)