#-*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
from GSP_WEB.common.util.date_util import Local2UTC, UTC2Local
from elasticsearch import Elasticsearch
from flask import Blueprint, request, render_template, json, Response
from dateutil import parser

from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB import app, login_required
import json

from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.query.link_dna_5tuple import GetLinkDnaListQueryEs

blueprint_page = Blueprint('bp_link_dna_5tuple_page', __name__, url_prefix='/5tuple')

@blueprint_page.route('/', methods=['GET'])
@login_required
def getLinkDnaLog():
    #logUtil.addLog(request.remote_addr, 1, 'link-dna/log')
    timefrom = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    typeList = CommonCode.query.filter_by(GroupCode="DATA_TYPE").all()

    return render_template('5tuple/list.html',timefrom = timefrom, timeto=timeto, typeList =typeList)


@blueprint_page.route('/getlist-es', methods=['POST'])
def getLinkDnaListES():
    logList = None

    # region search option
    per_page = int(request.form['perpage'])
    draw = int(request.form['draw'])
    start_idx = int(request.form['start'])
    # endregion

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    doc = GetLinkDnaListQueryEs(request)
    res = es.search(index="gsp-*" + "", doc_type="tuple5", body=doc, request_timeout=30)

    for row in res['hits']['hits']:
        row['display_time'] = row['_source']['min_timestamp']

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    if total > 10000 :
        total = 10000
    result = dict()
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = esResult
    result["draw"] = str(draw)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')