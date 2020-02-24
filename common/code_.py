#!/usr/bin/python3
# coding: utf-8
import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from common import cache_


def send_code(phone):
    # 1. 生成code
    code_set = set()
    while len(code_set) < 4:
        code_set.add(str(random.randint(0, 9)))
    code = ''.join(code_set)
    # 2. 保存code到缓存 - redis
    cache_.save_code(phone, code)

    # 3. 发送短信
    client = AcsClient('LTAIRiQGIywYBeYN', 'ZOHiNBYPr72dCFog2fLU5Pu9RvVAIf', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "Disen工作室")  # 签名： 途中旅游 或 Disen工作室
    request.add_query_param('TemplateCode', "SMS_128646125")
    request.add_query_param('TemplateParam', '{"code":"%s"}' % code)

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


def valid_code(phone, code):
    # 1. 从缓存中读取phone中code(发送的code)
    code_cache = cache_.get_code(phone)
    # 2. 判断code（输入）和缓存中的code是否相同
    return code_cache == code
