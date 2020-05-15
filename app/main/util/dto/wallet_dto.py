from flask_restplus import Namespace, fields
import app.main.util.dto.currency_dto as currency_dto

api = Namespace('user', description='user wallet')

proposal_zone_short = api.model(
    'proposal_zone',
    {
        'id': fields.String(description='proposal zone id'),
        'name': fields.String(required=True, description='proposal zone name'),
        'title': fields.String(required=True,
                               description='proposal zone title'),
        # 'summary': fields.String(description='summary'),
    })

currency_short = api.model(
    'currency', {
        'id': fields.String(description='The currency id'),
        'name': fields.String(description='The currency name'),
        'unit': fields.String(description='The currency unit'),
    })

user_wallet_get = api.model(
    'user',
    {
        'address':
        fields.String(required=True,
                      description='user proposal zone token address'),
        'nonce':
        fields.String(required=False,
                      description='Nonce code for security checks'),
        # 'zone_id':
        # fields.Integer(),
        # 'currency_id':
        # fields.Integer(),
        'zone':
        fields.Nested(proposal_zone_short),
        'currency':
        fields.Nested(currency_short),
    })
