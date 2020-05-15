import uuid
import datetime

from app.main import db
from sqlalchemy import and_
from app.main.model.user import User
from app.main.model.wallet import Wallet
from app.main.model.proposal import Proposal, ProposalZone
from app.main.model.currency import Currency

from app.main.service.util import save_changes
from app.main.service.upload_service import delete_image
from app.main.service.util.uuid import version_uuid
from app.main.util.token import generate_email_token, validate_token
from app.main.settings import Operations
from app.main.util.mail import send_reset_pwd_mail
from app.main.config import Config


def save_new_user(data):
    user = User.query.filter((User.email == data['email'].lower())
                             | (User.username == data['username'])).first()
    if not user:
        new_user = User(public_id=str(uuid.uuid4()),
                        email=data['email'].lower(),
                        username=data['username'].lower(),
                        password=data['password'],
                        registered_on=datetime.datetime.utcnow())
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User email or username already exists. Please Log in.',
        }
        return response_object, 409


def update_user_info(user, data):
    # if(data['avatar']):
    #     user.avatar = data['avatar']

    if (data['nickname']):
        user.nickname = data['nickname']

    if (data['sign']):
        user.sign = data['sign']

    # save to db
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'User info update success',
    }
    return response_object, 200


def update_user_avatar(id, avatar, old_avatar):
    user = User.query.filter_by(id=id).first()
    if user:
        user.avatar = avatar
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'User avatar update success',
        }
        # delete old avatar in s3
        if old_avatar:
            delete_image(old_avatar)

        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User is not exit',
        }
        return response_object, 404


def get_all_users():
    return User.query.all()


def search_by_mail(content):
    return User.query.filter(User.email.like("%"+content+"%")).all()


def get_a_user_by_id(id):
    user = User.query.filter(User.id == id).first()
    # user created proposals
    # created_proposals = Proposal.query.filter_by(creator_id=id, is_delete=0).paginate(
    #     page, Config.PROPOSAL_PER_PAGE, False)

    # user.proposals_created = created_proposals
    return user


def get_a_user_by_username(username):
    user = User.query.filter(User.username == username).first()
    # user created proposals
    # created_proposals = Proposal.query.filter_by(creator_id=id, is_delete=0).paginate(
    #     page, Config.PROPOSAL_PER_PAGE, False)

    # user.proposals_created = created_proposals
    return user


# get a user created proposals
def get_a_user_created_proposal(id, page):
    created_proposals = Proposal.query.filter_by(
        creator_id=id, is_delete=0).paginate(page, Config.PROPOSAL_PER_PAGE,
                                             False)

    return created_proposals


def get_a_user_by_auth_token(auth_token):
    resp = User.decode_auth_token(auth_token)
    if version_uuid(resp):
        return User.query.filter_by(public_id=resp).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.public_id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def forget_password(data):
    user = User.query.filter(User.email == data['email'].lower()).first()
    if not user:
        response_object = {
            'status': 'fail',
            'code': 404,
            'message': 'User email is not exists.',
        }
        return response_object, 200

    token = generate_email_token(user=user,
                                 operation=Operations.RESET_PASSWORD)
    print(token)
    # send mail
    send_reset_pwd_mail(to=user.email, token=token)
    response_object = {
        'status': 'success',
        'message': 'reset password email is sent.',
    }
    return response_object, 200


def reset_password(data):
    user = User.query.filter(User.email == data['email'].lower()).first()
    if not user:
        response_object = {
            'status': 'fail',
            'code': 404,
            'message': 'User email is not exists.',
        }
        return response_object, 200

    res = validate_token(user=user,
                         token=data['token'],
                         operation=Operations.RESET_PASSWORD,
                         new_password=data['password'])
    print(res)
    if res[0]:
        response_object = {
            'status': 'success',
            'message': 'reset password success.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': res[1],
        }
        return response_object, 200


def get_user_wallet(user):
    return user.wallets.all()


def validate_user_wallet_data(data):
    user_id = data.get('user_id', None)
    zone_id = data.get('zone_id', None)
    currency_id = data.get('currency_id', None)
    address = data.get('address', None)

    user = User.query.filter_by(id=user_id).first()
    zone = ProposalZone.query.filter_by(id=zone_id).first()
    currency = Currency.query.filter_by(id=currency_id).first()

    if user == None:
        response_object = {
            'status': 'fail',
            'message': 'user is not exists.',
        }
        return response_object, False

    if zone == None:
        response_object = {
            'status': 'fail',
            'message': 'zone is not exists.',
        }
        return response_object, False

    if currency == None:
        response_object = {
            'status': 'fail',
            'message': 'currency is not exists.',
        }
        return response_object, False

    return {}, True


def add_user_wallet_addr(data):

    user_id = data.get('user_id', None)
    zone_id = data.get('zone_id', None)
    currency_id = data.get('currency_id', None)
    address = data.get('address', None)

    try:

        validate_res = validate_user_wallet_data(data)
        if validate_res[1] == False:
            return validate_res[0], 200

        wallet = Wallet.query.filter_by(zone_id=zone_id,
                                        user_id=user_id,
                                        currency_id=currency_id).first()

        # check exist same record
        if wallet:
            response_object = {
                'status': 'fail',
                'message': 'already exist same zone and currency record.',
            }
            return response_object, 200

        new_wallet = Wallet(
            user_id=user_id,
            zone_id=zone_id,
            currency_id=currency_id,
            address=address,
        )

        save_changes(new_wallet)

        response_object = {
            'status': 'success',
            'message': 'add user wallet success.',
        }
        return response_object, 200
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401


def update_user_wallet_addr(data):
    user_id = data.get('user_id', None)
    zone_id = data.get('zone_id', None)
    currency_id = data.get('currency_id', None)
    address = data.get('address', None)

    try:
        validate_res = validate_user_wallet_data(data)
        if validate_res[1] == False:
            return validate_res[0], 200

        wallet = Wallet.query.filter_by(zone_id=zone_id,
                                        user_id=user_id,
                                        currency_id=currency_id).first()

        # check exist wallet
        if wallet:
            # change address
            wallet.address = address
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'update user wallet success.',
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'same zone_id,currency_id wallet is not exist.',
            }
            return response_object, 200

    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401
