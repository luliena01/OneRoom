import os
from config import CONFIG
from flask import Flask, render_template
from flask_restful import Api, Resource
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)

app.secret_key = CONFIG['Security']['secret_key']

# Logger
#formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
file_handler = TimedRotatingFileHandler(os.path.join(CONFIG['Storage']['log'], 'one_room.log'), when='midnight', interval=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)


@app.route('/wp/main', methods=["GET"])
def main():
	return render_template('views/main.html')


from auth import auth, auth_wp, mail
app.register_blueprint(auth)
app.register_blueprint(auth_wp)

from boards.notice import notice, notice_wp
app.register_blueprint(notice)
app.register_blueprint(notice_wp)

mail.init_mail(app)

#  from auth.controller import login_required, admin_auth
# app.jinja_env.filters['login_required'] = login_required
# app.jinja_env.filters['is_admin'] = admin_auth

app.debug = CONFIG['Debug']

if __name__ == "__main__":
	#for debug
	import argparse

	parser = argparse.ArgumentParser(description='Development Server Help')
	parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
						help="run in debug mode (for use with PyCharm)", default=False)
	parser.add_argument("-p", "--port", dest="port",
						help="port of server (default:%(default)s)", type=int, default=5000)

	cmd_args = parser.parse_args()
	app_options = {"port": cmd_args.port}

	if cmd_args.debug_mode:
		app_options["debug"] = True
		app_options["use_debugger"] = False
		app_options["use_reloader"] = False

	app.run()
