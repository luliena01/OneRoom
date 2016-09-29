from flask import current_app, request, make_response, session
from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc
from utils.GenerateUniqueId import generate_uuid
from database import db_session
import os
from config import CONFIG
from boards.info import fields
import models
from . import info
from auth.decorators import admin_auth, guest_auth
from utils import Response, image, Session

UPLOAD_PATH = os.path.join(CONFIG['Storage']['img']['path'], "info")


class Floor(Resource):
	@marshal_with(Response.ok_field(fields.floor))
	def get(self, floor):
		try:
			floor_info = []
			for room in db_session.query(models.Room).filter(models.Room.floor == floor).all():
				floor_info.append({'room': room.room, 'is_living': room.is_living, 'is_show': room.is_show, 'floor': room.floor, 'title': room.title, 'comment': room.comment})

			return Response.ok(floor_info)
		except Exception as e:
			current_app.logger.error(e)
			return Response.error()

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('floor', type=list, location='json', required=True)

		super(Floor, self).__init__()

	def post(self, floor):
		try:
			args = self.reqparse.parse_args()

			for roomInfo in args['floor']:
				room = db_session.query(models.Room).filter(models.Room.room == roomInfo['room']).one()

				room.is_show = roomInfo['is_show']
			db_session.commit()

			return Response.ok()
		except Exception as e:
			current_app.logger.error(e)
			return Response.error()


class Room(Resource):
	@marshal_with(Response.ok_field(fields.room))
	def get(self, room):
		try:
			room_info = []
			for room in db_session.query(models.Room).filter(models.Room.room == room).all():
				room_info.append(
					{'room': room.room, 'is_living': room.is_living, 'is_show': room.is_show, 'floor': room.floor, 'title': room.title, 'comment': room.comment, 'info': room.info,
					 'content': room.content})

			return Response.ok(room_info)
		except Exception as e:
			current_app.logger.error(e)
			return Response.error()

	@admin_auth
	def post(self):
		try:
			# parser = fields.get_notice_parser().copy()
			args = self.reqparse.parse_args()

			room = args['room']
			content = args['content']

			room = models.Room(room=room, content=content)

			db_session.add(room)
			db_session.commit()

			return Response.ok()
		except Exception as e:
			current_app.logger.error(e)
			return Response.error()


@info.route('/file/<file_no>/', methods=['GET'])
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


@info.route('/file/', methods=["POST"])
@admin_auth
def file_update():
	header = request.headers
	# filename = header["file-name"]
	# filesize = header["file-size"]
	# filetype = header["file-Type"]

	file_no = generate_uuid()

	url = 'sFileURL=/info/file/' + file_no

	# need to check file's extention
	# if it is not allowed file, url += 'errstr=NOTALLOW'
	try:
		file = request.get_data()
		if file:
			if not os.path.exists(UPLOAD_PATH):
				os.mkdir(UPLOAD_PATH)

			# f = open(os.path.join(UPLOAD_PATH, file_no), 'wb')
			# f.write(file)
			# f.close()
			#
			# print('save file : ' + file_no)
			#
			# image.resize(os.path.join(UPLOAD_PATH, file_no))

			image.save_img(file, os.path.join(UPLOAD_PATH, file_no))

			current_app.logger.info('Save info img file : ' + file_no)
	except Exception as e:
		current_app.logger.error(e)
		url = "&errstr=NOTALLOW"

	return url