from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from app.main.service.user_service import get_a_user_by_auth_token

from app.main.util.dto.proposal_claim_dto import proposal_claim, api
from app.main.service.proposal_claim_service import claim_proposal

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
            return claim_proposal(data=post_data, user_id=user.id)