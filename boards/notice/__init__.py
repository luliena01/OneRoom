from flask import Blueprint
from flask_restful import Api, Resource

notice = Blueprint('notice', __name__, url_prefix='/notice')
notice_wp = Blueprint('notice_wp', __name__, url_prefix='/wp/notice')

api = Api(notice)

from . import controller
api.add_resource(controller.List, '/list', '/list/<int:page>')
api.add_resource(controller.Content, '/content', '/content/<int:index>')

from . import page
