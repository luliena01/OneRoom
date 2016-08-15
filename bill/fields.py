from flask_restful import fields, reqparse

bill = {
	'usage': fields.Integer,
	'amount': fields.Integer
}

room = {
	'date': fields.String,
	'room': fields.String,
	'electric': fields.Nested(bill),
	'gas': fields.Nested(bill),
	'description': fields.String
}

user = {
	'date': fields.String,
	'electric': fields.Nested(bill),
	'gas': fields.Nested(bill),
	'description': fields.String
}

