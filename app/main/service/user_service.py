import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.model.proposal import Proposal
from app.main.service.util import save_changes
from app.main.service.upload_service import delete_image
from app.main.service.util.uuid import version_uuid
from app.main.util.token import generate_email_token, validate_token
from app.main.settings import Operations
from app.main.util.mail import send_reset_pwd_mail

def save_new_user(data):
    user = User.query.filter((User.email==data['email'].lower()) | (User.username==data['username'])).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'].lower(),
            username=data['username'].lower(),
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
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

    if(data['nickname']):
        user.nickname = data['nickname']

    if(data['sign']):
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


def get_a_user(id):
    user = User.query.filter(User.id==id).first()
    created = Proposal.query.filter_by(creator_id=id, is_delete=0).all()
    user.proposals_created = created
    return user

# 还未使用
def get_a_user_proposal(id):
    created = Proposal.query.filter_by(creator_id=id, is_delete=0).all()

    response_object = {
            'status': 'success',
            'data': {
                'created':created,
            }
        }
    return response_object, 200

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
    user = User.query.filter(User.email==data['email'].lower()).first()
    if not user:
        response_object = {
            'status': 'fail',
            'code': 404,
            'message': 'User email is not exists.',
        }
        return response_object, 200

    token = generate_email_token(user=user, operation=Operations.RESET_PASSWORD)
    print(token)
    # send mail
    send_reset_pwd_mail(to=user.email, token=token)
    response_object = {
            'status': 'success',
            'message': 'reset password email is sent.',
    }
    return response_object, 200


def reset_password(data):
    user = User.query.filter(User.email==data['email'].lower()).first()
    if not user:
        response_object = {
            'status': 'fail',
            'code': 404,
            'message': 'User email is not exists.',
        }
        return response_object, 200

    res = validate_token(user=user, token=data['token'], operation=Operations.RESET_PASSWORD,
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