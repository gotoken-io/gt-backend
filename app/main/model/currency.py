from app.main.exts import db


class Currency(db.Model):
    """
    Currency
    """
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    unit = db.Column(db.String(100), unique=True)
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    wallets = db.relationship('Wallet',
                              foreign_keys='Wallet.currency_id',
                              backref='currency',
                              lazy='dynamic')
