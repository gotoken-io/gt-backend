from app.main.model.user import User
from ..service.blacklist_service import save_token
from ..service.util.uuid import version_uuid

class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter((User.email==data.get('email').lower()) | (User.username==data.get('email'))).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.public_id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if version_uuid(resp):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            try:
                resp = User.decode_auth_token(auth_token)
                if version_uuid(resp):
                    user = User.query.filter_by(public_id=resp).first()
                    response_object = {
                        'status': 'success',
                        'data': {
                            'id': user.id,
                            'username': user.username,
                            'nickname': user.nickname,
                            'sign': user.sign,
                            'avatar': user.avatar,
                            'email': user.email,
                            'admin': user.admin,
                            'registered_on': str(user.registered_on)
                        }
                    }
                    return response_object, 200
                else:
                    response_object = {
                        'status': 'fail',
                        'message': resp
                    }
                    return response_object, 401
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': str(e)
                }
                return response_object, 500
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
