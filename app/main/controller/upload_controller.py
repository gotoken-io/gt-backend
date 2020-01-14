from flask import request
from flask_restplus import Resource
from werkzeug.utils import secure_filename
import os

from app.main.util.decorator import admin_token_required, token_required
from app.main.service.upload_service import save_new_image, delete_image, get_config
from app.main.util.dto import upload_dto
from app.main.config import basedir

api = upload_dto.api
upload_parser = upload_dto.upload_parser

@api.route('/image/')
@api.response(400, 'No file part')
@api.response(404, 'No selected file')
@api.expect(upload_parser)
class Upload(Resource):
    def post(self):
        if 'file' not in request.files:
            api.abort(400)

        file = request.files["file"]

        return save_new_image(file)

    
@api.route('/file/<string:key>')
class File(Resource):
    """
        File Resource
    """

    @api.doc('delete upload file')
    def delete(self, key):
        '''Delete file'''
        return delete_image(key)

@api.route('/config/')
class Config(Resource):
    """
        Upload Config Resource
    """

    @api.doc('get upload config')
    def get(self):
        '''get upload config'''
        return get_config(), 200