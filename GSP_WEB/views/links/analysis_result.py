#-*- coding: utf-8 -*-
import datetime

from dateutil import parser
from elasticsearch import Elasticsearch
from flask import request, Response, render_template, Blueprint, json, make_response, g, session
from sqlalchemy import or_, and_

from GSP_WEB import db_session, login_required, app
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.Link_Element_List import *
from GSP_WEB.models.Link_Element_TypeA import Link_Element_TypeA
from GSP_WEB.models.Link_Element_TypeB import Link_Element_TypeB
from GSP_WEB.views.links import blueprint_page
import flask_excel as excel
import numpy as np


@blueprint_page.route('/analysis_result', methods=['GET'])
@login_required
def analysis_result_List():
    #logUtil.addLog(request.remote_addr,1,'links > list ')
    #type_list = CommonCode.query.filter_by(GroupCode = 'raw_data_type').all()
    src_ip = request.args.get('src_ip').replace(" ", "") if request.args.get('src_ip') is not None else ""
    dst_ip = request.args.get('dst_ip').replace(" ", "") if request.args.get('dst_ip') is not None else ""
    type = request.args.get('type') if request.args.get('type') is not None else ""
    chart_type = request.args.get('chart_type') if request.args.get('chart_type') is not None else ""

    list_a = Link_Element_TypeA.query.filter(
        and_(Link_Element_TypeA.use_yn == 'Y', Link_Element_TypeA.del_yn == 'N')
        , Link_Element_TypeA.dst_columns_name != "@timestamp").all()
    list_b = Link_Element_TypeB.query.filter(
        and_(Link_Element_TypeB.use_yn == 'Y', Link_Element_TypeB.del_yn == 'N')).all()

    return render_template('links/analysis_result.html', src_ip=src_ip, dst_ip=dst_ip, type=type, chart_type = chart_type,
                           list_a = list_a, list_b = list_b)

