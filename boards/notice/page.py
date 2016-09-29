from . import notice_wp
from flask import render_template
from auth.decorators import guest_auth, admin_auth


@notice_wp.route('/list', methods=["GET"])
def list():
    return render_template('views/board/notice/list.html')


@notice_wp.route('/content', methods=["GET"])
@admin_auth
def content():
	return render_template('views/board/notice/content.html')
