from flask_restful import fields, reqparse


def ok_field(data_type=None):
	if not data_type:
		data_type = {}

	res = {
		'status': fields.Boolean,
		'data': fields.Nested(data_type, allow_null=True)
	}
	return res


def ok(data=None):
	return {'status': True, 'data': data}


def error_field():
	res = {
		'status': fields.Boolean,
		'error': fields.Nested(error_message)
	}
	return res


def error(code, url=None):
	return {'status': False, 'error': {"code": code.name, "message": code.message(), "redirect": url}}


error_message = {
	"code": fields.String,
	"message": fields.String,
	"redirect": fields.String
}
