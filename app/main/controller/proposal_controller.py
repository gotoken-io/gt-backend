from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from app.main.service import proposal_service
from app.main.service.comment_service import get_proposal_comments
from app.main.service.user_service import get_a_user_by_auth_token

import app.main.util.dto.proposal_dto as proposal_dto
import app.main.util.dto.proposal_zone_dto as proposal_zone_dto
import app.main.util.dto.currency_dto as currency_dto
from app.main.util.dto import comment_dto

# rename proposal_service function
save_new_proposal_zone = proposal_service.save_new_proposal_zone
get_all_proposal_zone = proposal_service.get_all_proposal_zone
save_new_proposal = proposal_service.save_new_proposal
get_all_proposal= proposal_service.get_all_proposal
get_all_proposal_in_zone=proposal_service.get_all_proposal_in_zone

get_a_proposal = proposal_service.get_a_proposal
get_a_proposal_zone = proposal_service.get_a_proposal_zone
get_all_currency = proposal_service.get_all_currency
update_proposal = proposal_service.update_proposal
update_proposal_zone = proposal_service.update_proposal_zone
delete_proposal=proposal_service.delete_proposal
delete_proposal_zone=proposal_service.delete_proposal_zone

# proposal zone dto
api_proposal_zone = proposal_zone_dto.api
proposal_zone = proposal_zone_dto.proposal_zone

# proposal zone api
@api_proposal_zone.route('/')
class ProposalZoneAPI(Resource):
    """
        Proposal Zone Resource
    """
    @api_proposal_zone.doc('create new proposal zone')
    @api_proposal_zone.expect(proposal_zone, validate=False)
    @admin_token_required
    def post(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)
        
        if user:
            post_data['creator_id']=user.id
            return save_new_proposal_zone(data=post_data)

    @api_proposal_zone.doc('get all proposal zones')
    @api_proposal_zone.marshal_list_with(proposal_zone, envelope='data')
    def get(self):
        return get_all_proposal_zone()

@api_proposal_zone.route('/<id>')
@api_proposal_zone.param('id', 'Proposal  zone id')
@api_proposal_zone.response(404, 'Proposal zone not found.')
class ProposalZoneSingleAPI(Resource):
    """
        Proposal Zone Single Resource
    """
    @api_proposal_zone.doc('get a proposal zone')
    @api_proposal_zone.marshal_with(proposal_zone, envelope='data')
    def get(self, id):
        """get a proposal zone given its id"""
        proposal_zone = get_a_proposal_zone(id)
        if not proposal_zone:
            # print('404')
            api_proposal_zone.abort(404)
        else:
            return proposal_zone
    
    @api_proposal_zone.doc('update proposal zone')
    @api_proposal_zone.expect(proposal_zone)
    @admin_token_required
    def put(self, id):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return update_proposal_zone(id=id, data=post_data, user=user)

    @api_proposal_zone.doc('delete proposal zone')
    @admin_token_required
    def delete(self, id):
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return delete_proposal_zone(id=id, user=user)


# proposal dto
api_proposal = proposal_dto.api
proposal = proposal_dto.proposal
proposal_post = proposal_dto.proposal_post
proposal_put = proposal_dto.proposal_put

# proposal api
@api_proposal.route('/')
class ProposalAPI(Resource):
    """
        Proposal Resource
    """
    @api_proposal.doc('create new proposal')
    @api_proposal.expect(proposal_post)
    @token_required
    def post(self):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        print(user)
        
        if user:
            post_data['creator_id']=user.id
            return save_new_proposal(data=post_data)



    @api_proposal.doc('get all proposal')
    @api_proposal.marshal_list_with(proposal, envelope='data')
    def get(self):
        zone_id = request.args.get("zone_id")
        if(zone_id):
            return get_all_proposal_in_zone(zone_id)
        else:
            return get_all_proposal()  

@api_proposal.route('/<id>')
@api_proposal.param('id', 'Proposal id')
@api_proposal.response(404, 'Proposal not found.')
class ProposalSingleAPI(Resource):
    @api_proposal.doc('get a proposal')
    @api_proposal.marshal_with(proposal, envelope='data')
    def get(self, id):
        """get a proposal given its id"""
        proposal = get_a_proposal(id)
        if not proposal:
            # print('404')
            api_proposal.abort(404)
        else:
            return proposal

    @api_proposal.doc('update proposal')
    @api_proposal.expect(proposal_post)
    @token_required
    def put(self, id):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return update_proposal(id=id, data=post_data, user=user)

    @api_proposal.doc('delete proposal')
    @admin_token_required
    def delete(self, id):
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return delete_proposal(id=id, user=user)

# proposal comment api

api_comment = comment_dto.api
comment_get_list = comment_dto.comment_get_list

@api_proposal.route('/comment/<id>')
@api_proposal.param('id', 'Proposal id')
@api_proposal.response(404, 'Proposal not found.')
class CommentAPI(Resource):
    """
        Proposal Comment Resource
    """
    @api_proposal.doc('get proposal comment')
    @api_proposal.marshal_with(comment_get_list, envelope='data')
    def get(self, id):
        """get a proposal given its id"""
        proposal = get_a_proposal(id)
        if not proposal:
            # print('404')
            api_proposal.abort(404)
        else:
            comments = get_proposal_comments(id)
            return comments


# currency dto
api_currency = currency_dto.api
currency = currency_dto.currency

# proposal api
@api_currency.route('/')
class CurrencyAPI(Resource):
    """
        Currency Resource
    """
    @api_currency.doc('get all currency')
    @api_currency.marshal_list_with(currency, envelope='data')
    def get(self):
        return get_all_currency()  
