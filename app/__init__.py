from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.proposal_controller import api_proposal_zone as proposal_zone_ns, api_proposal as proposal_ns, api_currency
from app.main.controller.comment_controller import api as comment_ns
from app.main.controller.upload_controller import api as upload_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(proposal_zone_ns)
api.add_namespace(proposal_ns)
api.add_namespace(api_currency)
api.add_namespace(comment_ns)
api.add_namespace(upload_ns)