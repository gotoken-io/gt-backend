import uuid
from app.main import db
from app.main.model import User, ProposalZone, Proposal, Currency, Category, ProposalLog
from app.main.service.util import save_changes
from app.main.config import Config
from sqlalchemy import desc, asc
from app.main.util.proposal import ProposalStatus, ProposalLogEvent
from datetime import datetime

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


def create_proposal_log(proposal_id,
                        event_key,
                        op_user_id,
                        creator_id,
                        op_time=datetime.utcnow(),
                        from_value=None,
                        to_value=None):

    proposal = Proposal.query.filter_by(id=proposal_id).first()
    if proposal == None:
        raise Exception("proposal id is not exist.")

    new_proposal_log = ProposalLog(
        proposal_id=proposal_id,
        event=ProposalLogEvent[event_key].value,
        op_user_id=op_user_id,
        op_time=op_time,
        from_value=from_value,
        to_value=to_value,
        creator_id=creator_id,
    )

    save_changes(new_proposal_log)


# get all proposal logs by proposal id
def get_a_proposal_logs(proposal_id):
    return ProposalLog.query.filter_by(proposal_id=proposal_id).order_by(
        desc(ProposalLog.op_time)).all()


def get_all_proposal_zone():
    return ProposalZone.query.filter_by(is_delete=0).all()


def get_all_proposal(
    page=1,
    zone_id=None,
    category_id=None,
    status_key=None,  # proposal status key
    sort_name="createtime",
    sort_by="desc"):

    zone = None
    category = None
    status = None

    if status_key:
        if hasattr(ProposalStatus, status_key):
            status = ProposalStatus[status_key].value

    print(status)

    # default filter
    if status:
        get_proposals_filter = Proposal.query.filter_by(status=status,
                                                        is_delete=0)
    else:
        get_proposals_filter = Proposal.query.filter_by(is_delete=0)

    if zone_id:
        zone = ProposalZone.query.filter_by(id=zone_id).first()
    if category_id:
        # check 'category_id' is exist or not
        category = Category.query.filter_by(id=category_id).first()

    if zone:
        # default filter(get all proposals in zone id)
        if status:
            print(status)
            get_proposals_filter = Proposal.query.filter_by(zone_id=zone_id,
                                                            status=status,
                                                            is_delete=0)
        else:
            get_proposals_filter = Proposal.query.filter_by(zone_id=zone_id,
                                                            is_delete=0)
        if category:
            if status:
                get_proposals_filter = Proposal.query.filter_by(
                    status=status,
                    zone_id=zone_id,
                    category_id=category_id,
                    is_delete=0)
            else:
                get_proposals_filter = Proposal.query.filter_by(
                    zone_id=zone_id, category_id=category_id, is_delete=0)
    else:
        if category:

            if status:
                get_proposals_filter = Proposal.query.filter_by(
                    status=status, category_id=category_id, is_delete=0)
            else:
                get_proposals_filter = Proposal.query.filter_by(
                    category_id=category_id, is_delete=0)

    # default order filter
    order_filter = Proposal.created.desc()

    if sort_name == "createtime":
        if sort_by == "desc":
            order_filter = Proposal.created.desc()
        if sort_by == "asc":
            order_filter = Proposal.created.asc()

    if sort_name == "amount":
        if sort_by == "desc":
            order_filter = Proposal.amount.desc()
        if sort_by == "asc":
            order_filter = Proposal.amount.asc()

    if sort_name == "comments":
        if sort_by == "desc":
            order_filter = desc(Proposal.comments_count)
        if sort_by == "asc":
            order_filter = asc(Proposal.comments_count)

    proposals = get_proposals_filter.order_by(order_filter).paginate(
        page, Config.PROPOSAL_PER_PAGE, False)
    return proposals


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
                theme_style=data.get('theme_style', None),
                theme_color=data.get('theme_color', None),
                cover=data.get('cover', None),
                vote_rule=data['vote_rule'],
                vote_addr_weight_json=data['vote_addr_weight_json'],
                creator_id=data['creator_id'],
                vote_duration_hours_min=data.get('vote_duration_hours_min',
                                                 24),
                vote_duration_hours_max=data.get('vote_duration_hours_max',
                                                 120),
            )

            currency_ids = data.get('currency_ids', [])

            # add currency
            for c_id in currency_ids:
                currency = Currency.query.get(c_id)
                if currency is not None:
                    new_proposal_zone.currencies.append(currency)

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
            'code': 409
        }
        return response_object, 200


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
            # proposal_zone.token = data.get('token', None)
            proposal_zone.summary = data['summary']
            proposal_zone.detail = data['detail']
            proposal_zone.cover = data['cover']
            proposal_zone.theme_style = data.get('theme_style', None)
            proposal_zone.theme_color = data.get('theme_color', None)
            proposal_zone.vote_rule = data['vote_rule']
            proposal_zone.vote_addr_weight_json = data['vote_addr_weight_json']

            # vote duration
            proposal_zone.vote_duration_hours_min = data.get(
                'vote_duration_hours_min', 24)
            proposal_zone.vote_duration_hours_max = data.get(
                'vote_duration_hours_max', 120)

            # link currencies
            currency_ids = data.get('currency_ids', [])

            # clear currencies
            proposal_zone.currencies.clear()

            # add currency
            for c_id in currency_ids:
                currency = Currency.query.get(c_id)
                if currency is not None:
                    proposal_zone.currencies.append(currency)

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
            category_id=data['category_id'],
            amount=data['amount'],
            summary=data['summary'],
            status=100,  # 创建成功，新创建的提案都是这个状态
            detail=data['detail'],
            creator_id=data['creator_id'],
            currency_id=data['currency_id'],
            tag=data['tag'],
            estimated_hours=data.get('estimated_hours', 0),
            vote_duration_hours=data.get('vote_duration_hours', 0),
        )

        save_changes(new_proposal)

        # add proposal log, create
        create_proposal_log(new_proposal.id, 'create', new_proposal.creator_id,
                            new_proposal.creator_id)

        response_object = {
            'status': 'success',
            'data': new_proposal.id,
            'message': 'Successfully create a new proposal.',
        }
        return response_object, 201
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 400


