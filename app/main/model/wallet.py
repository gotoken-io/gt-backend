from app.main.exts import db
from app.main.model.mixin import BaseModelMixin, TimestampMixin
from app.main.model.currency import Currency
from app.main.model.user import User
from app.main.model.proposal import ProposalZone
from web3.auto import w3
from eth_account.messages import encode_defunct


class Wallet(BaseModelMixin, TimestampMixin, db.Model):
    __tablename__ = "wallet"
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # is_delete = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    zone_id = db.Column(db.Integer,
                        db.ForeignKey('proposal_zone.id'),
                        primary_key=True)  # 对应 proposal zone id
    currency_id = db.Column(db.Integer,
                            db.ForeignKey('currency.id'),
                            primary_key=True)
    address = db.Column(db.String(255), nullable=True)  # wallet address

    @staticmethod
    def getNonce(wallet):
        """
        Gives a nonce for a wallet
        :param wallet:
        :return: string
        """
        return "THIS_IS_FIX_NONCE"

    @staticmethod
    def recover_address(data: str, signature: str) -> str:
        message = encode_defunct(text=data)
        return w3.eth.account.recover_message(message, signature=signature)

    @staticmethod
    def checkNonce(wallet, signature):
        """
        Check the nonce validity
        :param wallet:
        :return: string
        """
        result = Wallet.recover_address(Wallet.getNonce(wallet), signature)
        print(wallet.address, result)

        return result == wallet.address
