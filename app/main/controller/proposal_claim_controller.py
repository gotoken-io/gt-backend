from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from app.main.service.user_service import get_a_user_by_auth_token

from app.main.util.dto.proposal_claim_dto import proposal_claim, api, page_of_proposal_claim, proposal_claim_team
import app.main.service.proposal_claim_service as proposal_claim_service

api_proposal_claim = api
add_team = proposal_claim_team

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


@api_proposal_claim.route('/user/<username>')
class UserProposalClaimAPI(Resource):
    """
        User Proposals Claim Resource
    """
    @api_proposal_claim.doc('get a user claim proposals')
    @api_proposal_claim.marshal_with(page_of_proposal_claim, envelope='data')
    def get(self, username):
        page = int(request.args.get("page", 1))
        return proposal_claim_service.get_user_claims_username(
            username=username, page=page)


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


@api_proposal_claim.route('/result')
class SubmitProposalClaimAPI(Resource):
    """
        Submit Proposals Claim result
    """
    @api_proposal_claim.doc('submit the proposal claim result')
    @token_required
    def post(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        return proposal_claim_service.submit_claim_result(data=post_data,
                                                          user_id=user.id)


@api_proposal_claim.route('/verify/result')
class VerifyProposalClaimResultAPI(Resource):
    """
        Verify Proposals Claim Result
    """
    @api_proposal_claim.doc('verify a proposal claim result')
    @admin_token_required
    def put(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        claim_id = post_data.get('claim_id')
        approve = post_data.get('approve', True)

        return proposal_claim_service.verify_claim_result(claim_id=claim_id,
                                                          user_id=user.id,
                                                          approve=approve)


@api_proposal_claim.route('/verify')
class VerifyProposalClaimAPI(Resource):
    """
        Verify Proposals Claim Resource
    """
    @api_proposal_claim.doc('verify a proposal claim')
    @admin_token_required
    def put(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        claim_id = post_data.get('claim_id')
        approve = post_data.get('approve', True)

        return proposal_claim_service.verify_claim(claim_id=claim_id,
                                                   user_id=user.id,
                                                   approve=approve)
# proposal zone api
@api_proposal_claim.route('/team')
class ProposalClaimAPI(Resource):
    """
        Proposal Claim Resource
    """
    @api_proposal_claim.doc('Add a team member')
    @api_proposal_claim.expect(add_team, validate=False)
    @token_required
    def post(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return proposal_claim_service.add_team(data=post_data,
                                                   owner_id=user.id)

    @api.doc('delete team_member')
    def delete(self):
        id = request.json['id']
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)
        if user:
            return proposal_claim_service.delete_team(id, user)
