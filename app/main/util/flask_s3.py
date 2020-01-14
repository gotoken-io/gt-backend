import boto3

class S3Upload(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        S3_KEY = app.config.get('S3_KEY', '')
        S3_SECRET = app.config.get('S3_SECRET', '')

        self.bucket_name = app.config.get('S3_BUCKET', '')
        self.url_prefix = app.config.get('S3_URL_PREFIX')
        self.s3_reource = boto3.resource(
                's3',
                aws_access_key_id=S3_KEY,
                aws_secret_access_key=S3_SECRET
            )

    def get_bucket(self):
        return self.s3_reource.Bucket(self.bucket_name)

    def get_s3_config(self):
        return {
            'bucket': self.bucket_name,
            'url_prefix': self.url_prefix
        }