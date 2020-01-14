
from app.main.exts import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from app.main.model.mixin import TimestampMixin
from ..config import key
import jwt

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    avatar = db.Column(db.String(255))
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    nickname = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    sign = db.Column(db.String(255))

    confirmed = db.Column(db.Boolean, default=False)


    # 注意，backref 不能跟 talename 重名
    proposals_created = db.relationship('Proposal',
                                    foreign_keys='Proposal.creator_id',
                                    backref='creator', lazy='dynamic')
    # 该用户创造的 comment
    comment_created = db.relationship('Comment',
                                    foreign_keys='Comment.creator_id',
                                    backref='creator', lazy='dynamic')

    # 该用户的 wallet
    wallets = db.relationship('UserWallet',
                                    foreign_keys='UserWallet.user_id',
                                    backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def set_password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class UserWallet(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_delete = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token_zone_id = db.Column(db.Integer, db.ForeignKey('proposal_zone.id'), nullable=False) # 对应 proposal zone id
    wallet_addr = db.Column(db.String(255), nullable=False) # wallet address