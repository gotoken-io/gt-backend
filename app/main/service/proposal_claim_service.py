import uuid
from app.main import db
from app.main.model import User, Proposal, Currency, ProposalLog, ProposalClaim
from app.main.service.util import save_changes
from app.main.config import Config
from sqlalchemy import desc, asc
from app.main.util.proposal import ProposalStatus, ProposalLogEvent
from app.main.util.proposal_claim import ProposalClaimStatus
from datetime import datetime


# claim proposal
def claim_proposal(data, user_id):

    # check post data.proposal_id required
    proposal_id = data.get('proposal_id')
    if not proposal_id:
        response_object = {
            'status': 'fail',
            'message': 'proposal_id is required.',
        }
        return response_object, 200

    # check post data.reason required
    reason = data.get('reason')
    if not reason:
        response_object = {
            'status': 'fail',
            'message': 'reason is required.',
        }
        return response_object, 200

    # check proposal
    proposal = Proposal.query.filter_by(id=proposal_id).first()
    if not proposal:
        response_object = {
            'status': 'fail',
            'message': 'proposal is not exists.',
        }
        return response_object, 200

    # check user
    user = User.query.filter_by(id=user_id).first()
    if not user:
        response_object = {
            'status': 'fail',
            'message': 'user is not exists.',
        }
        return response_object, 200

    # check user claim this proposal before?
    for claim in user.claims:
        if claim.proposal_id == proposal_id:
            response_object = {
                'status': 'fail',
                'message': 'user already claim this proposal',
            }
            return response_object, 200

    new_claim_proposal = ProposalClaim(
        user_id=user_id,
        creator_id=user_id,
        proposal_id=proposal.id,
        status=ProposalClaimStatus['claiming'].value,
        reason=reason,
        budget_amount=data.get('budget_amount'),
        budget_currency_id=data.get('budget_currency_id'),
        payment_address=data.get('payment_address'),
    )

    save_changes(new_claim_proposal)
    response_object = {
        'status': 'success',
        'message': 'Successfully claim a proposal.',
        'data': {
            'claim_id': new_claim_proposal.claim_id,
        }
    }
    return response_object, 201
