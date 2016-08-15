from . import bill_wp
from flask import render_template


@bill_wp.route('/', methods=["GET"])
@bill_wp.route('/bills', methods=["GET"])
def user():
	return render_template('views/bill/bills.html')


@bill_wp.route('/manage', methods=["GET"])
def monthly():
	return render_template('views/bill/manage.html')
