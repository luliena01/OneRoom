from . import info_wp
from flask import render_template
from auth.decorators import guest_auth, admin_auth


@info_wp.route('/list', methods=["GET"])
def list():
	return render_template('views/board/info/list.html')


@info_wp.route('/edit', methods=["GET"])
@admin_auth
def content():
	return render_template('views/board/info/edit.html')
