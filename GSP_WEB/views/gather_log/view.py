#-*- coding: utf-8 -*-
import datetime
from GSP_WEB.common.util.date_util import Local2UTC
from elasticsearch import Elasticsearch
from flask import Blueprint, request, render_template, json, Response
from dateutil import parser

from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB import app, login_required
import json

blueprint_page = Blueprint('bp_gather_log_page', __name__, url_prefix='/gather-log')

@blueprint_page.route('', methods=['GET'])
@login_required
def getGetherLog():
    logUtil.addLog(request.remote_addr, 1, 'gather-log')
    kibana_uri = app.config['KIBANA_URI']
    return render_template('gather_log/list.html', kinana_uri = kibana_uri)