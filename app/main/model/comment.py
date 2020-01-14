from app.main.exts import db
from app.main.model.mixin import BaseModelMixin, TimestampMixin
from app.main.model.user import User
from datetime import datetime

class Comment(BaseModelMixin, TimestampMixin, db.Model):
    """
    Comment
    """

    __tablename__ = 'comment'

    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'))
    text = db.Column(db.String(500))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    replies = db.relationship(
        "Comment", backref=db.backref("parent", remote_side="Comment.id"), lazy="dynamic"
    )

    def creator(self):
        return User.query.filter(creator=self).first()