@blueprint_page.route('/analysis_result/columnlist', methods=['GET','POST'])
@login_required
def getElementColumnList():
    #logUtil.addLog(request.remote_addr, 1, 'linkdna-board/log')

    columns = list()

    col_link = {
        "data": "_id",
        "title": "Link IP(s) → IP(d)",
        "width" : "200px"
    }

    columns.append(col_link)

    #region DB 컬럼 기준 사용중인 Link 요소 컬럼 목록
    list_a = Link_Element_TypeA.query.filter(
        and_(Link_Element_TypeA.use_yn == 'Y', Link_Element_TypeA.del_yn == 'N')).all()
    list_b = Link_Element_TypeB.query.filter(
        and_(Link_Element_TypeB.use_yn == 'Y', Link_Element_TypeB.del_yn == 'N')).all()

    # new_list_a_order = [0,1,4,5,6,7,8,9,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30, 2, 3, 31,32,33,34,35,36,14,15]
    # list_a = [list_a[i] for i in new_list_a_order]

    useColumnList = []

    # 파라메터로 넘어온 사용 할 column list
    if request.form.get('ids') is not None :
        useColumnList = request.form.getlist('ids')

    elementList = dict()
    #type = request.args.get("type")
    for _row in list_a:
        if  (_row.dst_columns_name == "src_country_code" or _row.dst_columns_name == "dst_country_code") \
                and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "50px",
                # "height" : "150px;",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

        elif (_row.dst_columns_name == "src_lon" or _row.dst_columns_name == "src_lat" or _row.dst_columns_name == "dst_lon" or _row.dst_columns_name == "dst_lat") and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "135px",
                # "height" : "150px;",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

        elif (_row.dst_columns_name == "tcp_flags" or _row.dst_columns_name == "pps") and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "50px",
                # "height" : "150px;",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

        elif _row.dst_columns_name == "distance" and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "190px",
                # "height" : "150px;",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

        elif (_row.dst_columns_name != "src_ip" and _row.dst_columns_name != "dst_ip" \
                and _row.dst_columns_name != "@timestamp" and _row.dst_columns_name != "src_country_code" \
                and _row.dst_columns_name != "dst_country_code" and _row.dst_columns_name != "src_lon" and _row.dst_columns_name != "src_lat" \
                and _row.dst_columns_name != "dst_lon" and _row.dst_columns_name != "dst_lat" and _row.dst_columns_name != "tcp_flags" and _row.dst_columns_name != "pps" \
                and _row.dst_columns_name != "distance") and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "225px",
                #"padding": "0px",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

    for _row in list_b:
        if  (_row.dst_columns_name == "src_country_code" or _row.dst_columns_name == "dst_country_code") and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "50px",
                # "height" : "150px;",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

        elif (_row.dst_columns_name == "src_lon" or _row.dst_columns_name == "src_lat" or _row.dst_columns_name == "dst_lon" or _row.dst_columns_name == "dst_lat") and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "135px",
                # "height" : "150px;",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

        elif (_row.dst_columns_name == "tcp_flags" or _row.dst_columns_name == "pps") and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "50px",
                # "height" : "150px;",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

        elif _row.dst_columns_name == "distance" and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "190px",
                # "height" : "150px;",
                "data_type": _row.dst_data_type
            }
            columns.append(col)

        elif (_row.dst_columns_name != "src_ip" and _row.dst_columns_name != "dst_ip" \
                and _row.dst_columns_name != "@timestamp" and _row.dst_columns_name != "src_country_code" \
                and _row.dst_columns_name != "dst_country_code" and _row.dst_columns_name != "src_lon" and _row.dst_columns_name != "src_lat" \
                and _row.dst_columns_name != "dst_lon" and _row.dst_columns_name != "dst_lat" and _row.dst_columns_name != "tcp_flags" and _row.dst_columns_name != "pps" \
                and _row.dst_columns_name != "distance") and (_row.dst_columns_name in useColumnList):
            col = {
                "data": "_source." + _row.dst_columns_name,
                "title": _row.dst_columns_name,
                "width": "225px",
                #"padding": "0px",
                "data_type": _row.dst_data_type
            }
            columns.append(col)



    str_json = json.dumps(columns, encoding='utf-8')
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/analysis_result/list', methods=['GET','POST'])
@login_required
def geAnalysisResultList():
    #logUtil.addLog(request.remote_addr, 1, 'linkdna-board/log')

    columns = list()
    sortedResults = list()

    src_ip = request.form.get('search_src_ip').replace(" ", "")
    dst_ip = request.form.get('search_dst_ip').replace(" ", "")

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    doc = Link_Element_List.getAnalysisResult(request)
    docCount = Link_Element_List.getTotalAnalysisResultCount(request)
    resCount = es.count(index="gsp-link_dna" + "", doc_type="link_dna", body=docCount, request_timeout=60) #link count code added
    res = es.search(index="gsp-link_dna" + "", doc_type="link_dna", body=doc, request_timeout=60)

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    totalCount = resCount['count']
    if total > 10000:
        total = 10000
        #totalCount = 10000

    #차트 타입에 따라 array
    search_chart_type = request.form.get("search_chart_type")
    search_type = request.form.get("search_type")

    colList = request.form.getlist('requestColumnList')

    for _row in esResult:
        for _key, _val in _row['_source'].iteritems():
            if _key not in colList:
                continue
            ar = np.array(_row['_source'][_key])
            # 다차원 배열인 경우 주, 일 등으로 통계치를 구한다.
            if ar.ndim > 1:
                if search_chart_type == "DOW":
                    _row['_source'][_key] = getDayOfWeekSum(_row['_source'][_key])
                elif search_chart_type == "HOD":
                    _row['_source'][_key] = getHoursOfDay(_row['_source'][_key])

    for _row in esResult:
        for _key, _val in _row['_source'].iteritems():
            if _key not in colList:
                continue
            ar = np.array(_row['_source'][_key])
            if ar.ndim > 0:
                _row['_source'][_key] = getFlattenList(_row['_source'][_key])

    #sorted(reResult, key = lambda )#(key=itemgetter('@timestamp'))
    #sortedResults = sorted(esResult, key=itemgetter('@timestamp'))
    #sorted(esResult, key=lambda k: parser.parse(k['_source']['@timestamp'])) ##sort the retrieved data by timestamp so that the items in the view and the excel are listed identically. Modified by In chan Hwang
    #sorted(esResult, key=lambda k : (len(k['_source']['flag_list']) - k['_source']['flag_list'].count(0)), reverse=True)
    if src_ip == '' or dst_ip == '':
        sorted(esResult, key=lambda k: k['_source']['pkts-dispersion'], reverse=True)

    result = dict()
    result["total"] = totalCount#res['hits']['total']
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = esResult
    result["draw"] = int(request.form['draw'])

    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/analysis_result/excel-list', methods=['GET','POST'])
