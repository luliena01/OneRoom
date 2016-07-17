from flask import current_app
from config import CONFIG
from PIL import Image
import tempfile


def save_img(data, path):
	try:
		temp = tempfile.TemporaryFile()

		temp.write(data)

		temp.seek(0)

		save_resized_img(temp, path)
	except Exception as e:
		current_app.logger.error(e)
	finally:
		temp.close()


def save_resized_img(img_temp_file, path):
	try:
		with Image.open(img_temp_file) as img:
			width, height = img.size

			img.thumbnail(smallerSize(width, height), Image.ANTIALIAS)

			img.save(path, 'JPEG')
	except Exception as e:
		print('error!!!')
		current_app.logger.error(e)


def smallerSize(width, height):
	max_width = CONFIG['Storage']['img']['max_size']['width']
	max_height = CONFIG['Storage']['img']['max_size']['height']

	if width > max_width:
		height = height * max_width / width

	if height > max_height:
		width = width * max_height / height

	print(width)
	print(height)

	return (int(width), int(height))
