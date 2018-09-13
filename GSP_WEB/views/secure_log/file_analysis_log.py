# -*- coding: utf-8 -*-
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
from GSP_WEB.query.secure_log import getCncLogQuery, getCncLogQueryURL, getCncLogQueryURLCount, \
     getCncLogQueryCountFileAnalysisStatus
from GSP_WEB.views.secure_log import blueprint_page
import json


@blueprint_page.route('/file-anlaysis', methods=['GET'])
@login_required
def getFileLog():
    nowtime = datetime.datetime.now()
    start_of_day = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)
    logUtil.addLog(request.remote_addr, 1, 'secure-log/cnc')
    timefrom = start_of_day.strftime("%Y-%m-%d %H:%M")
    #timefrom = (datetime.datetime.now() - start_of_day).strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    logUtil.addLog(request.remote_addr, 1, 'security log > file analysis ')
    type_list = CommonCode.query.filter_by(GroupCode='an_data_from').all()
    #type_list.remove(type_list[0])
    return render_template('secure_log/file_analysis_list.html', timefrom=timefrom, timeto=timeto \
                           , type_list=type_list)


@blueprint_page.route('/file-anlaysis/getlist', methods=['POST'])
def getFileLogList():
    logList = None

    # region search option
    per_page = int(request.form['perpage'])
    draw = int(request.form['draw'])
    start_idx = int(request.form['start'])
    # endregion

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    query_type = "file"
    doc = getCncLogQuery(request,query_type)
    res = es.search(index="gsp*" + "", doc_type="analysis_results", body=doc)

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    resultList = []

    # search_keyword_type = request.form['search_keyword_type']
    # search_keyword = request.form['search_keyword']
    # sortedESresult = list()

    # if search_keyword and search_keyword_type:
    #      for aitem in esResult:
    #          if search_keyword in aitem['_source'][search_keyword_type]:
    #             sortedESresult.append(aitem)
    #
    # if sortedESresult:
    #      esResult = sortedESresult  ## Search feature has been added in Python implementation##
    #      total = len(esResult)

    # C&C타입 목록
    type_list = CommonCode.query.filter_by(GroupCode='RULE_CNC_TYPE').all()

    for row in esResult:
        resultRow = dict()
        times = parser.parse(row['_source']['@timestamp'])
        resultRow['timestamp'] = times.strftime("%Y.%m.%d %H:%M:%S")
        resultRow['data_from'] = row['_source'].get('data_from')
        resultRow['file_name'] = row['_source'].get('file_name')
        resultRow['md5'] = row['_source'].get('md5')
        if row['_source'].get('data_from') == "zombie zero":
            resultRow['collect_uri'] = row['_source'].get('uri')
            resultRow['category'] = row['_source'].get('malware_info')
        else:
            resultRow['collect_uri'] = row['_source'].get('collect_uri')
            resultRow['category'] = row['_source'].get('category')
        #resultRow['collect_seed_uri'] = row['_source'].get('collect_seed_uri')

        if int(row['_source']['security_level']) >= int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']):
            resultRow['result'] = '악성'
        else:
            resultRow['result'] = '정상'
        resultList.append(resultRow)

    #if total > 10000:
    #    total = 10000
    result = dict()
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = resultList
    result["draw"] = str(draw)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/file-anlaysis/excel-list', methods=['GET','POST'])
#@login_required
def getFileLogListExcel():
    logList = None

    # region search option
    #per_page = int(request.form['perpage'])

    start_idx = int(request.form['start'])
    # endregion

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    query_type = "file"
    documentCount = getCncLogQueryCountFileAnalysisStatus(request, query_type)
    resCountDoc = es.count(index="gsp*" + "", doc_type="analysis_results", body=documentCount)
    doc = getCncLogQuery(request, query_type, resCountDoc['count'])
    res = es.search(index="gsp*" + "", doc_type="analysis_results", body=doc)

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    resultList = []

    # search_keyword_type = request.form['search_keyword_type']
    # search_keyword = request.form['search_keyword']
    # sortedESresult = list()

    # if search_keyword and search_keyword_type:
    #      for aitem in esResult:
    #          if search_keyword in aitem['_source'][search_keyword_type]:
    #             sortedESresult.append(aitem)
    #
    # if sortedESresult:
    #      esResult = sortedESresult  ## Search feature has been added in Python implementation##
    #      total = len(esResult)

    # C&C타입 목록
    type_list = CommonCode.query.filter_by(GroupCode='RULE_CNC_TYPE').all()

    for row in esResult:
        resultRow = dict()
        times = parser.parse(row['_source']['@timestamp'])
        resultRow['timestamp'] = times.strftime("%Y.%m.%d %H:%M:%S")
        resultRow['data_from'] = row['_source'].get('data_from')
        resultRow['file_name'] = row['_source'].get('file_name')
        resultRow['md5'] = row['_source'].get('md5')
        if row['_source'].get('data_from') == "zombie zero":
            resultRow['collect_uri'] = row['_source'].get('uri')
            resultRow['category'] = row['_source'].get('malware_info')
        else:
            resultRow['collect_uri'] = row['_source'].get('collect_uri')
            resultRow['category'] = row['_source'].get('category')
        # resultRow['collect_seed_uri'] = row['_source'].get('collect_seed_uri')

        if int(row['_source']['security_level']) >= int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']):
            resultRow['result'] = '악성'
        else:
            resultRow['result'] = '정상'
        resultList.append(resultRow)


    result = OrderedDict()

    result['날짜'] = list()
    result['파일명'] = list()
    result['해시 값'] = list()
    result['다운로드 경로'] = list()
    result['시드 URI 경로'] = list()
    result['카테고리'] = list()
    result['분석 장비'] = list()
    result['분석 결과'] = list()

    for _item in resultList:
        result['카테고리'].append(_item['category'])
        result['다운로드 경로'].append(_item['collect_uri'])
        result['해시 값'].append(_item['md5'])
        result['파일명'].append(_item['file_name'])
        result['분석 장비'].append(_item['data_from'])
        result['날짜'].append(_item['timestamp'])
        result['분석 결과'].append(_item['result'])




    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")
