from flask_restplus import Namespace, fields

api = Namespace('comment', description='proposal comment related operations')


_user_get = api.model('user', {
    'id': fields.String(description='user id'),
    'email': fields.String(description='user email address'),
    'username': fields.String(description='user username'),
    'nickname': fields.String(description='user nickname'),
    'avatar': fields.String(description='user avatar url'),
})

_creator_fields = fields.Nested(_user_get)

_comment_reply = api.model('comment', {
    'id': fields.String(description='proposal comment id'),
    'text': fields.String(description='text'),
    'created': fields.DateTime(description='created timestamp'),
    'updated': fields.DateTime(description='updated timestamp'),
    'creator': _creator_fields,
})


# 获取 proposal detail 时,展示 comment list
comment_get_list = api.model('comment', {
    'id': fields.String(description='proposal comment id'),
    'text': fields.String(description='text'),
    'parent_id': fields.String(description='related comment id'),
    'created': fields.DateTime(description='created timestamp'),
    'updated': fields.DateTime(description='updated timestamp'),
    'creator': _creator_fields,
    'replies': fields.List(fields.Nested(_comment_reply))
})

# post/put a new post
comment_post = api.model('comment', {
    'proposal_id': fields.String(required=True, description='related proposal id'),
    'parent_id': fields.Integer(description='related comment id'),
    'text': fields.String(required=True, description='text'),
})