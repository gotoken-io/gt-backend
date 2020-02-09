from app.main.exts import db
from app.main.model.mixin import BaseModelMixin, TimestampMixin
from app.main.model.user import User
from app.main.model.currency import Currency
from app.main.model.comment import Comment
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func, and_


class Category(BaseModelMixin, TimestampMixin, db.Model):
    """
    Proposal Category
    """

    name = db.Column(db.String(200), unique=True)  # chinese name
    name_en = db.Column(db.String(200), unique=True,
                        nullable=True)  # english name

    order = db.Column(db.Integer, default=0)  # use for order category list
    proposals = db.relationship('Proposal', backref='category')

    @property
    def proposals_count(self):
        # return len(self.proposals)
        return Proposal.query.filter_by(category_id=self.id,
                                        is_delete=0).count()


class ProposalZone(BaseModelMixin, TimestampMixin, db.Model):
    """
    Proposal Zone
    """
    __tablename__ = 'proposal_zone'

    name = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(100))
    token = db.Column(db.String(100))  # token name
    summary = db.Column(db.String(200))
    detail = db.Column(db.Text)
    vote_rule = db.Column(db.Text)
    cover = db.Column(db.String(100))  # proposal cover image filename

    # 专区主题
    # proposal theme style css: {'background':'#ccc', 'color':'#fff'}
    theme_style = db.Column(db.Text)

    # 专区主题色
    theme_color = db.Column(db.Text)

    # 投票最小持续时间
    vote_duration_hours_min = db.Column(db.Integer,
                                        default=1)  # vote min duration: 1h

    # 投票最大持续时间
    vote_duration_hours_max = db.Column(
        db.Integer, default=120)  # vote min duration: 120h=5day

    vote_addr_weight_json = db.Column(db.Text)

    # 该专区下的提案
    proposals = db.relationship('Proposal',
                                foreign_keys='Proposal.zone_id',
                                backref='zone',
                                lazy='dynamic')

    # 该专区支持的代币
    currencies = db.relationship('Currency',
                                 secondary='zone_currency',
                                 backref="zones")

    # 绑定了该专区的用户钱包
    wallets = db.relationship('Wallet',
                              foreign_keys='Wallet.zone_id',
                              backref="zone",
                              lazy='dynamic')

    def __repr__(self):
        return "<Proposal Zone '{}'>".format(self.name)


# 专区与支持代币多对多关系
class ProposalZone_Currency(BaseModelMixin, TimestampMixin, db.Model):
    """
    Proposal zone - currency relations
    """
    __tablename__ = 'zone_currency'

    zone_id = db.Column(db.Integer,
                        db.ForeignKey('proposal_zone.id'),
                        primary_key=True)
    currency_id = db.Column(db.Integer,
                            db.ForeignKey('currency.id'),
                            primary_key=True)


class Proposal(BaseModelMixin, TimestampMixin, db.Model):
    """
    Proposal
    """

    __tablename__ = 'proposal'

    zone_id = db.Column(db.Integer, db.ForeignKey('proposal_zone.id'))
    zone_proposal_id = db.Column(
        db.Integer)  # 该 proposal 在某专区内的 ID, 以在该专区内的 ID 为自增
    title = db.Column(db.String(200))
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'),
                            nullable=True)
    tag = db.Column(db.String(200))
    amount = db.Column(db.DECIMAL)

    # 前端上,只能选择该专区支持的代币
    currency_id = db.Column(db.Integer,
                            db.ForeignKey('currency.id'),
                            nullable=True)
    summary = db.Column(db.String(200))
    detail = db.Column(db.Text)
    status = db.Column(db.Integer)

    # 预计工时
    estimated_hours = db.Column(db.Integer, nullable=True)

    # 投票最大持续时间
    vote_duration_hours = db.Column(
        db.Integer, default=7200)  # vote default duration: 7200min=5day

    # 注意，backref 不能跟 talename 重名
    comments = db.relationship('Comment',
                               foreign_keys='Comment.proposal_id',
                               backref='link_proposal',
                               lazy='dynamic')

    def __repr__(self):
        return "<Proposal '{}'>".format(self.title)

    def zone(self):
        return ProposalZone.query.filter(zone=self).first()

    def creator(self):
        return User.query.filter(creator=self).first()

    def currency_unit(self):
        return Currency.query.filter(currency_unit=self).first()

    # 加上 @property 注解,表示这是一个属性字段
    # @property
    # def comments_count(self):
    #     return Comment.query.with_parent(self).filter_by(is_delete=0).count()

    @hybrid_property
    def comments_count(self):
        return self.comments.filter_by(is_delete=0).count()

    @comments_count.expression
    def comments_count(cls):
        return (select([func.count(Comment.id)]).where(
            and_(Comment.proposal_id == cls.id, Comment.is_delete == 0)))
