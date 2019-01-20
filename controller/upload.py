# -*- coding: utf-8 -*-
import base64
import os
import time
from mongodb import PyMongo
import oss2
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask import Blueprint, request
from flask import current_app as app

from common.result import SUCCESS, ERROR

upload = Blueprint('upload', __name__)
mdb = PyMongo()

photos = UploadSet('PHOTO')


@upload.route('/uploadBaseImage', methods=['POST'])
# @token
def uploadImage():
    body = request.get_json()
    if 'image' not in body:
        return ERROR('Missing Image')
    key_id = app.config['ACCESSKEYID']
    key_secert = app.config['ACCESSKEYSECRET']

    endpoint = app.config['ENDPOINT']
    bucket_name = app.config['BUCKETNAME']

    image_strs = body['image']
    urls = []
    for image_str in image_strs:
        affix = image_str.split(';')[0].split('/')[1]
        image_str = image_str.split(',')[1]

        auth = oss2.Auth(key_id, key_secert)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)

        file_name = str(int(round(time.time() * 1000))) + '.' + affix
        imgdata = base64.b64decode(image_str)
        path = app.config['UPLOADED_PHOTO_DEST'] + '/' + file_name
        file = open(path, 'wb')
        file.write(imgdata)
        file.close()
        local_file = path
        result = bucket.put_object_from_file(file_name, local_file)
        os.remove(local_file)
        if result.resp.status == 200:
            urls.append(result.resp.response.url)
        else:
            return ERROR('upload failed')
    return SUCCESS(urls)


@upload.route('/uploadPhoto', methods=['POST'])
# @token
def upload():
    upload_photo = request.files['photo']
    key_id = app.config['ACCESSKEYID']
    key_secert = app.config['ACCESSKEYSECRET']

    endpoint = app.config['ENDPOINT']
    bucket_name = app.config['BUCKETNAME']

    auth = oss2.Auth(key_id, key_secert)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    file_name = str(int(round(time.time() * 1000))) + '.' + upload_photo.mimetype.split('/')[-1]
    local_file = photos.save(upload_photo)
    local_file = app.config['UPLOADED_PHOTO_DEST'] + '/' + local_file
    result = bucket.put_object_from_file(file_name, local_file)
    os.remove(local_file)
    if result.resp.status == 200:
        return SUCCESS(result.resp.response.url)
    else:
        return ERROR('upload failed')



