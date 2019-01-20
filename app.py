# -*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
import systemConfig
import os
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_cors import CORS
import logger
from redClient import Redis

app = Flask(__name__)
app.config.from_object(systemConfig)
# flask_uploads
app.config['UPLOADED_PHOTO_DEST'] = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads'
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES
CORS(app, supports_credentials=True)
photos = UploadSet('PHOTO')
configure_uploads(app, photos)

# 用redis存储session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis().red


@app.route('/')
def hello_world():
    return "hello,world"


@app.route('/test', methods=['POST',])
def api_test():
    print(request.get_json()['data'])
    result = {
        'code': 0,
        'data': 1
    }
    return jsonify(result)

def register_blueprints():
    from controller.user import user
    app.register_blueprint(user, url_prefix='/user')

    from cmsController.admin import admin
    app.register_blueprint(admin)
    from cmsController.user import cmsUser
    app.register_blueprint(cmsUser)
    # from controller.upload import upload
    # app.register_blueprint(upload)


register_blueprints()

if __name__ == '__main__':
    # app.run(host = '0.0.0.0',debug=True)
    app.run(debug=True,port=5000)