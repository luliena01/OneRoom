from flask_restful import fields

floor = {
	'room': fields.String,
	'is_living': fields.Boolean,
	'is_show': fields.Boolean,
	'floor': fields.String,
	'title': fields.String,
	'comment': fields.String
}

room = {
	'room': fields.String,
	'is_living': fields.Boolean,
	'is_show': fields.Boolean,
	'floor': fields.Integer,
	'title': fields.String,
	'comment': fields.String,
	'info': fields.String,
	'content': fields.String
}
