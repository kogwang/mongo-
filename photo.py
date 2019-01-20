from flask_uploads import IMAGES, UploadSet,configure_uploads
from flask import current_app as app
import os
app.config['UPLOADED_PHOTO_DEST'] = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads'
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES

photos = UploadSet('PHOTO')
configure_uploads(app,photos)