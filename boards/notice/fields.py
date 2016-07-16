from flask_restful import fields, reqparse

notice = {
	'index': fields.String,
	'title': fields.String,
	'content': fields.String,
	'counter': fields.Integer(default=0),
	'register_date': fields.DateTime(dt_format='rfc822'),
	'author_id': fields.String
}

paging = {
	# paging
	'page': fields.Integer(default=0),
	'per_page': fields.Integer(default=20),
	'total_count': fields.Integer(default=0)
}

notice_list = {
	'notice': fields.List(fields.Nested(notice, allow_null=True)),
	'paging': fields.Nested(paging),
}
