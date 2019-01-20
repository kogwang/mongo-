# -*- coding:utf-8 -*-

SECRET_KEY = 'abcdefg'

# OSS 例
ACCESSKEYID = 'LTAIsajNsK6jCcTD'
ACCESSKEYSECRET = 'RHiDRXVFosnd7jzTY33rPBfzoogiey'

ENDPOINT = 'http://oss-cn-hangzhou.aliyuncs.com'
BUCKETNAME = 'easystock'

# redis
REDIS_HOST = 'localhost'
REDIS_PASSWORD = ''
REDIS_PORT=6379

# 小程序
APPID = ''
SECRET = ''

# mongo
# MONGO_URL='mongodb://用户:密码@域名或ip:端口/admin'
MONGO_URL = 'mongodb://localhost'

# 缓存刷新模块用的配置
CACHE_PREFIX = 'TEST_'
CACHE_CONFIG = {
    'TEST': {
        'name': 'TEST',
        'module': 'utils.cache.testCache',
        'func': 'test',
        'kwargs': {'key': 1111}
    }

}
