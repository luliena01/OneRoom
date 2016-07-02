import logging
from logging.handlers import TimedRotatingFileHandler

class Logger:

    def get_log_handler:
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        handler = TimedRotatingFileHandler(os.path.join(os.getcwd(), "templates", "logs", 'one_room.log'), when='midnight', interval=1)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        return handler