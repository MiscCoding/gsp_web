# import redis as redis
import dateutil
import pytz
from flask import Flask, render_template, url_for, session, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from pyspark import SparkContext, SQLContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
from werkzeug.utils import find_modules, import_string, redirect

from GSP_WEB.common.encoder.encryptEncoder import EncryptEncoder
from GSP_WEB.common.util.decorators import login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.database import init_db
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import logging

app = Flask(__name__)
app.config.from_pyfile('../config.py')

# Init Logger
logger = logging.getLogger()
logger.setLevel(app.config.get('LOG_LEVEL'))
logfile = app.config['LOG_FILE']
rotatingHandler = logging.handlers.TimedRotatingFileHandler(filename=logfile, when='midnight', interval=1, encoding='utf-8')
fomatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
rotatingHandler.setFormatter(fomatter)
logger.addHandler(rotatingHandler)

# region Init Database
app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SQLALCHEMY_NATIVE_UNICODE'] = True

db = SQLAlchemy(app)
db_session = db.session
init_db(db)

# region Register BluePrint
for name in find_modules('GSP_WEB.views', recursive=True):
    mod = import_string(name)
    if hasattr(mod, 'blueprint_page'):
        app.register_blueprint(mod.blueprint_page)
# endregion

@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return render_template('500.html'), 500

@app.route('/')
@login_required
def index():
    return redirect("/index")

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.template_filter('strftime')
def format_iso_to_local(isodate, fmt=None):
    date = dateutil.parser.parse(isodate)
    local_timezone = pytz.timezone('Asia/Seoul')
    date.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    format = '%Y-%m-%d %H:%M:%S'
    return date.strftime(format)

@app.template_filter('currency')
def format_currency(value):
    return "{:,}".format(value)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
    return