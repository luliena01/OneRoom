from flask import Blueprint
from flask_restful import Api, Resource

info = Blueprint('info', __name__, url_prefix='/info')
info_wp = Blueprint('info_wp', __name__, url_prefix='/wp/info')

api = Api(info)

from . import controller
api.add_resource(controller.Floor, '/floor/<string:floor>')
api.add_resource(controller.Room, '/room/<string:room>')

from . import page
