from flask_restplus import Namespace, fields
import app.main.util.dto.currency_dto as currency_dto
import app.main.util.dto.proposal_zone_dto as proposal_zone_dto
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

pagination = api.model(
    'A page of results', {
        'page':
        fields.Integer(description='Number of this page of results'),
        'pages':
        fields.Integer(description='Total number of pages of results'),
        'per_page':
        fields.Integer(description='Number of items per page of results'),
        'total':
        fields.Integer(description='Total number of results'),
    })

proposal_category = api.model(
    'category', {
        'id': fields.Integer(description='proposal category id'),
        'name': fields.String(required=True,
                              description='proposal category name'),
        'name_en': fields.String(description='proposal category name(en)'),
    })
creator_fields = fields.Nested(_user_dto)

proposal = api.model(
    'proposal', {
        'id': fields.String(description='proposal id'),
        'zone_proposal_id': fields.String(description='proposal id in zone'),
        'title': fields.String(required=True, description='proposal title'),
        'summary': fields.String(description='summary'),
        'tag': fields.String(description='tag'),
        'category': fields.Nested(proposal_category),
        'zone': fields.Nested(proposal_zone_dto.proposal_zone),
        'currency_unit': fields.Nested(currency_dto.currency),
        'creator': creator_fields,
        'comments_count':
        fields.Integer(description='proposal comments count'),
    })

proposal_claim = api.model(
    'proposal_claim',
    {
        'claim_id':
        fields.String(description='claim id'),
        'proposal_id':
        fields.String(description='proposal id'),
        'proposal':
        fields.Nested(proposal),
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
        'result':
        fields.String(required=True, description='proposal claim result'),
        'payment_address':
        fields.String(required=True,
                      description='claimer use to get token reward address'),
    })

page_of_proposal_claim = api.inherit(
    'Page of proposal claims', pagination,
    {'items': fields.List(fields.Nested(proposal_claim))})
