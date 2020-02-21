from flask_restplus import Namespace, fields
import app.main.util.dto.currency_dto as currency_dto

api = Namespace('proposal_claim', description='Proposal claim')

proposal_claim = api.model(
    'proposal_claim', {
        'id':
        fields.String(description='claim id'),
        'proposal_id':
        fields.String(description='proposal id'),
        'user_id':
        fields.String(description='claimer user id'),
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
