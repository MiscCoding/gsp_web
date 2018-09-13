#-*- coding: utf-8 -*-
import datetime
from elasticsearch import Elasticsearch
from flask import Blueprint, request, render_template, json, Response
from dateutil import parser
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB import app, login_required
import json

from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Link_Element_List import *
from GSP_WEB.query.ip_uri_map import GetIpUriMapQuery, typeName

blueprint_page = Blueprint('bp_ip_uri_maps_page', __name__, url_prefix='/ip-uri-maps')

@blueprint_page.route('/', methods=['GET'])
@login_required
def getIpUriMap():
    logUtil.addLog(request.remote_addr, 1, 'ip-uri-maps')
    timefrom = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return render_template('ip_uri_map/list.html',timefrom = timefrom, timeto=timeto )


@blueprint_page.route('/getlist', methods=['POST'])
@login_required
def getIpUriMapList():
    logList = None

    # region search option
    per_page = int(request.form['perpage'])
    draw = int(request.form['draw'])
    start_idx = int(request.form['start'])
    # endregion

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    doc = GetIpUriMapQuery(request)
    res = es.search(index="gsp-*" + "", doc_type=typeName, body=doc, request_timeout=60)

    for row in res['hits']['hits']:
        row['display_time'] = parser.parse(row['_source']['@timestamp']).strftime('%Y-%m-%d %H:%M:%S')

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    if total > 10000:
        total = 10000
    result = dict()
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = esResult
    result["draw"] = str(draw)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')