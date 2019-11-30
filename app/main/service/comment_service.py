import uuid
import datetime
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
        new_comment = Comment(
            proposal_id=data['proposal_id'],
            text=data['text'],
            creator_id=data['creator_id'],
            # parent_id=data['parent_id'],
        )

        save_changes(new_comment)
        response_object = {
            'status': 'success',
            'message': 'Successfully create a new comment.',
        }
        return response_object, 201
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
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
        db.session.comment()
        
        response_object = {
            'status': 'success',
            'message': 'Successfully create a new comment.',
        }
        return response_object, 200

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return response_object, 400
