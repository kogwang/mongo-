# -*- coding:utf-8 -*-

import mdbCollection

mdbCollection.ADMIN_USER.drop()
mdbCollection.ADMIN_USER.insert({'username': 'admin', 'password': '123'})
