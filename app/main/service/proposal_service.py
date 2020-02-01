import uuid
from app.main import db
from app.main.model import User, ProposalZone, Proposal, Currency, Category
from app.main.service.util import save_changes
from app.main.config import Config
from sqlalchemy import func

# def detect_user_exist(func):
#     def wrapper(data):
#         user = User.query.filter_by(id=data['creator_id']).first()
#         if not user:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'ceator_id is not exists.',
#             }
#             return response_object, 404
#     return wrapper


def get_all_proposal_zone():
    return ProposalZone.query.filter_by(is_delete=0).all()


def get_all_proposal(page=1):
    proposals = Proposal.query.filter_by(is_delete=0).paginate(
        page, Config.PROPOSAL_PER_PAGE, False)
    return proposals


def get_all_proposal_in_zone(zone_id, page=1):
    proposals_in_zone = Proposal.query.filter_by(
        zone_id=zone_id, is_delete=0).paginate(page, Config.PROPOSAL_PER_PAGE,
                                               False)
    return proposals_in_zone


def get_all_proposals_count_in_zone(zone_id):
    proposal_count = Proposal.query.filter_by(zone_id=zone_id,
                                              is_delete=0).count()
    return proposal_count


def get_a_proposal_zone(id):
    return ProposalZone.query.filter_by(id=id).first()


def get_a_proposal(id):
    return Proposal.query.filter_by(id=id).first()


def get_all_currency():
    return Currency.query.all()


# @detect_user_exist
def save_new_proposal_zone(data):

    proposal_zone = ProposalZone.query.filter_by(name=data['name']).first()
    if not proposal_zone:
        try:
            new_proposal_zone = ProposalZone(
                name=data['name'],
                token=data['token'],
                title=data['title'],
                summary=data['summary'],
                detail=data['detail'],
                theme_style=data['theme_style'],
                cover=data['cover'],
                vote_rule=data['vote_rule'],
                vote_addr_weight_json=data['vote_addr_weight_json'],
                creator_id=data['creator_id'],
            )
            save_changes(new_proposal_zone)
            response_object = {
                'status': 'success',
                'message': 'Successfully create a new proposal zone.',
            }
            return response_object, 201
        except Exception as e:
            response_object = {'status': 'fail', 'message': str(e)}
            return response_object, 400
    else:
        response_object = {
            'status': 'fail',
            'message': 'Proposal zone name already exists.',
        }
        return response_object, 409


# update proposal zone
def update_proposal_zone(id, data, user):
    proposal_zone = ProposalZone.query.filter_by(id=id).first()
    if not proposal_zone:
        response_object = {
            'status': 'fail',
            'message': 'Proposal zone id is not exists.',
        }
        return response_object, 404
    else:
        try:
            proposal_zone.name = data['name']
            proposal_zone.title = data['title']
            proposal_zone.token = data['token']
            proposal_zone.summary = data['summary']
            proposal_zone.detail = data['detail']
            proposal_zone.cover = data['cover']
            proposal_zone.theme_style = data['theme_style']
            proposal_zone.vote_rule = data['vote_rule']
            proposal_zone.vote_addr_weight_json = data['vote_addr_weight_json']

            # write to db
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully update a proposal zone.',
            }
            return response_object, 200
        except Exception as e:
            print(e)
            response_object = {'status': 'fail', 'message': str(e)}
            return response_object, 401


def save_new_proposal(data):

    # check 'zone_id' is exist or not
    proposal_zone = ProposalZone.query.filter_by(id=data['zone_id']).first()
    if not proposal_zone:
        response_object = {
            'status': 'fail',
            'message': 'relate zone_id is not exists.',
        }
        return response_object, 404

    # check 'category_id' is exist or not
    category = Category.query.filter_by(id=data['category_id']).first()
    if not category:
        response_object = {
            'status': 'fail',
            'message': 'relate category_id is not exists.',
        }
        return response_object, 404

    try:

        # 当前 zone 内的 proposal 数量
        zone_proposal_count = get_all_proposals_count_in_zone(data['zone_id'])

        # 新的 proposal zone id
        new_zone_proposal_id = zone_proposal_count + 1

        new_proposal = Proposal(
            zone_id=data['zone_id'],
            zone_proposal_id=new_zone_proposal_id,
            title=data['title'],
            categroy_id=data['category_id'],
            amount=data['amount'],
            summary=data['summary'],
            status=100,  # 创建成功，新创建的提案都是这个状态
            detail=data['detail'],
            creator_id=data['creator_id'],
            currency_id=data['currency_id'],
            tag=data['tag'],
        )

        save_changes(new_proposal)
        response_object = {
            'status': 'success',
            'message': 'Successfully create a new proposal.',
        }
        return response_object, 201
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401


