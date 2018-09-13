#-*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
import flask_excel as excel
from GSP_WEB.common.util.date_util import Local2UTC
from elasticsearch import Elasticsearch
from flask import Blueprint, request, render_template, json, Response
from dateutil import parser

from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB import app, login_required
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.query.secure_log import getCncLogQuery, getCncLogQueryURL, getCncLogQueryURLCount
from GSP_WEB.views.secure_log import blueprint_page

import json

@blueprint_page.route('/cnc', methods=['GET'])
@login_required
def getCncLog():
    nowtime = datetime.datetime.now()
    start_of_day = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)
    logUtil.addLog(request.remote_addr, 1, 'secure-log/cnc')
    timefrom = start_of_day.strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    logUtil.addLog(request.remote_addr, 1, 'rules > c&c ')
    type_list = CommonCode.query.filter_by(GroupCode='an_data_from_url').all()
    return render_template('secure_log/cnc_list.html',timefrom = timefrom, timeto=timeto\
                           , type_list = type_list)

@blueprint_page.route('/cnc/getlist', methods=['POST'])
def getCncLogListES():
    logList = None

    # region search option
    #per_page = int(request.form['perpage'])
    draw = int(request.form['draw'])
    #start_idx = int(request.form['start'])
    # endregion

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    query_type = "uri"
    doc = getCncLogQueryURL(request, query_type)
    res = es.search(index="gsp*" + "", doc_type="analysis_results", body=doc)

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    resultList = []
    sortedESresult = list()

    search_keyword = request.form['search_keyword']

    # if search_keyword:
    #     for aitem in esResult:
    #         if search_keyword in aitem['_source']['uri']:
    #             sortedESresult.append(aitem)
    #
    # if sortedESresult:
    #     esResult = sortedESresult ## Search feature has been added in Python implementation
    #     total = len(esResult)



    #C&C타입 목록
    type_list = CommonCode.query.filter_by(GroupCode='RULE_CNC_TYPE').all()

    for row in esResult:
        resultRow = dict()
        times = parser.parse(row['_source']['@timestamp'])
        resultRow['timestamp'] = times.strftime("%Y.%m.%d %H:%M:%S")
        #uri_type_name = [item.EXT1 for item in type_list if item.Code == row['_source']['uri_type'] ]
        uri_type_name = row['_source']['data_from']
        if int(row['_source']['security_level']) >= int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']):
            resultRow['result'] = '악성'
        else:
            resultRow['result'] = '정상'
        resultRow['data_from'] = row['_source'].get('data_from')
        resultRow['category'] = row['_source'].get('category')
        resultRow['uri'] = row['_source'].get('uri')
        resultList.append(resultRow)

    #if total > 10000 :
    #    total = 10000
    result = dict()
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = resultList
    result["draw"] = str(draw)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/cnc/excel-list', methods=['GET','POST'])
#@login_required
def getCncLogListExcel():
    logList = None

    # region search option
    #per_page = int(request.form['perpage'])
    #start_idx = int(request.form['start'])
    # endregion

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    query_type = "uri"
    countDoc = getCncLogQueryURLCount(request, query_type)
    documentAmount = es.count(index="gsp*" + "", doc_type="analysis_results", body=countDoc)
    doc = getCncLogQueryURL(request, query_type, documentAmount['count'])
    res = es.search(index="gsp*" + "", doc_type="analysis_results", body=doc)

    esresult = res['hits']['hits']
    total = int(res['hits']['total'])
    resultList = []

    sortedESresult = list()
    search_keyword = request.form['search_keyword']
    search_keyword_type = request.form['search_keyword_type']

    # if search_keyword:
    #     for myItem in esresult:
    #         if search_keyword in myItem['_source']['uri']: #Searched items excel download bug fixed. It happened due to invalid input read from HTML by Jquery. Server does not understand such thing.
    #             sortedESresult.append(myItem)
    #
    # if sortedESresult:
    #     esresult = sortedESresult  ## Search feature has been added in Python implementation


    # C&C타입 목록
    type_list = CommonCode.query.filter_by(GroupCode='RULE_CNC_TYPE').all()

    for row in esresult:
        resultRow = dict()
        times = parser.parse(row['_source']['@timestamp'])
        resultRow['timestamp'] = times.strftime("%Y.%m.%d %H:%M:%S")
        # uri_type_name = [item.EXT1 for item in type_list if item.Code == row['_source']['uri_type'] ]
        uri_type_name = row['_source']['data_from']
        if int(row['_source']['security_level']) >= int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']):
            resultRow['result'] = '악성'
        else:
            resultRow['result'] = '정상'
        resultRow['data_from'] = row['_source'].get('data_from')
        resultRow['category'] = row['_source'].get('category')
        resultRow['uri'] = row['_source'].get('uri')
        resultList.append(resultRow)

    result = OrderedDict()

    result['날짜'] = list()
    result['분석장비'] = list()
    result['분석 URI'] = list()
    result['카테고리'] = list()
    result['분석 결과'] = list()

    for _item in resultList:
        result['날짜'].append(_item['timestamp'])
        result['분석장비'].append(_item['data_from'])
        result['분석 URI'].append(_item['uri'])
        result['카테고리'].append(_item['category'])
        result['분석 결과'].append(_item['result'])

    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")