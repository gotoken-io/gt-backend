from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from app.main.service.user_service import get_a_user_by_auth_token

from app.main.util.dto.proposal_claim_dto import proposal_claim, api
import app.main.service.proposal_claim_service as proposal_claim_service

api_proposal_claim = api


# proposal zone api
@api_proposal_claim.route('/')
class ProposalClaimAPI(Resource):
    """
        Proposal Claim Resource
    """
    @api_proposal_claim.doc('claim a proposal')
    @token_required
    def post(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return proposal_claim_service.claim_proposal(data=post_data,
                                                         user_id=user.id)

    @api_proposal_claim.doc('cancel claim a proposal')
    @token_required
    def put(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return proposal_claim_service.cancel_claim_proposal(
                data=post_data, user_id=user.id)


@api_proposal_claim.route('/user/<user_id>')
@api_proposal_claim.param('user_id', 'user id')
class UserProposalClaimAPI(Resource):
    """
        User Proposals Claim Resource
    """
    @api_proposal_claim.doc('get a user claim proposals')
    @api_proposal_claim.marshal_list_with(proposal_claim, envelope='data')
    def get(self, user_id):
        return proposal_claim_service.get_user_claims(user_id=user_id)


@api_proposal_claim.route('/proposal/<proposal_id>')
@api_proposal_claim.param('proposal_id', 'proposal id')
class ProposalClaimsAPI(Resource):
    """
        User Proposals Claim Resource
    """
    @api_proposal_claim.doc('get a user claim proposals')
    @api_proposal_claim.marshal_list_with(proposal_claim, envelope='data')
    def get(self, proposal_id):
        return proposal_claim_service.get_proposal_claims(
            proposal_id=proposal_id)
