from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from app.main.service.auth_helper import Auth
import app.main.util.dto.auth_dto as auth_dto

api = auth_dto.api
user_auth = auth_dto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)

    @api.doc('get user info')
    @token_required
    def get(self):
        # get auth token
        return Auth.get_logged_in_user(request)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    @token_required
    def post(self):
        
        return Auth.logout_user(request)