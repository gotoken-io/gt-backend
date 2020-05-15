from flask_restplus import Namespace, fields

api = Namespace('auth', description='authentication related operations')

user_auth = api.model('auth_details', {
    'email': fields.String(required=True, description='The email address'),
    'password': fields.String(required=True, description='The user password '),
})

address_auth = api.model('auth_address_details', {
    'address': fields.String(required=True, description='The wallet address'),
    'signature': fields.String(required=True, description='Verification Signature '),
})
