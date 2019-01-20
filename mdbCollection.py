# -*- coding:utf-8 -*-
from mongodb import PyMongo

mdb = PyMongo()

USER = mdb.db['user']
ADMIN_USER = mdb.db['adminUser']
