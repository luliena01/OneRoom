from flask_restful import fields, reqparse
from passlib.hash import sha256_crypt

room = {
	'room': fields.String,
	'is_living': fields.Boolean
}

role = {
	'id': fields.Integer,
	'name': fields.String
}

user = {
	'code': fields.String,
	'email': fields.String,
	'user_name': fields.String,
	'confirmed': fields.Boolean,
	'role': fields.Nested(role),
	'room_info': fields.Nested(room, allow_null=True),
	'phone': fields.String,
	'member_since': fields.DateTime(dt_format='iso8601'),
	'last_seen': fields.DateTime(dt_format='iso8601')
}

user_list = {
	"list": fields.List(fields.Nested(user))
}
