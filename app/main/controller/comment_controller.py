from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from app.main.service.comment_service import save_new_comment, update_comment
from app.main.service.user_service import get_a_user_by_auth_token
from app.main.util.dto import comment_dto


api = comment_dto.api
comment_get_list = comment_dto.comment_get_list
comment_post = comment_dto.comment_post

# comment api
@api.route('/')
class CommentAPI(Resource):
    """
        Comment Resource
    """
    @api.doc('create new comment')
    @api.expect(comment_post)
    @token_required
    def post(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            post_data['creator_id']=user.id
            return save_new_comment(data=post_data)

    @api.doc('update comment')
    @api.expect(comment_post, validate=True)
    def put(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            post_data['creator_id']=user.id
            return update_comment(data=post_data)
