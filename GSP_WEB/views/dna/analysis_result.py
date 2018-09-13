#-*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

from dateutil import parser
from elasticsearch import Elasticsearch
from flask import request, Response, render_template, Blueprint, json, make_response, g, session
from sqlalchemy import or_, and_

from GSP_WEB import db_session, login_required, app
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.DNA_Element import DNA_Element
from GSP_WEB.query import dna_result
from GSP_WEB.views.dna import blueprint_page
import flask_excel as excel

@blueprint_page.route('/analysis_result', methods=['GET'])
@login_required
def analysisResult_List():
    #logUtil.addLog(request.remote_addr,1,'links > list ')
    #type_list = CommonCode.query.filter_by(GroupCode = 'raw_data_type').all()
    dna = request.args.get("dna")
    sector = request.args.get("sector")
    whiteList = request.args.get("whitelist")
    showWhiteListFalse = request.args.get("showWhiteListFalse")

    return render_template('dna/analysis_result.html', dna= dna, sector= sector, whiteList= whiteList, showWhiteListFalse = showWhiteListFalse)

@blueprint_page.route('/analysis_result/columnlist', methods=['GET'])
#@login_required
def getDnaColumnList():
    #logUtil.addLog(request.remote_addr, 1, 'linkdna-board/log')

    columns = list()

    col_num = {
        "data" : "rownum",
        "title" : "",
        "width": "50px"
    }
    columns.append(col_num)

    col_link = {
        "data": "_id",
        "title": "Link IP(s) → IP(d)",
        "width" : "200px"
    }

    columns.append(col_link)

    #region DB 컬럼 기준 사용중인 Link 요소 컬럼 목록
    list_a = DNA_Element.query.filter(
        and_(DNA_Element.use_yn == 'Y', DNA_Element.del_yn == 'N')).all()

    for _row in list_a:
        col = {
            "data": "_source." + _row.dna_name + ".sector",
            "title": _row.dna_name,
            "width": "150px"
        }
        columns.append(col)

    str_json = json.dumps(columns, encoding='utf-8')
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/analysis_result/list', methods=['POST'])
#@login_required
def getDnaAnalysisResultList():
    #logUtil.addLog(request.remote_addr, 1, 'linkdna-board/log')

    columns = list()
    whiteList = request.form.get('showWhiteListFalse')


    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    doc = dna_result.getAnalysisResult(request)
    res = es.search(index="gsp-link_result" + "", doc_type="dna_result", body=doc, request_timeout=60)

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    if total > 10000:
        total = 10000

    for index, _row in enumerate(esResult):
        _row['rownum'] = int(request.form.get('start')) + index + 1

    result = dict()
    result["recordsTotal"] = total
    result["recordsFiltered"] = str(total)
    result["data"] = esResult
    result["draw"] = int(request.form['draw'])
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/analysis_result/excel-list', methods=['GET','POST'])
#@login_required
def getDnaAnalysisResultExcel():
    columns = list()

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    doc = dna_result.getAnalysisResult(request)
    res = es.search(index="gsp-link_result" + "", doc_type="dna_result", body=doc, request_timeout=60)

    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    if total > 10000:
        total = 10000

    result = OrderedDict()

    result['src_ip'] = list()
    result['dst_ip'] = list()

    for _item in esResult:
        result['src_ip'].append(_item['_source']['src_ip'])
        result['dst_ip'].append(_item['_source']['dst_ip'])

    for _item in esResult:
        for _key, _val in _item['_source'].iteritems():
            if _key == "@timestamp" or _key=='src_ip' or _key =="dst_ip":
                continue

            if result.has_key(_key) == False:
                result[_key] = list()
            if isinstance(_val, dict) is True:
                _val = _val['sector']

            result[_key].append(_val)
    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")