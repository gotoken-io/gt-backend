from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
import app.main.util.dto.user_dto as user_dto
from app.main.service import user_service

api = user_dto.api
_user = user_dto.user
user_get = user_dto.user_get
user_get_all = user_dto.user_get_all

save_new_user = user_service.save_new_user
get_all_users =user_service.get_all_users
get_a_user =user_service.get_a_user
get_a_user_by_auth_token =user_service.get_a_user_by_auth_token
update_user_avatar = user_service.update_user_avatar

@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    # @admin_token_required
    # @token_required
    # 记得替换回 _user
    @api.marshal_list_with(user_get_all, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(user_get, envelope='data')
    def get(self, id):
        """get a user given its identifier"""
        user = get_a_user(id)
        if not user:
            api.abort(404)
        else:
           
            return user

@api.route('/avatar')
@api.response(404, 'User not found.')
class UserAvatar(Resource):
    @api.doc('update user avatar')
    @token_required
    def post(self):
        """update user avatar"""
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return update_user_avatar(id=user.id, avatar=post_data['avatar'])

