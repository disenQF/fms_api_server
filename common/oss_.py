#!/usr/bin/python3
# coding: utf-8

import oss2

small_style = 'image/interlace,1/resize,m_lfit,w_100/quality,q_90/bright,3/contrast,-21'


def get_bucket():
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth('LTAIRiQGIywYBeYN', 'ZOHiNBYPr72dCFog2fLU5Pu9RvVAIf')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'fms-xa-py905')

    return bucket


def upload_head(user_id, file_name, file_path):
    bucket = get_bucket()

    # <yourObjectName>上传文件到OSS时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
    # <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    key = f'head/{user_id}-{file_name}'
    ret = bucket.put_object_from_file(key, file_path)

    if ret.status == 200:
        return bucket.sign_url('GET', key, 3600 * 24 * 7, params={'x-oss-process': small_style})


def get_oss_img_url(user_id, file_name):
    bucket = get_bucket()
    key = f'head/{user_id}-{file_name}'
    return bucket.sign_url('GET', key, 3600 * 24 * 7, params={'x-oss-process': small_style})
