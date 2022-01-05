# coding:utf-8

import os
import time

from .error import NotFileError, FormatError, NotPathError
def check_file(path):
    # 验证路径是否存在
    if not os.path.exists(path):
        raise NotPathError('not found %s' % path)
    # 验证是为json文件
    if not path.endswith('.json'):
        raise FormatError('need json format')
    # 验证是否为文件
    if not os.path.isfile(path):
        raise NotFileError('this is a not file')

def timestamp_to_date(timestamp):
    timestamp = time.localtime(timestamp)
    date = time.strftime('%Y-%m-%d %H:%M:%S',timestamp)
    return date