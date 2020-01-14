from flask_restplus import Namespace, fields

api = Namespace('currency', description='authentication related operations')

currency = api.model('currency', {
    'id': fields.String(description='The currency id'),
    'name': fields.String(description='The currency name'),
    'unit': fields.String(description='The currency unit'),
})