from flask import Blueprint
from flask_restful import Api, Resource

bill = Blueprint('bill', __name__, url_prefix='/bill')
bill_wp = Blueprint('bill_wp', __name__, url_prefix='/wp/bill')

api = Api(bill)

from . import controller
api.add_resource(controller.Month, '/month', '/month/<int:year>/<int:month>')
api.add_resource(controller.User, '/user')

from . import page
