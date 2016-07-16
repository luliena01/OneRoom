from flask import current_app
from flask_mail import Mail
from flask_mail import Message
from config import CONFIG

mail = Mail()


def init_mail(app):
	# mail = Mail(app)
	mail.init_app(app)


def make_confirm_email(email, url):
	try:
		if CONFIG['Email_confirm']['enable'] is not True:
			return

		msg = Message("Please, confirm your email.", sender=CONFIG['Email_confirm']['sender'], recipients=email)
		msg.body = "Please, confirm your email through this url : " + url
		mail.send(msg)

		current_app.logger.info("Send confirm email to new user (" + email + ") : ", str(msg))
	except Exception as e:
		current_app.logger.error(str(e))
