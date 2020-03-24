from app.main.exts import db
from app.main.model.mixin import BaseModelMixin, TimestampMixin
from app.main.model.currency import Currency
from app.main.model.user import User
from app.main.model.proposal import Proposal
from app.main.util.proposal_claim import ProposalClaimStatus
from app.main.util.common import uuid4
from app.main.model.proposal_claim_team import ProposalClaimTeam


class ProposalClaim(BaseModelMixin, TimestampMixin, db.Model):
    __tablename__ = "proposal_claim"

    claim_id = db.Column(db.String(200), nullable=False, default=uuid4)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    proposal_id = db.Column(db.Integer,
                            db.ForeignKey('proposal.id'),
                            primary_key=True)

    # 申领状态
    # 100 申领中
    # 200 申领通过
    # 300 申领不通过
    # 400 撤销申领
    # 500 提交结果中
    # 600 结果通过
    # 700 结果不通过
    status = db.Column(db.Integer,
                       default=ProposalClaimStatus['claiming'].value)

    # 申领理由
    reason = db.Column(db.Text)
    plan = db.Column(db.Text)

    budget_amount = db.Column(db.DECIMAL, nullable=True)
    budget_currency_id = db.Column(db.Integer,
                                   db.ForeignKey('currency.id'),
                                   nullable=True)

    # 收款地址
    payment_address = db.Column(db.String(255), nullable=True)

    # 完成结果
    result = db.Column(db.Text, nullable=True)

    # team = db.relationship('ProposalClaimTeam',
    #                        foreign_keys='ProposalClaimTeam.team_id',
    #                        backref='team',
    #                        lazy='dynamic')

    @property
    def status_key(self):
        if self.status:
            return ProposalClaimStatus(self.status).name

    @property
    def team(self):
        return ProposalClaimTeam.query.filter_by(team_id=self.id)

    # @property
    # def creator(self):
    #     return User.query.filter_by(id=self.creator_id).first()
