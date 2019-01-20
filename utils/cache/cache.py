# -*- coding:utf-8 -*-
# @Auther : liubin
# @Time : 2018/9/5
"""
利用反射，实现需要的用到缓存的方法直接可配置化调用

usage:

config.py
    CACHE_PREFIX = 'PROD_'
    CACHE_CONFIG = {
        'TEST': {
                'name': 'TEST',
                'module': 'utils.cache.testCache',
                'func': 'test',     # name of the function
                'kwargs': {'key': 1111}
        }
        'QUESTION_OF_TAGS': {
            'name': 'QUESTION_OF_TAGS',
            'module': 'wdController.tag',
            'func': 'questByTagForCache',
            'kwargs': {'skip': 0, 'limit': 10, 'autoRefresh': True}
        },
        'EXCLUSIVE_PAGE': {
            'name': 'EXCLUSIVE_PAGE',
            'module': 'service.userService',
            'class': 'UserService',
            'func': 'exclusiveHomePageCache',
            'kwargs': {},
            'type': 'CLASS',
            'methodType': 'classmethod'  / 'staticmethod'
        }
    }
xxx.py
    from utils.cache.cache import CacheFactory

    data = CacheFactory('TEST').getInstance().get()

utils.cache.testCache.py

    def test(**kwargs):
        pass
"""
import redis
from systemConfig import REDIS_HOST, REDIS_PASSWORD,REDIS_PORT
import importlib
from bson.json_util import dumps, loads, ObjectId
import logging
from systemConfig import CACHE_PREFIX, CACHE_CONFIG
from mongodb import PyMongo
import threading
import logger

red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
# red = redis.Redis(host='localhost', port=6379, db=0)
mdb = PyMongo()


class CacheFactory:
    def __init__(self, name):
        self.name = name

    def getInstance(self):
        return Cache(CACHE_CONFIG[self.name])


class Cache:
    def __init__(self, cacheConfig):
        self.cacheConfig = cacheConfig
        self.tp = cacheConfig.get('type', None)
        self.methodType = cacheConfig.get('methodType', None)
        if self.tp == 'CLASS':
            self.module = importlib.import_module(cacheConfig['module'])
            self.clazz = getattr(self.module, cacheConfig['class'])
            if self.methodType == 'classmethod' or self.methodType == 'staticmethod':
                self.func = getattr(self.clazz, cacheConfig['func'])
            else:
                self.func = getattr(self.clazz(), cacheConfig['func'])
        else:
            self.module = importlib.import_module(cacheConfig['module'])
            self.func = getattr(self.module, cacheConfig['func'])

    def get(self, prefixId=None, **kwargs):
        """
        get the cache data directly,
        if not cached , invoke refresh()
        :param prefixId: customed prefixId
        :param kwargs: the params of the func in CACHE_CONFIG
        :return: cached data
        """
        name = self.cacheConfig.get('name', None)
        if not name:
            raise Exception('name is invalid => ' + repr(name))
        if prefixId is None:
            key = CACHE_PREFIX + name
        else:
            key = CACHE_PREFIX + name + '_' + str(prefixId)
        logging.info(u'get cache of key :' + key)
        re = red.get(key)
        if re is None or re == 'null' or re == '':
            logging.info(u'cache key dose not exists:' + repr(key))
            return self.refresh(key, **kwargs)
        return loads(re)

    def refresh(self, key=None, **kwargs):
        """
        refresh the cached data and return the new data
        :param key: specified key of cache
        :param kwargs: the params of the func in CACHE_CONFIG
        :return:
        """
        kw = self.cacheConfig.get('kwargs', {})
        if key is None:
            key = CACHE_PREFIX + self.cacheConfig['name']
        kw.update(kwargs)
        re = self.func(**kw)
        logging.info(u'refresh cache' + key)
        red.set(key, dumps(re))
        return re

    def refreshAsync(self, key=None, **kwargs):
        threading.Thread(target=self.refresh, args=(key,), kwargs=kwargs).start()


# if __name__ == '__main__':
#     CacheFactory('TEST').getInstance().refresh()
