
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.main.settings import Operations
from app.main.model.user import User
from app.main import db
from app.main.config import key as secret_key

# expire_in: 过期时间，单位s
def generate_email_token(user, operation, expire_in=300, **kwargs):
    s = Serializer(secret_key, expire_in)

    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data).decode("utf-8") 


def validate_token(user, token, operation, new_password=None):
    s = Serializer(secret_key)

    try:
        data = s.loads(token)
    except SignatureExpired:
        # 过期
        return False, 'SignatureExpired'
    except BadSignature:
        # 验证错误
        return False, 'BadSignature'

    # 二次验证
    if operation != data.get('operation') or user.id != data.get('id'):
        return False, 'DoubleCheckError'

    if operation == Operations.CONFIRM:
        user.confirmed = True , 'success'
    elif operation == Operations.RESET_PASSWORD:
        user.set_password(new_password) # 会自动把 password 明文加密
    elif operation == Operations.CHANGE_EMAIL:
        new_email = data.get('new_email')
        if new_email is None:
            return False , 'new_email not set'
        if User.query.filter_by(email=new_email).first() is not None:
            return False, 'new_email is already exist'
        user.email = new_email
    else:
        return False, 'Operations not found'

    db.session.commit()
    return True, 'success'