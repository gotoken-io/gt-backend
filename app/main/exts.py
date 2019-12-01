from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.main.util.flask_qiniu import Qiniu

db = SQLAlchemy()

flask_bcrypt = Bcrypt()


qiniu_store = Qiniu()
