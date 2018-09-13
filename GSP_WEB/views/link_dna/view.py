#-*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
from GSP_WEB.common.util.date_util import Local2UTC, UTC2Local
from elasticsearch import Elasticsearch
from flask import Blueprint, request, render_template, json, Response
from dateutil import parser

from GSP_WEB.common.util import spark_helper
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB import app, login_required
import json

from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_Profile import Rules_Profile
from GSP_WEB.query.link_dna import GetLinkDnaListQueryEs, GetLinkDnaTuple3, GetLinkDnaTuple2, GetServerConnectionCount, \
    GetClientConnectionCount, GetMatchedInfo

blueprint_page = Blueprint('bp_link_dna_log_page', __name__, url_prefix='/link-dna')

@blueprint_page.route('/', methods=['GET'])
@login_required
def getLinkDnaLog():
    logUtil.addLog(request.remote_addr, 1, 'link-dna/log')
    timefrom = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    profileList = Rules_Profile.query.all()
    typeList = CommonCode.query.filter_by(GroupCode="DATA_TYPE").all()

    return render_template('linkdna_log/list.html',timefrom = timefrom, timeto=timeto, profileList = profileList, typeList =typeList)


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
    res = es.search(index="gsp-*" + "", doc_type="link_dna_tuple4", body=doc, request_timeout=30)

    for row in res['hits']['hits']:
        row['display_time'] = parser.parse(row['_source']['min_timestamp']).strftime('%Y-%m-%d %H:%M:%S')

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

@blueprint_page.route('/getdetail')
def getLinkDnaDetail():
    endtime = parser.parse(request.args['end_time'])
    starttime = parser.parse(request.args['start_time'])
    svr_ip = request.args['src_ip']
    svr_port = request.args.get('src_port') if request.args.get('src_port') is not None else ""
    cl_ip = request.args.get('dst_ip')
    #region analysis results query
    query = {
        "size": 10,
        "sort": [
            {"security_level": "desc"}
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {"@timestamp": {"gte": starttime.isoformat(), "lte": endtime.isoformat()}}
                    },
                    {
                        "term": {"svr_ip": svr_ip}
                    },
                    {
                        "term": {"cl_ip": cl_ip}
                    },
                    {
                        "term": {"svr_port": svr_port}
                    }
                ]
            }
        }
    }
    #endregion
    result = dict()
    analysis_results = dict()
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    try:
        res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="analysis_results", body=query,request_timeout=30)
        analysis_results['file_name'] = ''
        analysis_results['uri'] = ''
        analysis_results['md5'] = ''
        analysis_results['security_level'] = ''

        for _item in res['hits']['hits']:
            analysis_results['file_name'] = _item['_source']['file_name']
            analysis_results['uri'] = _item['_source']['uri']
            analysis_results['md5'] = _item['_source']['md5']
            if int(_item['_source']['security_level']) >= int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']) :
                analysis_results['security_level'] = "악성"
            else:
                analysis_results['security_level'] = "정상"
            break;

        result['analysis_results'] = analysis_results
    except Exception:
        print("")

    #서버 접속수 계산 쿼리
    query_servercon = GetServerConnectionCount(starttime, endtime, svr_ip, svr_port)
    res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="link_dna_tuple3", body=query_servercon)
    for _item in res['hits']['hits']:
        result['server_con'] = _item['_source']['cnt']

    # 클라이언트 접속수 계산 쿼리
    query_clientcon = GetClientConnectionCount(starttime, endtime, cl_ip)
    res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="link_dna_tuple2", body=query_clientcon)
    for _item in res['hits']['hits']:
        result['client_con'] = _item['_source']['cnt']

    #traffics
    query_traffics = GetMatchedInfo(starttime, endtime, svr_ip, svr_port, cl_ip)
    res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="traffics", body=query_traffics)
    for _item in res['hits']['hits']:
        result['traffics'] = _item['_source']['alert']['signature']

    #syslogs
    query_syslogs = GetMatchedInfo(starttime, endtime, svr_ip, svr_port, cl_ip)
    res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="syslogs", body=query_syslogs)
    for _item in res['hits']['hits']:
        result['syslogs_name'] = _item['_source']['syslog_name']
        result['syslogs_msg'] = _item['_source']['msg']

    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

#Retail Version
@blueprint_page.route('/getdetailAnalysis')
def getLinkDnaDetailAnalaysis():
    searchtime = Local2UTC(parser.parse(request.args['search_time']))
    endtime = searchtime + datetime.timedelta(hours=12)
    starttime = searchtime - datetime.timedelta(hours=12)
    svr_ip = request.args['svr_ip']
    svr_port = request.args['svr_port']
    cl_ip = request.args['cl_ip']
    query = {
        "size": 10,
        "sort": [
            {"security_level": "desc"}
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {"@timestamp": {"gte": starttime.isoformat(), "lte": endtime.isoformat()}}
                    },
                    {
                        "term": {"svr_ip": svr_ip}
                    },
                    {
                        "term": {"cl_ip": cl_ip}
                    },
                    {
                        "term": {"svr_port": svr_port}
                    }
                ]
            }
        }
    }

    result = dict()
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="analysis_results", body=query,request_timeout=30)

    result['file_name'] = ''
    result['uri'] = ''
    result['md5'] = ''
    result['security_level'] = ''

    for _item in res['hits']['hits']:
        result['file_name'] = _item['_source']['file_name']
        result['uri'] = _item['_source']['uri']
        result['md5'] = _item['_source']['md5']
        if int(_item['_source']['security_level']) >= int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']) :
            result['security_level'] = "악성"
        else:
            result['security_level'] = "정상"
        break;

    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/con-server-list', methods=['GET'])
def getConServer():
    logUtil.addLog(request.remote_addr, 1, 'link-dna/con-server-list')
    start_time = request.args['start_time']
    end_time = request.args['end_time']
    con_svr_from = request.args['con_svr_from']
    con_svr_to = request.args['con_svr_to']
    doc = GetLinkDnaTuple3(start_time, end_time, con_svr_from, con_svr_to)
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="link_dna_tuple3", body=doc)

    return render_template('linkdna_log/server_con.html', listServerCon=res['hits']['hits'] )

@blueprint_page.route('/con-client-list', methods=['GET'])
def getConClient():
    logUtil.addLog(request.remote_addr, 1, 'link-dna/con-server-list')
    start_time = request.args['start_time']
    end_time = request.args['end_time']
    con_from = request.args['con_cli_from']
    con_to = request.args['con_cli_to']
    doc = GetLinkDnaTuple2(start_time, end_time, con_from, con_to)
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="link_dna_tuple2", body=doc)

    return render_template('linkdna_log/client_con.html', listServerCon=res['hits']['hits'] )