#@login_required
def getAnalysisResultExcel():
    columns = list()

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    doc = Link_Element_List.getAnalysisResult(request)
    res = es.search(index="gsp-link_dna" + "", doc_type="link_dna", body=doc, request_timeout=60)

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    if total > 10000:
        total = 10000

    # 차트 타입에 따라 array
    search_chart_type = request.form.get("search_chart_type")
    search_type = request.form.get("search_type")

    colList = request.form.getlist('requestColumnList')

    for _row in esResult:
        for _key, _val in _row['_source'].iteritems():
            if _key not in colList:
                continue
            ar = np.array(_row['_source'][_key])
            # 다차원 배열인 경우 주, 일 등으로 통계치를 구한다.
            if ar.ndim > 1:
                if search_chart_type == "DOW":
                    _row['_source'][_key] = getDayOfWeekSum(_row['_source'][_key])
                elif search_chart_type == "HOD":
                    _row['_source'][_key] = getHoursOfDay(_row['_source'][_key])

    for _row in esResult:
        for _key, _val in _row['_source'].iteritems():
            if _key not in colList:
                continue
            ar = np.array(_row['_source'][_key])
            if ar.ndim > 0:
                _row['_source'][_key] = getFlattenList(_row['_source'][_key])

    result = {

    }

    #sorted(esResult, key=lambda k: parser.parse(k['_source']['@timestamp'])) ##sort the retrieved data by timestamp so that the items in the view and the excel are listed identically. Modified by In chan Hwang
    #sorted(esResult, key=lambda k: (len(k['_source']['flag_list']) - k['_source']['flag_list'].count(0)), reverse=True)
    sorted(esResult, key=lambda k: k['_source']['pkts-dispersion'], reverse=True)
    for _item in esResult:
        for _key, _val in _item['_source'].iteritems():
            if result.has_key(_key) == False:
                result[_key] = list()

            temp_val = None
            if isinstance(_val , list):
                temp_val = NoneToEmptyString(_val)[:]
            else:
                temp_val = _val
            result[_key].append(temp_val)
    return excel.make_response_from_dict(result, "csv",
                                          file_name="export_data")

def getDayOfWeekSum(arr):

    try:
        arr = np.array(arr, dtype=np.float)
        arr[np.isnan(arr)] = 0
    except Exception:
        return arr

    if arr.ndim != 3:
        return arr

    return np.sum(np.sum(arr, axis=2), axis=1).tolist()


def getHoursOfDay(arr):
    try:
        arr = np.array(arr, dtype=np.float)
        arr[np.isnan(arr)] = 0
    except Exception:
        return arr

    if arr.ndim != 3:
        return arr

    hod = np.sum(np.sum(arr, axis=0), axis=1)

    return hod.tolist()

def getFlattenList(arr):
    try:
        arr = np.array(arr, dtype=np.float)
        arr[np.isnan(arr)] = 0
    except Exception:
        return arr

    if arr.ndim == 3:
        arr = np.sum(np.sum(arr, axis=2), axis=1)

    if arr.ndim == 2:
        arr = np.sum(arr, axis=0)

    return arr.tolist()

def NoneToEmptyString(arr):
    try:
        arr = np.array(arr, dtype=np.float)
        arr[np.isnan(arr)] = 0
    except Exception:
        return arr

    return arr.tolist()