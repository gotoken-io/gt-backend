from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
import app.main.util.dto.proposal_dto as proposal_dto
import app.main.util.dto.user_dto as user_dto
import app.main.util.dto.wallet_dto as wallet_dto
from app.main.service import user_service

api = user_dto.api
_user = user_dto.user
_forget_password = user_dto.forget_password
_reset_password = user_dto.reset_password
user_get = user_dto.user_get
user_get_all = user_dto.user_get_all
page_of_proposals = proposal_dto.page_of_proposals

save_new_user = user_service.save_new_user
get_all_users = user_service.get_all_users
# get_a_user = user_service.get_a_user
get_a_user_created_proposal = user_service.get_a_user_created_proposal
get_a_user_by_auth_token = user_service.get_a_user_by_auth_token
update_user_avatar = user_service.update_user_avatar
update_user_info = user_service.update_user_info
forget_password = user_service.forget_password
reset_password = user_service.reset_password


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


@api.route('/<username>')
@api.param('username', 'Username')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(user_get, envelope='data')
    def get(self, username):
        """get a user by username"""
        user = user_service.get_a_user_by_username(username)
        if not user:
            api.abort(404)
        else:

            return user


@api.route('/<username>/proposal')
@api.param('username', 'Username')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user proposals')
    @api.marshal_with(page_of_proposals, envelope='data')
    def get(self, username):
        """get a user proposals"""
        user = user_service.get_a_user_by_username(username)
        if not user:
            api.abort(404)
        else:

            p_type = request.args.get("p_type", "created")
            page = int(request.args.get("page", 1))
            if p_type == "created":
                proposals = get_a_user_created_proposal(id=user.id, page=page)
            return proposals


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

            return update_user_avatar(id=user.id,
                                      avatar=post_data['avatar'],
                                      old_avatar=post_data['old_avatar'])


@api.route('/info')
@api.response(404, 'User not found.')
class UserAvatar(Resource):
    @api.doc('update user info')
    @token_required
    def post(self):
        """update user info"""
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return update_user_info(user, post_data)
        else:
            response_object = {
                'status': 'fail',
                'message': 'User is not exit',
            }
            return response_object, 404


# current logined user wallet
@api.route('/wallet')
class UserWallet(Resource):
    @api.doc('get user wallet')
    @token_required
    @api.marshal_list_with(wallet_dto.user_wallet_get, envelope='data')
    def get(self):
        # get current user token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)
        if not user:
            api.abort(404)
        else:
            return user_service.get_user_wallet(user)

    @api.doc('add user wallet address')
    @token_required
    def post(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            post_data['user_id'] = user.id
            return user_service.add_user_wallet_addr(data=post_data)

    @api.doc('update user wallet address')
    @token_required
    def put(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            post_data['user_id'] = user.id
            return user_service.update_user_wallet_addr(data=post_data)


@api.route('/forget-password')
class ForgetPasswordAPI(Resource):
    """
    Forget password
    """
    @api.doc('forget password')
    @api.expect(_forget_password)
    def post(self):
        """submit forget password request"""
        data = request.json
        return forget_password(data)


@api.route('/reset-password')
class ResetPasswordAPI(Resource):
    """
    Reset password
    """
    @api.doc('reset password')
    @api.expect(_reset_password)
    def post(self):
        """submit reset password request"""
        data = request.json
        return reset_password(data)