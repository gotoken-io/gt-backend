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
get_all_proposal = proposal_service.get_all_proposal

get_a_proposal = proposal_service.get_a_proposal
get_a_proposal_zone = proposal_service.get_a_proposal_zone
get_all_currency = proposal_service.get_all_currency
update_proposal = proposal_service.update_proposal
update_proposal_zone = proposal_service.update_proposal_zone
delete_proposal = proposal_service.delete_proposal
delete_proposal_zone = proposal_service.delete_proposal_zone

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
            post_data['creator_id'] = user.id
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
page_of_proposals = proposal_dto.page_of_proposals
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
            post_data['creator_id'] = user.id
            return save_new_proposal(data=post_data)

    @api_proposal.doc('get all proposal')
    @api_proposal.marshal_with(page_of_proposals, envelope='data')
    def get(self):
        zone_id = request.args.get("zone_id")
        category_id = request.args.get("category_id")
        page = int(request.args.get("page", 1))
        sort_name = request.args.get("sort_name", "createtime")
        sort_by = request.args.get("sort_by", "desc")
        status_key = request.args.get("status_key")

        return get_all_proposal(zone_id=zone_id,
                                page=page,
                                category_id=category_id,
                                status_key=status_key,
                                sort_name=sort_name,
                                sort_by=sort_by)


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


@api_proposal.route('/<id>/status')
@api_proposal.param('id', 'Proposal id')
@api_proposal.response(404, 'Proposal not found.')
class ProposalStatusAPI(Resource):
    @api_proposal.doc('update proposal status')
    @api_proposal.expect(proposal_post)
    @admin_token_required
    def put(self, id):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return proposal_service.update_proposal_status(id=id,
                                                           data=post_data,
                                                           user=user)


@api_proposal.route('/<id>/log')
@api_proposal.param('id', 'Proposal id')
@api_proposal.response(404, 'Proposal not found.')
class ProposalLogAPI(Resource):
    @api_proposal.doc('get proposal logs')
    @api_proposal.marshal_list_with(proposal_dto.proposal_log, envelope='data')
    def get(self, id):
        return proposal_service.get_a_proposal_logs(proposal_id=id)


@api_proposal.route('/<id>/progress')
@api_proposal.param('id', 'Proposal id')
@api_proposal.response(404, 'Proposal not found.')
class ProposalProgressAPI(Resource):
    @api_proposal.doc('add proposal progress')
    @token_required
    def post(self, id):
        # get the post data
        post_data = request.json
        # get auth token
        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)

        if user:
            return proposal_service.add_proposal_progress(id=id,
                                                          data=post_data,
                                                          user=user)


@api_proposal.route('/category')
class ProposalCategoryAPI(Resource):
    @api_proposal.doc('get all proposal categories')
    @api_proposal.marshal_list_with(proposal_dto.proposal_category,
                                    envelope='data')
    def get(self):
        all_categories = proposal_service.get_all_category()
        return all_categories

    @api_proposal.doc('add a new proposal category')
    @admin_token_required
    def post(self):
        post_data = request.json

        auth_token = request.headers.get('Authorization')
        user = get_a_user_by_auth_token(auth_token)
        if user:
            creator_id = user.id

        name = post_data.get('name')
        name_en = post_data.get('name_en', name)
        order = post_data.get('order', 0)

        return proposal_service.save_new_category(name, name_en, order,
                                                  creator_id)

    @api_proposal.doc('update a proposal category')
    @admin_token_required
    def put(self):
        post_data = request.json

        id = post_data.get('id')
        name = post_data.get('name')
        name_en = post_data.get('name_en')
        order = post_data.get('order', 0)

        return proposal_service.update_category(id, name, name_en, order)

    @api_proposal.doc('delete a proposal category')
    @admin_token_required
    def delete(self):
        post_data = request.json

        id = post_data.get('id')

        return proposal_service.delete_category(id)


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
