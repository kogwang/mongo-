# -*- coding:utf-8 -*-
from pymongo import MongoClient
from systemConfig import MONGO_URL

class PyMongo():

    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client['test_database']

