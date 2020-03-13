from app.main.exts import db
from app.main.model.mixin import BaseModelMixin, TimestampMixin
from app.main.model.user import User
from app.main.model.currency import Currency
from app.main.model.comment import Comment
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func, and_
from app.main.util.proposal import ProposalStatus, ProposalLogEvent
from datetime import datetime
from app.main.util.common import md5


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

    # 合约地址
    multiSigAddress = db.Column(db.String(100))
    voteAddress = db.Column(db.String(100))

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

    # 提案状态

    # 100 待投票: 创建后第一个状态,此时还未上链
    # 200 立项投票中: 上链成功, 在规定投票时间内进行链上投票
    # 300 申领中: 如果投票通过, 提案状态自动改变(投票结束时达成条件)
    # 400 投票未通过: 在规定投票时内, 没有达成通过条件, 状态自动改变
    # 以下是 status=300 后才会有的状态
    # 500 进行中: 由(专区)管理员修改到此状态
    # 600 验收中: 由(专区)管理员修改到此状态，此时需要进行多签投票,决定提案是否验收
    # 700 已完成: 如果投票通过, 提案状态自动改变(投票结束时达成条件)
    # 800 失败: 验收投票不通过, 提案状态自动改变(投票结束时达成条件)
    status = db.Column(db.Integer)

    # 是否已经上链
    # onchain = db.Column(db.Boolean, default=False)

    # 上链后的 hash
    onchain_hash = db.Column(db.String(500))

    # 预计工时
    estimated_hours = db.Column(db.Integer, nullable=True)

    # 投票开始时间, 默认是创建后马上开始
    vote_start_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 投票最大持续时间
    vote_duration_hours = db.Column(
        db.Integer, default=7200)  # vote default duration: 7200min=5day

    # 注意，backref 不能跟 talename 重名
    comments = db.relationship('Comment',
                               foreign_keys='Comment.proposal_id',
                               backref='link_proposal',
                               lazy='dynamic')

    logs = db.relationship('ProposalLog',
                           foreign_keys='ProposalLog.proposal_id',
                           backref='proposal',
                           lazy='dynamic')

    claims = db.relationship('ProposalClaim',
                             foreign_keys='ProposalClaim.proposal_id',
                             backref='proposal',
                             lazy='dynamic')

    def __repr__(self):
        return "<Proposal '{}'>".format(self.title)

    # 加上 @property 注解,表示这是一个属性字段
    # @property
    # def comments_count(self):
    #     return Comment.query.with_parent(self).filter_by(is_delete=0).count()

    def set_onchain_hash(self):
        self.onchain_hash = md5(
            str([
                self.id, self.title, self.summary, self.status,
                self.creator_id, self.created
            ]))

    @property
    def status_key(self):
        if self.status:
            return ProposalStatus(self.status).name

    @hybrid_property
    def comments_count(self):
        return self.comments.filter_by(is_delete=0).count()

    @comments_count.expression
    def comments_count(cls):
        return (select([func.count(Comment.id)]).where(
            and_(Comment.proposal_id == cls.id, Comment.is_delete == 0)))


class ProposalLog(BaseModelMixin, TimestampMixin, db.Model):
    """
    proposal log
    """

    __tablename__ = 'proposal_log'

    proposal_id = db.Column(db.Integer,
                            db.ForeignKey('proposal.id'),
                            nullable=False)

    event = db.Column(db.Integer)
    from_value = db.Column(db.Text, nullable=True)  # 操作前的值
    to_value = db.Column(db.Text, nullable=True)  # 操作后的值
    op_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    op_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def event_key(self):
        return ProposalLogEvent(self.event).name

    @property
    def operator(self):
        return User.query.filter_by(id=self.op_user_id).first()

    @property
    def creator(self):
        return User.query.filter_by(id=self.creator_id).first()
