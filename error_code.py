from enum import Enum


class Error_message(Enum):
	def message(self):
		return self.value


class Global(Error_message):
	UNKOWN = 'Unkown error.',
	DO_NOT_HAVE_PERMISSION = 'Do not have the permission.'


class Login(Error_message):
	NOT_FOUND_ID = 'Not found the email. Please, Sign up',
	WRONG_PASSWORD = 'Wrong password. Please, find your password.',
	ALREADY_REGISTER = "Your id is already registered. Please, login",
	NOT_CONFORMED = "Please, check your email to conform your email address."
