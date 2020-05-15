from app.main.exts import db
from app.main.model.mixin import BaseModelMixin, TimestampMixin
from app.main.model.currency import Currency
from app.main.model.user import User
from app.main.model.proposal import Proposal
from app.main.util.proposal_claim import ProposalClaimStatus
from app.main.util.common import uuid4


class ProposalClaimTeam(BaseModelMixin, TimestampMixin, db.Model):
    __tablename__ = "proposal_claim_team"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey(
        'proposal_claim.id'))
    responsibility = db.Column(db.Text)
    # TODO refactor that in flask dto

    def user(self):
        return User.query.filter_by(id=self.user_id)
