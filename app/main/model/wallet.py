from app.main.exts import db
from app.main.model.mixin import BaseModelMixin, TimestampMixin
from app.main.model.currency import Currency
from app.main.model.user import User
from app.main.model.proposal import ProposalZone


class Wallet(BaseModelMixin, TimestampMixin, db.Model):
    __tablename__ = "wallet"
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # is_delete = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    zone_id = db.Column(db.Integer,
                        db.ForeignKey('proposal_zone.id'),
                        primary_key=True)  # 对应 proposal zone id
    currency_id = db.Column(db.Integer,
                            db.ForeignKey('currency.id'),
                            primary_key=True)
    address = db.Column(db.String(255), nullable=True)  # wallet address
