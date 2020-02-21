from app.main.exts import db
from app.main.model.mixin import BaseModelMixin, TimestampMixin
from app.main.model.currency import Currency
from app.main.model.user import User
from app.main.model.proposal import Proposal
from app.main.util.proposal_claim import ProposalClaimStatus


class ProposalClaim(BaseModelMixin, TimestampMixin, db.Model):
    __tablename__ = "proposal_claim"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    proposal_id = db.Column(db.Integer,
                            db.ForeignKey('proposal.id'),
                            primary_key=True)

    # 申领状态
    # 100 申领中
    # 200 申领通过
    # 300 申领不通过
    # 400 撤销申领
    status = db.Column(db.Integer,
                       default=ProposalClaimStatus['claiming'].value)

    # 申领理由
    reason = db.Column(db.Text)

    budget_amount = db.Column(db.DECIMAL, default=0.0)
    budget_currency_id = db.Column(db.Integer,
                                   db.ForeignKey('currency.id'),
                                   nullable=True)

    # 收款地址
    payment_address = db.Column(db.String(255), nullable=True)
