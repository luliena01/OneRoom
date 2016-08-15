from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy.sql.expression import desc, asc

from flask import current_app, session, jsonify
import datetime

from database import db_session
from utils import Response, Session
from bill import bill, fields
import models
import error_code


@bill.route('/monthlist', methods=["GET"])
def month_list():
	try:
		date_list = []
		for b in db_session.query(models.Bill.target_date).group_by(models.Bill.target_date).order_by(asc(models.Bill.target_date)).all():
			date_list.append({'year': '{:%Y}'.format(b[0]), 'month': '{:%m}'.format(b[0])})
			# year = '{:%Y}'.format(b[0])
			# month = '{:%m}'.format(b[0])
			#
			# if year not in date_list:
			# 	date_list[year] = [month]
			# else:
			# 	date_list[year].append(month)

		return jsonify(status=True, data=date_list)
	except Exception as e:
		current_app.logger.error(str(e))
		return jsonify(status=False, error='Unknown error')


class Month(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('bill', type=list, location='json', required=True)

	@marshal_with(Response.ok_field(fields.room))
	def get(self, year=None, month=None):
		try:
			if year is None or month is None:
				date = db_session.query(models.Bill.target_date).order_by(desc(models.Bill.target_date)).first()
			else:
				date = datetime.datetime(year, month, 1)

			bill = []
			for month_bill in db_session.query(models.Bill).filter(models.Bill.target_date == date).all():
				bill.append(
					{'date': '{:%Y %m}'.format(date), 'room': month_bill.room, 'electric': {'usage': month_bill.electric_usage, 'amount': month_bill.electric_amount},
					 'gas': {'usage': month_bill.gas_usage, 'amount': month_bill.gas_amount},
					 'description': month_bill.description})

			return Response.ok(bill)
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)

	def post(self, year, month):
		try:
			args = self.reqparse.parse_args()

			for bill in args['bill']:
				user = db_session.query(models.User.code).filter(models.User.room == bill['room']).one_or_none()

				user_bill = models.Bill(target_date=datetime.datetime(year, month, 1), room=bill['room'], author_id=user, electric_usage=bill['electric']['usage'],
										electric_amount=bill['electric']['amount'], gas_usage=bill['gas']['usage'], gas_amount=bill['gas']['amount'],
										description=bill['description'])
				db_session.add(user_bill)

			db_session.commit()
			return Response.ok()

		except Exception as e:
			db_session.rollback()
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)


class User(Resource):
	@marshal_with(Response.ok_field(fields.user))
	def get(self):
		try:
			user = session.get(Session.USER_SESSION)

			bill = []
			for target_date, electric_usage, electric_amount, gas_usage, gas_amount, description in db_session.query(models.Bill.target_date, models.Bill.electric_usage,
																													 models.Bill.electric_amount,
																													 models.Bill.gas_usage, models.Bill.gas_amount,
																													 models.Bill.description).filter(
						models.Bill.author_id == user).all():
				date = '{:%Y %m}'.format(target_date)
				bill.append({'date': date, 'electric': {'usage': electric_usage, 'amount': electric_amount}, 'gas': {'usage': gas_usage, 'amount': gas_amount},
							 'description': description})

				return Response.ok(bill)
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)
