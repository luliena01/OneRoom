from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy.sql.expression import desc, asc
from sqlalchemy.orm import joinedload

from flask import current_app, session, redirect
from passlib.hash import sha256_crypt
from utils.GenerateUniqueId import generate_uuid
from datetime import datetime
from . import auth

from database import db_session
import models
import error_code
from utils import Response, Session

from auth import fields, mail, decorators
from auth.decorators import admin_auth


class Login(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('id', type=str)
		self.reqparse.add_argument('password', type=str)

		super(Login, self).__init__()

	# login, sign in
	def post(self):
		try:
			args = self.reqparse.parse_args()

			email = args['id']
			query = db_session.query(models.User).filter(models.User.email == email)
			user = query.one_or_none()

			if user is None:
				# return {'status': 'error', 'code': error_code.Login.NOT_FOUND_ID, 'message': error_code.Login.NOT_FOUND_ID.message()}
				return Response.error(error_code.Login.NOT_FOUND_ID)

			if not sha256_crypt.verify(str(args['password']), user.password_hash):
				# return {'status': 'error', 'code': error_code.Login.WRONG_PASSWORD, 'message': error_code.Login.WRONG_PASSWORD.message()}
				return Response.error(error_code.Login.WRONG_PASSWORD)

			if user.confirmed is False:
				return Response.error(error_code.Login.NOT_CONFORMED)

			user.last_seen = datetime.now()
			db_session.commit()

			session.clear()
			session[Session.LOGIN_SESSION] = sha256_crypt.encrypt(str(user.code + user.password_hash))
			session[Session.USER_SESSION] = user.code
			session[Session.ADMIN_SESSION] = decorators.is_admin(user.code)

			current_app.logger.info("Login - " + email)

			return Response.ok()
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)

		# class Logout(Resource):
		# login, sign in


@auth.route('/logout', methods=['GET'])
def get():
	try:
		session.clear()
		# gc.collect()
		return redirect('/wp/auth/login')
	except Exception as e:
		current_app.logger.error(str(e))
		return redirect('/wp/auth/login')


class User(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('email', type=str)
		self.reqparse.add_argument('password', type=str)
		self.reqparse.add_argument('confirmed', type=bool)
		self.reqparse.add_argument('user_name', type=str)
		self.reqparse.add_argument('role', type=str)
		self.reqparse.add_argument('room', type=str)
		self.reqparse.add_argument('phone', type=str)

		super(User, self).__init__()

	@admin_auth
	# @marshal_with(Response.ok_field(fields.user))
	# def get(self):
	# 	try:
	# 		list = db_session.query(models.User).options(joinedload(models.User.role)).options(joinedload(models.User.room_info)).order_by(asc(models.User.email)).all()
	#
	# 		return Response.ok(list)
	# 	except Exception as e:
	# 		current_app.logger.error(str(e))
	# 		return Response.error(error_code.Global.UNKOWN)

	@marshal_with(Response.ok_field(fields.user))
	def get(self, code=None):
		try:
			if code is None:
				#check admin auth
				list = db_session.query(models.User).options(joinedload(models.User.role)).options(joinedload(models.User.room_info)).order_by(asc(models.User.email)).all()

				return Response.ok(list)
			else:
				user = db_session.query(models.User).options(joinedload(models.User.role)).options(joinedload(models.User.room_info)).filter(models.User.code == code).one()

				return Response.ok(user)
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)

	# sign up
	def post(self):
		try:
			args = self.reqparse.parse_args()

			email = args['email']
			query = db_session.query(models.User).filter(models.User.email == email)
			user = query.one_or_none()

			if user is not None:
				current_app.logger.warning("Already register id : " + email)
				return Response.error(error_code.Login.ALREADY_REGISTER)

			new_user = models.User(code=generate_uuid(), email=email, password_hash=sha256_crypt.encrypt(str(args['password'])), user_name=args['user_name'], role_id=args['role'],
								   room=args['room'], phone=args['phone'])
			db_session.add(new_user)
			db_session.commit()

			current_app.logger.info("Register new user : " + email)

			# generate confirm emain
			url = "/auth/confirm/" + generate_uuid()

			confirm = models.Confirm(email=email, type=models.Confirm_type.CONFIRM_REGISTER.name, url=url)
			db_session.add(confirm)
			db_session.commit()

			mail.make_confirm_email(email, url)

			return Response.ok()

		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)

	@marshal_with(Response.ok_field(fields.user))
	def put(self, code):
		try:
			args = self.reqparse.parse_args()

			user = db_session.query(models.User).options(joinedload(models.User.role)).options(joinedload(models.User.room_info)).filter(models.User.code == code).one()

			if args['password'] is not None:
				user.password_hash = sha256_crypt.encrypt(str(args['password']))
			if args['confirmed'] is not None:
				user.confirmed = args['confirmed']
			if args['user_name'] is not None:
				user.user_name = args['user_name']
			if args['phone'] is not None:
				user.phone = args['phone']

			db_session.commit()

			return Response.ok(user)
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)

	def delete(self, code):
		try:
			db_session.query(models.User).filter(models.User.code == code).delete()

			return Response.ok()
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)


class Room(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('room', type=str)
		self.reqparse.add_argument('is_living', type=bool, required=True)

		super(Room, self).__init__()

	@marshal_with(Response.ok_field(fields.room))
	def get(self):
		room_list = []
		try:
			for room, is_living in db_session.query(models.Room.room, models.Room.is_living).order_by(desc(models.Room.room)):
				room_list.append({'room': room, 'is_living': is_living})

			return Response.ok(room_list)
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)

	@marshal_with(Response.ok_field(fields.room))
	def put(self, code):
		try:
			args = self.reqparse.parse_args()

			room = db_session.query(models.Room).options(joinedload(models.Room.user)).filter(models.Room.room == args['room'] and models.User.code == code).one()

			room.is_living = args['is_living']
			db_session.commit()

			return Response.ok(room)
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)


class Role(Resource):
	@marshal_with(Response.ok_field(fields.role))
	def get(self):
		role_list = []
		try:
			for id, name in db_session.query(models.Role.id, models.Role.name).order_by(desc(models.Role.id)):
				role_list.append({'id': id, 'name': name})

			# return role_list
			return Response.ok(role_list)
		except Exception as e:
			current_app.logger.error(str(e))
			return Response.error(error_code.Global.UNKOWN)
