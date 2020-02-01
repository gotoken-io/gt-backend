from flask_restplus import Namespace, fields
import app.main.util.dto.currency_dto as currency_dto
import app.main.util.dto.proposal_zone_dto as proposal_zone_dto
import app.main.util.dto.user_dto as user_dto
from app.main.util.dto.comment_dto import comment_get_list

api = Namespace('proposal', description='proposal related operations')

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
    'category',{
        'id': fields.String(description='proposal category id'),
        'name': fields.String(required=True, description='proposal category name'),
        'name_en': fields.String(description='proposal category name(en)'),
        'order': fields.Integer(description='proposal category order index', default=0),
        'proposals_count': fields.Integer(description='related proposal count'),
    }
)

# 用户创建的 proposal
proposal_created_item = api.model(
    'proposal', {
        'id': fields.String(description='proposal id'),
        'title': fields.String(required=True, description='proposal title'),
        'summary': fields.String(description='summary'),
        'detail': fields.String(description='detail'),
        'amount': fields.String(description='proposal amount'),
        'status': fields.String(description='proposal status'),
        'creator_id': fields.String(description='creator user.id'),
        'created': fields.DateTime(description='created timestamp'),
        'updated': fields.DateTime(description='updated timestamp'),
        'tag': fields.String(description='tag'),
        'category': fields.Nested(proposal_category),
        'zone': fields.Nested(proposal_zone_dto.proposal_zone),
        'currency_unit': fields.Nested(currency_dto.currency),
    })

proposals_created_fields = fields.List(fields.Nested(proposal_created_item))
user_get = api.model(
    'user',
    {
        'email': fields.String(required=True,
                               description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'avatar': fields.String(description='user avatar'),
        'public_id': fields.String(description='user public Identifier'),
        'id': fields.String(description='user Identifier'),
        # 'proposals_created': proposals_created_fields
    })

creator_fields = fields.Nested(user_get)


proposal = api.model(
    'proposal',
    {
        'id': fields.String(description='proposal id'),
        'zone_proposal_id': fields.String(description='proposal id in zone'),
        'title': fields.String(required=True, description='proposal title'),
        'summary': fields.String(description='summary'),
        'detail': fields.String(description='detail'),
        'amount': fields.String(description='proposal amount'),
        'status': fields.String(description='proposal status'),
        'creator_id': fields.String(description='creator user.id'),
        'created': fields.DateTime(description='created timestamp'),
        'updated': fields.DateTime(description='updated timestamp'),
        'tag': fields.String(description='tag'),
        'category': fields.Nested(proposal_category),
        'zone': fields.Nested(proposal_zone_dto.proposal_zone),
        'creator': creator_fields,
        'currency_unit': fields.Nested(currency_dto.currency),
        'comments_count': fields.Integer(description='proposal comments count'),
    })

page_of_proposals = api.inherit(
    'Page of proposals', pagination,
    {'items': fields.List(fields.Nested(proposal))})

proposal_post = api.model(
    'proposal', {
        'zone_id': fields.String(required=True,
                                 description='proposal zone id'),
        'title': fields.String(required=True, description='proposal title'),
        'summary': fields.String(description='summary'),
        'detail': fields.String(description='detail'),
        'amount': fields.String(description='proposal amount'),
        'status': fields.String(description='proposal status'),
        'tag': fields.String(description='proposal tag'),
    })

proposal_put = api.model(
    'proposal', {
        'title': fields.String(required=True, description='proposal title'),
        'summary': fields.String(description='summary'),
        'detail': fields.String(description='detail'),
        'amount': fields.String(description='proposal amount'),
        'tag': fields.String(description='proposal tag'),
    })
