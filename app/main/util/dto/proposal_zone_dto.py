from flask_restplus import Namespace, fields

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
        'token':
        fields.String(required=True, description='proposal zone token'),
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
    })
