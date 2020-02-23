from flask_restplus import Namespace, fields
import app.main.util.dto.currency_dto as currency_dto
# import app.main.util.dto.user_dto as user_dto

api = Namespace('proposal_claim', description='Proposal claim')

_user_dto = api.model(
    'user', {
        'id': fields.String(description='user id'),
        'email': fields.String(description='user email address'),
        'username': fields.String(description='user username'),
        'nickname': fields.String(description='user nickname'),
        'avatar': fields.String(description='user avatar url'),
    })
user_fields = fields.Nested(_user_dto)

proposal_claim = api.model(
    'proposal_claim',
    {
        'claim_id':
        fields.String(description='claim id'),
        'proposal_id':
        fields.String(description='proposal id'),
        'status_key':
        fields.String(description='proposal claim status key'),
        'user_id':
        fields.String(description='claimer user id'),
        'claimer':
        user_fields,
        # 'creator':
        # user_fields,
        'budget_amount':
        fields.String(description='claimer budget amount'),
        'budget_currency_id':
        fields.String(description='budget currency id'),
        'created':
        fields.DateTime(description='created timestamp'),
        'reason':
        fields.String(required=True, description='proposal claim reason'),
        'payment_address':
        fields.String(required=True,
                      description='claimer use to get token reward address'),
    })
