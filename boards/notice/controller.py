from flask import current_app, session, request, make_response
from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc
from database import db_session
import os
from config import CONFIG
from models import Notice, User
from utils.GenerateUniqueId import generate_uuid
from boards.notice import fields
from . import notice
from auth.decorators import admin_auth, guest_auth
from utils import Response

UPLOAD_PATH = os.path.join(CONFIG['Storage']['img'], "notice")
PER_PAGE = CONFIG['Page']['max_content']
NOTICE_BOARD = "NOTICE"


class List(Resource):
	@marshal_with(Response.ok_field(fields.notice_list))
	def get(self, page=1):
		count = db_session.query(Notice).count()

		if count == 0:
			pagination = {'page': page, 'per_page': PER_PAGE, 'total_count': count}
			return {'paging': pagination}

		# boardList = db_session.query(Notice).options(joinedload(User)).order_by(desc(Notice.index))[(page - 1) * PER_PAGE: page * PER_PAGE]
		boardList = []
		for index, title, counter, registerDate, user_name in db_session.query(Notice.index, Notice.title, Notice.counter, Notice.register_date, User.user_name). \
																	  join(User, Notice.author_id == User.code).order_by(desc(Notice.index))[
															  (page - 1) * PER_PAGE: page * PER_PAGE]:
			boardList.append({'index': index, 'title': title, 'author_id': user_name, 'counter': counter, 'register_date': registerDate})

		pagination = {'page': page, 'per_page': PER_PAGE, 'total_count': count}
		return Response.ok({'notice': boardList, 'paging': pagination})


class Content(Resource):
	@marshal_with(Response.ok_field(fields.notice))
	def get(self, index):
		notice = db_session.query(Notice).filter(Notice.index == index).one()

		# add counter
		session_notice = session.get(NOTICE_BOARD)
		if session_notice is None or str(index) not in session_notice:
			notice.counter += 1
			db_session.commit()
			if session_notice is None:
				session[NOTICE_BOARD] = {str(index): True}
			else:
				session_notice[str(index)] = True

		return Response.ok(notice)


	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type=str)
		self.reqparse.add_argument('content', type=str)

		super(Content, self).__init__()

	@admin_auth
	def post(self):
		try:
			# parser = fields.get_notice_parser().copy()
			args = self.reqparse.parse_args()

			title = args['title']
			content = args['content']
			email = session.get('email')

			#get json from request BUT title and content is null when they was inserted
			user = db_session.query(User.email).filter(User.email == email).one()
			new_notice = Notice(title=title, content=content, author_id=user)

			db_session.add(new_notice)
			db_session.commit()

			return Response.ok()
		except Exception as e:
			current_app.logger.error(e)
			return {'message': "error"}

	@admin_auth
	def put(self, index):
		try:
			# parser = fields.get_notice_parser()
			# args = parser.parse_args()
			args = self.reqparse.parse_args()

			notice = db_session.query(Notice).filter(Notice.index == index).one()
			notice.author_id = db_session.query(User.email).filter(User.email == session.get('email')).one()
			notice.title = args['title']
			notice.content = args['content']

			db_session.commit()

			return Response.ok()
		except Exception as e:
			current_app.logger.error(e)
			return {'message': e}

	@guest_auth
	def delete(self, index):
		try:
			db_session.query(Notice).filter(Notice.index == index).delete()

			return Response.ok()
		except Exception as e:
			current_app.logger.error(e)
			return {'message': e}


@notice.route('/file/<file_no>/', methods=['GET'])
@admin_auth
def get_file(file_no):
	try:
		file = open(os.path.join(UPLOAD_PATH, file_no), 'rb')
		content = file.read()
		response = make_response(content)
		response.headers["Content-Disposition"] = "attachment; filename=" + file_no
		return response
	except Exception as e:
		current_app.logger.error(e)


@notice.route('/file/', methods=["POST"])
@admin_auth
def file_update():
	header = request.headers
	filename = header["file-name"]
	filesize = header["file-size"]
	filetype = header["file-Type"]

	file_no = generate_uuid()

	url = 'sFileURL=/notice/file/' + file_no

	# need to check file's extention
	# if it is not allowed file, url += 'errstr=NOTALLOW'
	try:
		file = request.get_data()
		if file:
			if not os.path.exists(UPLOAD_PATH):
				os.mkdir(UPLOAD_PATH)

			f = open(os.path.join(UPLOAD_PATH, file_no), 'wb')
			f.write(file)
			f.close()

			current_app.logger.info('Save Notice img file : ' + file_no)
	except Exception as e:
		current_app.logger.error(e)
		url = "&errstr=NOTALLOW"

	return url
