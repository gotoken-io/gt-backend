from flask_restplus import Namespace, fields
from werkzeug.datastructures import FileStorage

api = Namespace('upload', description='upload related operations')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)
