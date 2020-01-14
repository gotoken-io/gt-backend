from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from app.main.util.flask_qiniu import Qiniu
from app.main.util.flask_s3 import S3Upload

db = SQLAlchemy()

flask_bcrypt = Bcrypt()


# qiniu_store = Qiniu()
s3_store = S3Upload()
