from flask import current_app, session, redirect
from functools import wraps
from sqlalchemy.orm import joinedload
from passlib.hash import sha256_crypt
from database import db_session
from utils import Session
import models


def guest_auth(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		if Session.LOGIN_SESSION in session:
			if verify_login(session.get(Session.USER_SESSION), session.get(Session.LOGIN_SESSION)):
				return func(*args, **kwargs)
			else:
				return redirect('/wp/auth/login')
		else:
			# flash("You need to login.")
			return redirect('/wp/auth/login')

	return wrap


def admin_auth(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		if not verify_login(session.get(Session.USER_SESSION), session.get(Session.LOGIN_SESSION)):
			return redirect('/wp/auth/login')

		if Session.LOGIN_SESSION in session:
			if is_admin(session.get(Session.USER_SESSION)):
				return func(*args, **kwargs)
		else:
			# flash("You are not administrator.")
			return redirect('/wp/auth/login')

	return wrap


def tenant_auth(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		if not verify_login(session.get(Session.USER_SESSION), session.get(Session.LOGIN_SESSION)):
			return redirect('/wp/auth/login')

		if Session.LOGIN_SESSION in session:
			if is_tenant(session.get(Session.USER_SESSION)) or is_admin(session.get(Session.USER_SESSION)):
				return func(*args, **kwargs)
		else:
			# flash("You are not administrator.")
			return redirect('/wp/auth/login')

	return wrap


def verify_login(code, verify_data):
	try:
		if code is None or verify_data is None:
			return False
		user = db_session.query(models.User).filter(models.User.code == code).first()
		if user is None:
			return False
		return sha256_crypt.verify(code + user.password_hash, verify_data)
	except Exception as e:
		current_app.logger.error(str(e))
		return False


def is_admin(code):
	try:
		user = db_session.query(models.User).filter(models.User.code == code).first()
		if user is not None and user.role_id == 1:
			return True
		else:
			return False
	except Exception as e:
		current_app.logger.error(str(e))
		return False


def is_tenant(code):
	try:
		user = db_session.query(models.User).options(joinedload(models.User.room_info)).filter(models.User.code == code).first()
		if user is not None and user.role_id == 2 and user.room_info is not None and user.room_info.is_living is True:
			return True
		else:
			return False
	except Exception as e:
		current_app.logger.error(str(e))
		return False
