from flask import Flask

from .config import config_by_name
from app.main.exts import db, flask_bcrypt, s3_store


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    flask_bcrypt.init_app(app)
    # init aws s3 store
    s3_store.init_app(app)

    return app