from flask import Blueprint
from flask_restful import Api, Resource

auth = Blueprint('auth', __name__, url_prefix='/auth')
auth_wp = Blueprint('auth_wp', __name__, url_prefix='/wp/auth')

api = Api(auth)

from . import controller

api.add_resource(controller.Login, '/login')
# api.add_resource(controller.Logout, '/logout')
api.add_resource(controller.User, '/user', '/user/<string:code>')
api.add_resource(controller.Room, '/room', '/room/<string:code>')
api.add_resource(controller.Role, '/role')

from . import page
