import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__)) # app/main

APP_ROOT = os.path.join(os.path.dirname(__file__), '../..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'gotkengogogo')
    DEBUG = False

    # qiniu config
    # QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
    # QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
    # QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME')
    # QINIU_BUCKET_DOMAIN = os.getenv('QINIU_BUCKET_DOMAIN')

    # s3 config
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_KEY = os.getenv("S3_KEY")
    S3_SECRET = os.getenv("S3_SECRET_ACCESS_KEY")
    S3_URL_PREFIX = os.getenv("S3_URL_PREFIX")

    # GT config
    GT_DOMAIN = os.getenv('GT_DOMAIN', 'https://gotoken.io')



class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'gt_dev.db')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'gt_test.db')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = 'https://gotoken.io'


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
