import uuid
from datetime import datetime
from flask import json
from app.main import db
from app.main.model import User, Comment, Proposal
from app.main.service.util import save_changes


def save_new_comment(data):
    # 判断 comment 关联的 proposal.id 是否存在
    proposal = Proposal.query.filter_by(id=data['proposal_id']).first()
    if not proposal:
        response_object = {
            'status': 'fail',
            'message': 'relate proposal_id is not exists.',
        }
        return response_object, 404

    try:
        if 'parent_id' in data:
            new_comment = Comment(
                proposal_id=data['proposal_id'],
                text=data['text'],
                creator_id=data['creator_id'],
                parent_id=data['parent_id'],
            )
        else:
            # reply
            new_comment = Comment(
                proposal_id=data['proposal_id'],
                text=data['text'],
                creator_id=data['creator_id'],
            )

        save_changes(new_comment)
        response_object = {
            'status': 'success',
            'message': 'Successfully create a new comment.',
            'data': {
                'id': new_comment.id,
                'created': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
            },
        }
        return response_object, 201
    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 400


def update_comment(data):
    # 判断 comment.id 是否存在
    comment = Comment.query.filter_by(id=data['id']).first()
    if not comment:
        response_object = {
            'status': 'fail',
            'message': 'comment id is not exists.',
        }
        return response_object, 404

    try:
        comment.text = data['text']
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully update a new comment.',
        }
        return response_object, 200

    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 400


def delete_comment(id, user):
    # 判断 comment.id 是否存在
    comment = Comment.query.filter_by(id=id).first()
    if not comment:
        response_object = {
            'status': 'fail',
            'message': 'comment id is not exists.',
        }
        return response_object, 404

    # only creator and admin can delete
    if user.id != comment.creator_id and user.admin != 1:
        response_object = {
            'status': 'fail',
            'message': 'no permission.',
        }
        return response_object, 403

    try:
        comment.is_delete = 1
        # 批量'删除'该条评论下关联的所有回复
        db.session.query(Comment).filter(
            Comment.parent_id == comment.id).update({Comment.is_delete: 1})
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully delete comment.',
        }
        return response_object, 200

    except Exception as e:
        print(e)
        response_object = {'status': 'fail', 'message': str(e)}
        return response_object, 400


def get_proposal_comments(proposal_id):
    return Comment.query.filter_by(proposal_id=proposal_id,
                                   is_delete=0,
                                   parent_id=None).order_by(
                                       Comment.created.desc()).all()
