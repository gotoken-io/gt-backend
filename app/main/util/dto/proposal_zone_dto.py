from flask_restplus import Namespace, fields
import app.main.util.dto.currency_dto as currency_dto

api = Namespace('proposal_zone',
                description='proposal zone related operations')

proposal_zone = api.model(
    'proposal_zone', {
        'id':
        fields.String(description='proposal zone id'),
        'name':
        fields.String(required=True, description='proposal zone name'),
        'title':
        fields.String(required=True, description='proposal zone title'),
        'currencies':
        fields.List(fields.Nested(currency_dto.currency_short)),
        'summary':
        fields.String(description='summary'),
        'detail':
        fields.String(description='detail'),
        'cover':
        fields.String(description='cover filename'),
        'theme_color':
        fields.String(required=True, description='proposal zone theme color'),
        'vote_rule':
        fields.String(description='vote rule'),
        'vote_addr_weight_json':
        fields.String(description='this zone vote address relate vote weight'),
        'vote_duration_hours_min':
        fields.Integer(description='vote duration min hours'),
        'vote_duration_hours_max':
        fields.Integer(description='vote duration max hours'),
        'creator_id':
        fields.String(description='creator user.id'),
        'created':
        fields.DateTime(description='created timestamp'),
        'updated':
        fields.DateTime(description='updated timestamp'),
        'multiSigAddress':
        fields.String(description='Multi Signature contract address'),
        'voteAddress':
        fields.String(description='Vote contract address'),
        'total_proposals':
        fields.Integer(description='Total of proposals in the zone'),
    })
