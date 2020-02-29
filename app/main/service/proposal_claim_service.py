import uuid
from app.main import db
from app.main.model import User, Proposal, Currency, ProposalLog, ProposalClaim
from app.main.service.util import save_changes
from app.main.config import Config
from sqlalchemy import desc, asc
from app.main.util.proposal import ProposalStatus, ProposalLogEvent
from app.main.util.proposal_claim import ProposalClaimStatus
from app.main.service.proposal_service import create_proposal_log
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
    proposal_claim = ProposalClaim.query.filter_by(proposal_id=proposal_id,
                                                   user_id=user_id).first()
    if proposal_claim:
        # if proposal_claim.status_key == 'claiming':
        #     response_object = {
        #         'status': 'fail',
        #         'message': 'user already claim this proposal',
        #     }
        #     return response_object, 200

        # if proposal_claim.status_key == 'cancel':

        # claim same proposal again.
        proposal_claim.status = ProposalClaimStatus['claiming'].value
        proposal_claim.reason = reason

        db.session.commit()

        # create proposal log, proposal_claim_claiming
        create_proposal_log(proposal_id=proposal_id,
                            event_key='proposal_claim_claiming',
                            op_user_id=user_id,
                            creator_id=user_id,
                            to_value=user_id)

        response_object = {
            'status': 'success',
            'message': 'user claim this proposal again.',
        }

        return response_object, 200

    try:
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

        # create proposal log, proposal_claim_claiming
        create_proposal_log(proposal_id=new_claim_proposal.proposal_id,
                            event_key='proposal_claim_claiming',
                            op_user_id=user_id,
                            creator_id=user_id,
                            to_value=user_id)

        response_object = {
            'status': 'success',
            'message': 'Successfully claim a proposal.',
            'data': {
                'claim_id': new_claim_proposal.claim_id,
            }
        }

        return response_object, 201
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 200


# cancel claim proposal
# only claimer can cancel his proposal claim
def cancel_claim_proposal(data, user_id):
    # check post data.proposal_id required
    proposal_id = data.get('proposal_id')
    if not proposal_id:
        response_object = {
            'status': 'fail',
            'message': 'proposal_id is required.',
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

    try:
        proposal_claim = ProposalClaim.query.filter_by(
            proposal_id=proposal_id, user_id=user_id).first()
        if not proposal_claim:
            response_object = {
                'status': 'fail',
                'message': 'proposal claim record is not exists.',
            }
            return response_object, 200

        proposal_claim.status = ProposalClaimStatus['cancel'].value
        db.session.commit()

        # create proposal log, proposal_claim_cancel
        create_proposal_log(proposal_id=proposal_claim.proposal_id,
                            event_key='proposal_claim_cancel',
                            op_user_id=user_id,
                            creator_id=user_id,
                            to_value=proposal_claim.claimer.id)

        response_object = {
            'status': 'success',
            'message': 'proposal claim cancel success.',
        }
        return response_object, 200

    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 200


# admin approve or fail claim
def verify_claim(claim_id, user_id, approve=True):
    proposal_claim = ProposalClaim.query.filter_by(claim_id=claim_id).first()

    if not proposal_claim:
        response_object = {
            'status': 'fail',
            'message': 'proposal claim is not exists.',
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

    if not user.admin:
        response_object = {
            'status': 'fail',
            'message': 'permission deny.',
        }
        return response_object, 200

    status_key = 'passed'
    log_event_key = 'proposal_claim_passed'

    if not approve:
        status_key = 'fail'
        log_event_key = 'proposal_claim_fail'

    proposal_claim.status = ProposalClaimStatus[status_key].value
    db.session.commit()

    # create proposal log, proposal_claim_passed/proposal_claim_fail
    create_proposal_log(proposal_id=proposal_claim.proposal_id,
                        event_key=log_event_key,
                        op_user_id=user_id,
                        creator_id=user_id,
                        to_value=proposal_claim.claimer.username)

    response_object = {
        'status': 'success',
        'message': 'proposal claim status set {} success.'.format(status_key),
    }
    return response_object, 200


# claimer submit result
def submit_claim_result(data, user_id):
    claim_id = data.get('claim_id')
    if not claim_id:
        response_object = {
            'status': 'fail',
            'message': 'claim_id is required.',
        }
        return response_object, 200

    proposal_claim = ProposalClaim.query.filter_by(claim_id=claim_id).first()

    if not proposal_claim:
        response_object = {
            'status': 'fail',
            'message': 'proposal claim is not exists.',
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

    # check user_id is claimer.id
    if user_id != proposal_claim.claimer.id:
        response_object = {
            'status': 'fail',
            'message': 'user is not claimer.',
        }
        return response_object, 200

    result = data.get('result')
    if not result:
        response_object = {
            'status': 'fail',
            'message': 'result is required.',
        }
        return response_object, 200

    proposal_claim.result = result
    proposal_claim.status = ProposalClaimStatus['submit_result'].value
    db.session.commit()

    # create proposal log, proposal_claim_passed/proposal_claim_fail
    create_proposal_log(proposal_id=proposal_claim.proposal_id,
                        event_key='proposal_claim_result_submit',
                        op_user_id=user_id,
                        creator_id=user_id)

    response_object = {
        'status': 'success',
        'message': 'proposal claim result submit success',
    }

    return response_object, 200


def verify_claim_result(claim_id, user_id, approve=True):
    proposal_claim = ProposalClaim.query.filter_by(claim_id=claim_id).first()

    if not proposal_claim:
        response_object = {
            'status': 'fail',
            'message': 'proposal claim is not exists.',
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

    if not user.admin:
        response_object = {
            'status': 'fail',
            'message': 'permission deny.',
        }
        return response_object, 200

    status_key = 'result_approve'
    log_event_key = 'proposal_claim_result_approve'

    if not approve:
        status_key = 'result_fail'
        log_event_key = 'proposal_claim_result_fail'

    proposal_claim.status = ProposalClaimStatus[status_key].value
    db.session.commit()

    # create proposal log, verify proposal claim result
    create_proposal_log(proposal_id=proposal_claim.proposal_id,
                        event_key=log_event_key,
                        op_user_id=user_id,
                        creator_id=user_id,
                        to_value=proposal_claim.claimer.username)

    response_object = {
        'status': 'success',
        'message': 'proposal claim status set {} success.'.format(status_key),
    }
    return response_object, 200


def get_user_claims_username(username, page):

    # check user
    user = User.query.filter_by(username=username).first()
    if not user:
        print('user is not exists.')
        # response_object = {
        #     'status': 'fail',
        #     'message': 'user is not exists.',
        # }
        return None

    user_claims = ProposalClaim.query.filter_by(
        user_id=user.id, is_delete=0).paginate(page, Config.PROPOSAL_PER_PAGE,
                                               False)

    return user_claims


def get_proposal_claims(proposal_id):
    # check proposal
    proposal = Proposal.query.filter_by(id=proposal_id).first()
    if not proposal:
        response_object = {
            'status': 'fail',
            'message': 'proposal is not exists.',
        }
        return response_object, 200

    proposal_claims = ProposalClaim.query.filter_by(
        proposal_id=proposal_id).all()
    return proposal_claims