# update proposal info
def update_proposal(id, data, user):
    # check update proposal.id is exist or not
    proposal = Proposal.query.filter_by(id=id).first()

    # only creator, admin can udpate
    if (proposal.creator_id != user.id and user.admin != True):
        response_object = {
            'status': 'fail',
            'message': 'permission deny',
        }
        return response_object, 403

    if not proposal:
        response_object = {
            'status': 'fail',
            'message': 'proposal is not exists.',
        }
        return response_object, 404

    # check 'category_id' is exist or not
    category_id = data.get('category_id')
    if category_id:
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
        proposal.category_id = category_id

        proposal.estimated_hours = data.get('estimated_hours', 0)

        db.session.commit()

        # add proposal log, update info
        create_proposal_log(proposal.id, 'update_info', proposal.creator_id,
                            proposal.creator_id)

        response_object = {
            'status': 'success',
            'message': 'Successfully update proposal.',
        }
        return response_object, 200
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 401


def add_proposal_progress(id, data, user):
    # check id is exist
    proposal = Proposal.query.filter_by(id=id).first()
    if not proposal:
        response_object = {
            'status': 'fail',
            'message': 'proposal is not exists.',
        }
        return response_object, 404

    # only creator, admin can udpate
    if (proposal.creator_id != user.id and user.admin != True):
        response_object = {
            'status': 'fail',
            'message': 'permission deny',
        }
        return response_object, 403

    try:
        progress_content = data.get(
            'progress_content')  # proposal progress content

        if progress_content == None:
            response_object = {
                'status': 'fail',
                'message': 'progress_content is required.',
            }
            return response_object, 200

        # add proposal log, update progress
        create_proposal_log(proposal_id=proposal.id,
                            event_key='update_progress',
                            op_user_id=proposal.creator_id,
                            creator_id=proposal.creator_id,
                            to_value=progress_content)

        response_object = {
            'status': 'success',
            'message': 'Successfully add a proposal progress.',
        }
        return response_object, 200
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 200


# update proposal status
def update_proposal_status(id, data, user):
    # check id is exist
    proposal = Proposal.query.filter_by(id=id).first()
    if not proposal:
        response_object = {
            'status': 'fail',
            'message': 'proposal is not exists.',
        }
        return response_object, 404

    # only admin can udpate status
    if (user.admin != True):
        response_object = {
            'status': 'fail',
            'message': 'permission deny',
        }
        return response_object, 403

    try:
        status_key = data.get('status_key', 'wait_to_vote')
        old_status_key = proposal.status
        proposal.status = ProposalStatus[status_key].value

        db.session.commit()

        # add proposal log, update status
        create_proposal_log(proposal_id=proposal.id,
                            event_key='update_status',
                            op_user_id=user.id,
                            creator_id=user.id,
                            from_value=old_status_key,
                            to_value=status_key)

        response_object = {
            'status': 'success',
            'message': 'Successfully update proposal status.',
        }
        return response_object, 200
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 200


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
    return Category.query.filter_by(is_delete=0).order_by(
        Category.order.desc()).all()


def validate_category_name(_name, _name_en, _id=None):
    if not _id:
        if Category.query.filter_by(name=_name).first():
            raise Exception("name is exist.")

        if _name_en:
            if Category.query.filter_by(name_en=_name_en).first():
                raise Exception("name_en is exist.")
    else:
        if Category.query.filter(Category.id != _id,
                                 Category.name == _name).first():
            raise Exception("name is exist.")

        if _name_en:
            if Category.query.filter(Category.id != _id,
                                     Category.name_en == _name_en).first():
                raise Exception("name_en is exist.")


# save a new category
def save_new_category(_name, _name_en, _order, _creator_id):

    if not _name:
        response_object = {
            'status': 'fail',
            'message': 'name is required.',
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
            'data': {
                'id': category.id,
                'name': category.name,
                'name_en': category.name_en,
            }
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


def delete_category(_id):
    # check 'category_id' is exist or not
    category = Category.query.filter_by(id=_id).first()
    if not category:
        response_object = {
            'status': 'fail',
            'message': 'relate category.id is not exists.',
        }
        return response_object, 404

    # this category has related proposals
    if len(category.proposals) > 0:

        class r_proposal:
            def __init__(self, id, title):
                self.id = id
                self.title = title

        related_proposals = []

        for p in category.proposals:
            related_proposals.append((p.id, p.title))

        response_object = {
            'status': 'fail',
            'message': 'this category.id exist relate proposal',
            'data': related_proposals
        }
        return response_object, 400

    # can delete this category
    category.is_delete = 1
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully delete proposal category.',
    }
    return response_object, 200