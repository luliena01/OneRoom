from . import auth_wp
from flask import render_template


@auth_wp.route('/login', methods=["GET"])
def login():
	return render_template('views/auth/login.html')


@auth_wp.route('/register', methods=["GET"])
def register():
	return render_template('views/auth/register.html')


@auth_wp.route('/user/list', methods=["GET"])
def user_list():
	return render_template('views/auth/list.html')
