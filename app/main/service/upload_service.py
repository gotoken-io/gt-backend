from app.main.util.file import file_type
from app.main import s3_store
# from app.main.util.flask_s3 import get_bucket, get_buckets_list, get_s3_config
# from flask_restplus import Resource, Api, Namespace, fields
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage
import random, string
import os

# 允许上传的图片类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# generate random file name
def random_name(num=10):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(num))

def save_new_image(file):
    if file.filename == '':
        return {
            'status': 'fail',
            'message': 'no set filename'
        }

    if not allowed_file(file.filename):
        allowed_file_ext = ','.join(ALLOWED_EXTENSIONS)
        return {
            'status': 'fail',
            'message': 'only support file extension:' + allowed_file_ext,
            'data': allowed_file_ext
        }

    if file and allowed_file(file.filename):

        mime = file.filename.rsplit(".")[1]
        file_key = random_name() + "." + mime

        my_bucket = s3_store.get_bucket()
        my_bucket.Object(file_key).put(Body=file,ContentType=file_type(file.filename))
        return {
            'status': 'success',
            'message': 'upload file success',
            'data': file_key
        }

def get_config():
    return {
        "status":"success",
        "data": s3_store.get_s3_config(),
    }

def delete_image(key):
    my_bucket = s3_store.get_bucket()
    my_bucket.Object(key).delete()
    # 不管怎样都返回 del 成功，即使 key 不存在也不会报错
    return {
        "status": "success",
        "message": "file delte success"
    }

