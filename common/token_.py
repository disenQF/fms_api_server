#!/usr/bin/python3
# coding: utf-8

import uuid
import hashlib


def gen_token(user_id):
    md5_ = hashlib.md5()
    md5_.update((uuid.uuid4().hex + str(user_id)).encode('utf-8'))
    md5_.update('&$#()**@'.encode('utf-8'))
    return md5_.hexdigest()
