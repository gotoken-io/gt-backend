from app.main.exts import db
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime


class BaseModelMixin(object):
    """
    base model mixin
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    @declared_attr
    def creator_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

class TimestampMixin(object):
    """
    timestamp mixin
    """
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)