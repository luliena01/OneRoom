import os
from config import CONFIG
from flask import Flask, render_template, request, url_for
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)

app.secret_key = CONFIG['Security']['secret_key']

from content_management import Content