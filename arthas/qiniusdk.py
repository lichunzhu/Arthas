# -*- coding:utf-8 -*-
# user    :chauncylee
# time    :18-9-18 下午15:43
# filename:qiniusdk.py
# IDE     :PyCharm

import os

from arthas import app
from qiniu import Auth, put_data

# 需要填写你的 Access Key 和 Secret Key
access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']
# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = app.config['QINIU_BUCKET_NAME']
domain_prefix = app.config['QINIU_DOMAIN']


def qiniu_upload_file(source_file, save_file_name):
    """
    :param source_file: source_file sent to qiniu cloud
    :param save_file_name: file name on qiniu cloud
    :return: url of saved image
    """
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, save_file_name)
    # 要上传文件的本地路径
    localfile = './sync/bbb.jpg'
    ret, info = put_data(token, save_file_name, source_file.stream)
    print type(info.status_code), info
    assert ret['key'] == save_file_name
    if info.status_code == 200:
        return domain_prefix + save_file_name
    return None
