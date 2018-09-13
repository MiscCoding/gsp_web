import os
import logging

DEBUG = True
SECRET_KEY = os.urandom(24)
SESSION_COOKIE_NAME = '!npcore_webserver_session@'
DATABASE_URI = 'mysql+pymysql://root:npCore!234@192.168.200.41:3306/GSP_WEB?charset=utf8'
ELASTICSEARCH_URI = '192.168.200.41'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_INDEX = 'gsp-*'
ELASTICSEARCH_INDEX_HEAD = 'gsp-'
SEND_FILE_MAX_AGE_DEFAULT = 0
UPLOAD_FOLDER = '/usr/gsp/nfs'
UPLOAD_CRAWLING_FOLDER = 'CRAWLING'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
REDIS_HOST_IP = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 11
default_log_path = '/usr/gsp/web/log/gsp.log'
LOG_FILE = os.getenv('BACKOFFICE_LOG_FILE', default_log_path)
LOG_MAX_BYTES = 2048
LOG_BACKUP_COUNT = 10
LOG_LEVEL = logging.INFO
SESSION_TIMEOUT_MIN = 30
SQLALCHEMY_TRACK_MODIFICATIONS = True
ANALYSIS_RESULTS_SECURITY_LEVEL_MIN = 4
KIBANA_URI = "http://121.156.47.202:8080/app/kibana#/discover?_g=()&_a=(columns:!(_source),index:AWE6gXVe-A91BkKZeJVv,interval:auto,query:(match_all:()),sort:!('@timestamp',desc))"
