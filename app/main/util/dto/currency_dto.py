from flask_restplus import Namespace, fields

api = Namespace('currency', description='authentication related operations')

proposal_zone = api.model(
    'proposal_zone', {
        'id': fields.String(description='proposal zone id'),
        'name': fields.String(required=True, description='proposal zone name'),
        'title': fields.String(required=True,
                               description='proposal zone title'),
    })

currency_short = api.model(
    'currency', {
        'id': fields.String(description='The currency id'),
        'name': fields.String(description='The currency name'),
        'unit': fields.String(description='The currency unit'),
    })

currency = api.model(
    'currency', {
        'id': fields.String(description='The currency id'),
        'name': fields.String(description='The currency name'),
        'unit': fields.String(description='The currency unit'),
        'zones': fields.List(fields.Nested(proposal_zone)),
    })