# update proposal info
def update_proposal(id, data, user):

    # only creator, admin can udpate
    if (proposal.creator_id != user.id and user.admin != True):
        response_object = {
            'status': 'fail',
            'message': 'permission deny',
        }
        return response_object, 403

    # check update proposal.id is exist or not
    proposal = Proposal.query.filter_by(id=id).first()
    if not proposal:
        response_object = {
            'status': 'fail',
            'message': 'proposal is not exists.',
        }
        return response_object, 404

    # check 'category_id' is exist or not
    category = Category.query.filter_by(id=data['category_id']).first()
    if not category:
        response_object = {
            'status': 'fail',
            'message': 'relate category_id is not exists.',
        }
        return response_object, 404

    try:
        proposal.title = data['title']
        proposal.amount = data['amount']
        proposal.summary = data['summary']
        proposal.detail = data['detail']
        proposal.currency_id = data['currency_id']
        proposal.tag = data['tag']
        proposal.category_id = data['category_id']

        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully update proposal.',
        }
        return response_object, 200
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401


def delete_proposal(id, user):
    proposal = Proposal.query.filter_by(id=id).first()
    if not proposal:
        response_object = {
            'status': 'fail',
            'message': 'proposal is not exists.',
        }
        return response_object, 404
    if (proposal.creator_id != user.id and user.admin != True):
        response_object = {
            'status': 'fail',
            'message': 'permission deny',
        }
        return response_object, 403

    try:
        proposal.is_delete = 1
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully delete proposal.',
        }
        return response_object, 200
    except Exception as e:
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401


def delete_proposal_zone(id, user):
    proposal_zone = ProposalZone.query.filter_by(id=id).first()
    if not proposal_zone:
        response_object = {
            'status': 'fail',
            'message': 'proposal zone id is not exists.',
        }
        return response_object, 404
    if (user.admin != True):
        response_object = {
            'status': 'fail',
            'message': 'permission deny',
        }
        return response_object, 403

    try:
        proposal_zone.is_delete = 1
        # 该专区下所有 proposal 都被删除
        db.session.query(Proposal).filter(Proposal.zone_id == id).update(
            {Proposal.is_delete: 1})

        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully delete proposal zone and it`s proposal.',
        }
        return response_object, 200
    except Exception as e:
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401


# get all category
def get_all_category():
    return Category.query.filter_by(is_delete=0).all()


def validate_category_name(_name, _name_en, _id):
    if not _id:
        if Category.query.filter_by(name=_name).first():
            raise Exception("category name is exist.")

        if _name_en:
            if Category.query.filter_by(name_en=_name_en).first():
                raise Exception("category name_en is exist.")
    else:
        if Category.query.filter(Category.id != _id,
                                 Category.name == _name).first():
            raise Exception("category name is exist.")

        if _name_en:
            if Category.query.filter(Category.id != _id,
                                     Category.name_en == _name_en).first():
                raise Exception("category name_en is exist.")


# save a new category
def save_new_category(_name, _name_en, _order, _creator_id):

    if not _name:
        response_object = {
            'status': 'fail',
            'message': 'category name is required.',
        }
        return response_object, 404

    try:

        validate_category_name(_name, _name_en)

        category = Category(
            name=_name,
            name_en=_name_en,
            order=_order,
            creator_id=_creator_id,
        )

        save_changes(category)

        response_object = {
            'status': 'success',
            'message': 'Successfully add a new proposal category.',
        }
        return response_object, 200

    except Exception as e:
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401


def update_category(_id, _name, _name_en, _order):
    # check 'category_id' is exist or not
    category = Category.query.filter_by(id=_id).first()
    if not category:
        response_object = {
            'status': 'fail',
            'message': 'relate category.id is not exists.',
        }
        return response_object, 404

    try:
        validate_category_name(_name, _name_en, _id)

        category.name = _name
        category.name_en = _name_en
        category.order = _order

        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully update proposal category.',
        }
        return response_object, 200

    except Exception as e:
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401
