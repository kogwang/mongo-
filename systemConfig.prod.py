# -*- coding:utf-8 -*-
"""
生产环境用的配置
"""
SECRET_KEY = 'abcdefg'

# OSS 例
ACCESSKEYID = 'LTAIsajNsK6jCcTD'
ACCESSKEYSECRET = 'RHiDRXVFosnd7jzTY33rPBfzoogiey'

ENDPOINT = 'http://oss-cn-hangzhou.aliyuncs.com'
BUCKETNAME = 'easystock'

# redis
REDIS_HOST = 'localhost'
REDIS_PASSWORD = ''
REDIS_PORT = 6379

# 小程序
APPID = ''
SECRET = ''

# mongo
# MONGO_URL='mongodb://用户:密码@域名或ip:端口/admin'
MONGO_URL = 'mongodb://localhost'

# 缓存刷新模块用的配置
# CACHE_PREFIX用于解决 生产、测试用了同一个redis的key重复的情况，
# 由于微信的sessionKey的限制，如果分开存放的话，可能造成同一天请求过多的sessionKey,导致业务无法进行下去。
# 所以放到redis里面
CACHE_PREFIX = 'PROD_'
CACHE_CONFIG = {
    'TEST': {
        'name': 'TEST',
        'module': 'utils.cache.testCache',
        'func': 'test',
        'kwargs': {'key': 1111}
    }

}
