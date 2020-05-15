from app.main.model.user import User
from ..service.blacklist_service import save_token
from ..service.util.uuid import version_uuid
from app.main.model.wallet import Wallet
from app.main import db
from secrets import token_hex


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter((User.email == data.get('email').lower()) | (
                User.username == data.get('email'))).first()
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
    def login_address(data, zoneId):
        try:
            # fetch the user data
            wallet = Wallet.query.filter_by(
                address=data.get('address'), zone_id=zoneId).first()
            if not wallet:
                response_object = {
                    'status': 'fail',
                    'message': 'Address not found'
                }
                return response_object, 404

            user = User.query.filter_by(id=wallet.user_id).first()
            if not user:
                response_object = {
                    'status': 'fail',
                    'message': 'User not found'
                }
                return response_object, 404

            checkNonce = Wallet.checkNonce(wallet, data.get("signature"))
            # Invalidate the nonce
            wallet.nonce = None
            db.session.commit()
            if checkNonce:
                response_object = {
                    'status': 'fail',
                    'message': 'Wrong Signature'
                }
                return response_object, 401

            auth_token = User.encode_auth_token(user.public_id)

            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'Authorization': auth_token.decode()
            }
            return response_object, 200

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def get_nonce(address):
        try:
            # fetch the user data
            wallet = Wallet.query.filter_by(
                address=address).first()

            if not wallet:
                response_object = {
                    'status': 'fail',
                    'message': 'Address not found'
                }
                return response_object, 404

            user = User.query.filter_by(id=wallet.user_id).first()

            if not user:
                response_object = {
                    'status': 'fail',
                    'message': 'User not found'
                }
                return response_object, 404

            wallet.nonce = str(token_hex(32))
            db.session.commit()
            response_object = {
                'status': 'success',
                'nonce':  wallet.nonce,
                'userId': wallet.user_id
            }
            return response_object, 200

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
