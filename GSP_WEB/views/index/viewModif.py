#-*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

from dateutil import parser
from elasticsearch import Elasticsearch
from flask import request, render_template, Blueprint, json

from GSP_WEB import login_required, db_session, app
from GSP_WEB.common.encoder.decimalEncoder import DecimalEncoder
from GSP_WEB.common.util.date_util import Local2UTC
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Nations import nations
from GSP_WEB.query.secure_log import getMaliciousCodeLogDataCountDashboard
from GSP_WEB.models.Rules_Crawl import Rules_Crawl

from GSP_WEB.models.Rules_BlackList import Rules_BlackList
from GSP_WEB.models.Rules_CNC import Rules_CNC
from GSP_WEB.models.malicious_info import malicious_info
from GSP_WEB.query import dashboard
from GSP_WEB.query.dashboard import *

blueprint_page = Blueprint('bp_index_page_modif', __name__, url_prefix='/modifindex')

# @blueprint_page.route('', methods=['GET'])
# @login_required
# def getIndex():
#     uri = CommonCode.query.filter_by(GroupCode='dashboard_link').filter_by(Code ='001').first()
#     return render_template('index/dashboard_kibana.html', kibana_link = uri.EXT1)
#
# @blueprint_page.route('/modifDashboardLink', methods=['PUT'])
# def setDashboardLink():
#     uri = CommonCode.query.filter_by(GroupCode='dashboard_link').filter_by(Code='001').first()
#     uri.EXT1 = request.form.get('link')
#     db_session.commit()
#     return ''


def todayUrlAnalysis(request, query_type = "uri"):
    per_page = 1
    start_idx = 0
    end_dt = "now/d"
    str_dt = "now-1d/d"

    # "now-1d/d", "now/d"

    query = {
        "size": per_page,
        "from": start_idx,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}
                    }, {
                        "term": {"analysis_type": query_type}
                    }

                ]
            }
        }
    }

    return query


def todayFileAnalysis(request, query_type = "file"):
    per_page = 1
    start_idx = 0
    end_dt = "now/d"
    str_dt = "now-1d/d"

    # "now-1d/d", "now/d"

    query = {
        "size": per_page,
        "from": start_idx,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}
                    }, {
                        "term": {"analysis_type": query_type}
                    }

                ]
            }
        }
    }



    return query



def totalMaliciousUrlQuery(request, query_type = "uri"):
    per_page = 1
    start_idx = 0
    end_dt = "now/d"
    str_dt = "now-1d/d"


    # "now-1d/d", "now/d"

    # timebefore = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
    # before = parser.parse(timebefore).isoformat()
    # timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # now = parser.parse(timeNow).isoformat()
    query = {
        "size": per_page,
        "from": start_idx,
        "query": {
            "bool": {
                "must": [
                    {

                        "term": {"analysis_type": query_type}

                    }
                    # {
                    #     "range":
                    #         {
                    #             "security_level": {"gte": "4"}
                    #         }
                    # }
                ]
            }
        }
    }

    secQuery = {"range": {"security_level": {"gte": int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])}}}
    query["query"]["bool"]["must"].append(secQuery)

    return query


def totalMaliciousQuery(request, query_type):
    per_page = 1
    start_idx = 0
    end_dt = "now/d"
    str_dt = "now-1d/d"


    # "now-1d/d", "now/d"

    # timebefore = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
    # before = parser.parse(timebefore).isoformat()
    # timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # now = parser.parse(timeNow).isoformat()
    query = {
        "size": per_page,
        "from": start_idx,
        "query": {
            "bool": {
                "must": [
                    # {
                    #     "range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}
                    # }
                    # {
                    #     "range":
                    #         {
                    #             "security_level": {"gte": "4"}
                    #         }
                    # }
                ]
            }
        }
    }

    secQuery = {"range": {"security_level": {"gte": int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])}}}
    query["query"]["bool"]["must"].append(secQuery)

    return query


def todayURLFileCount(type, device):
    end_dt = "now/d"
    str_dt = "now-1d/d"
    query = {

        "query": {
            "bool": {
                "must": [
                    # {
                    #     "range": {"@timestamp": {"gt": str_dt, "lte": end_dt}}
                    # }
                ]
            }
        }
    }
    dataFrom = {"match" : {"data_from" : {"query":device, "type":"phrase"}}}
    analysisType = {"match": {"analysis_type": {"query": type, "type": "phrase"}}}
    range = { "range": {"@timestamp": {"gt": str_dt, "lte": end_dt}}}
    # secQuery = {"range": {"security_level": {"gte": int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])}}}
    query["query"]["bool"]["must"].append(dataFrom)
    query["query"]["bool"]["must"].append(analysisType)
    query["query"]["bool"]["must"].append(range)

    return query


@blueprint_page.route('/getTopBoardModif')
def getTopBoardModif():
    query = dashboard.topboardQuery
    results = db_session.execute(query)

    nowtime = datetime.datetime.now()
    start_of_day = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)

    total = 0
    before_total = 0

    totalMaliciousCodeCount = 0
    totalTodayUriAnalysisCount = 0
    totalTodayUriAnalysisCountNPC = 0
    totalTodayUriAnalysisCountIMAS = 0


    totalTodayMaliciousFileCount = 0
    totalTodayMaliciousFileCountIMAS = 0
    totalTodayMaliciousFileCountNPC = 0
    totalTodayMaliciousFileCountZombieZero = 0

    totalMaliciousUrlCount = 0
    totalMaliciousUrlCountRDBMS = 0
    totalMaliciousFileCountRDBMS = 0


    totalYesterdayMaliciousUrlCount = 0
    totalYesterdayMaliciousFileCount = 0

    #Total malicious code count query to MySQL
    maliciousCodeQueryResult = malicious_info.query
    maliciousCodeQueryResult = maliciousCodeQueryResult.count()
    totalMaliciousFileCountRDBMS = maliciousCodeQueryResult
    maliciousCodeTodayQueryResult = malicious_info.query.filter(malicious_info.cre_dt.between(start_of_day, nowtime))
    todayMaliciousFileCountRDBMS = maliciousCodeTodayQueryResult.count()


    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    ##Total analysis URL and file count
    query_type = "analysis_info"
    doc = getMaliciousCodeLogDataCountDashboard(query_type)
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=doc)
        totalAnalysisCountElasticsearch = res['count']
    except Exception as e:
        totalAnalysisCountElasticsearch = 0

    doc = getMaliciousCodeLogDataCountDashboard(query_type, today=True)
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=doc)
        todayAnalysisCountElasticsearch = res['count']
    except Exception as e:
        todayAnalysisCountElasticsearch = 0

    ##Total finished crawled element count
    query_type = "url_crawleds"
    doc = Rules_Crawl.getCrawlCountDashboard()
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=doc)
        totalCrawledElementCount = res['count']
    except Exception as e:
        totalCrawledElementCount = 0
    ##Today crawled element count
    doc = Rules_Crawl.getCrawlCountDashboard(today=True)
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=doc)
        todayCrawledElementCount = res['count']
    except Exception as e:
        todayCrawledElementCount = 0

    ##Total collected URL and Today collected URLs.
    query_type = "url_jobs"
    doc = Rules_Crawl.getCrawlCountDashboard()
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=doc, request_timeout=120)
        totalCollectedURLCount = res['count']
    except Exception as e:
        totalCollectedURLCount = 0



    doc = Rules_Crawl.getCrawlCountDashboard(today=True)
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=doc, request_timeout=60)
        todayCollectedURLCount = res['count']
    except Exception as e:
        todayCollectedURLCount = 0

    ## Dashboard Link DNA count. Total count first.
    ## Netflow Doc
    NetflowCount = 0
    SyslogCount = 0
    TrafficCount = 0

    totalCollectedLinkCount = 0
    todayCollectedLinkCount = 0

    ## syslog subcount variables
    idsCount = 0
    aptCount = 0

    query_type = "link_dna"
    NFdoc = dashboard.DashboardTotalLinkCount("flag_list")
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=NFdoc, request_timeout=60)
        NetflowCount = res['count']
    except Exception as e:
        NetflowCount = 0


    ##Traffic  total count
    TRdoc = dashboard.DashboardTotalLinkCount("payload")
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=TRdoc, request_timeout=60)
        TrafficCount = res['count']
    except Exception as e:
        TrafficCount = 0

    ##IDS and APT sub counters to get Syslog count
    idsdoc = dashboard.DashboardTotalLinkCount("ids_*")
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=idsdoc, request_timeout=60)
        idsCount = res['count']
    except Exception as e:
        idsCount = 0

    aptdoc = dashboard.DashboardTotalLinkCount("apt_*")
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=aptdoc, request_timeout=60)
        aptCount = res['count']
    except Exception as e:
        aptCount = 0

    #Total syslog count
    SyslogCount =  idsCount + aptCount
    totalCollectedLinkCount = NetflowCount + TrafficCount + SyslogCount

    ## Dashboard Link DNA count. Today count second.

    query_type = "link_dna"
    NFdoc = dashboard.DashboardTotalLinkCount("flag_list", today=True)
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=NFdoc, request_timeout=60)
        NetflowCount = res['count']
    except Exception as e:
        NetflowCount = 0

    ##Traffic  total count
    TRdoc = dashboard.DashboardTotalLinkCount("payload", today=True)
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=TRdoc, request_timeout=60)
        TrafficCount = res['count']
    except Exception as e:
        TrafficCount = 0

    ##IDS and APT sub counters to get Syslog count
    idsdoc = dashboard.DashboardTotalLinkCount("ids_*", today=True)
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=idsdoc, request_timeout=60)
        idsCount = res['count']
    except Exception as e:
        idsCount = 0

    aptdoc = dashboard.DashboardTotalLinkCount("apt_*", today=True)
    try:
        res = es.count(index="gsp-*", doc_type=query_type, body=aptdoc, request_timeout=60)
        aptCount = res['count']
    except Exception as e:
        aptCount = 0

    ##Total syslog count
    SyslogCount = idsCount + aptCount
    todayCollectedLinkCount = NetflowCount + TrafficCount + SyslogCount




    ##total Malicious code count
    # query_type = ""
    # doc = totalMaliciousQuery(request, query_type)
    # res = es.search(index="gsp*" + "", doc_type="analysis_results", body=doc)
    # totalMaliciousCodeCount = int(res['hits']['total']) #Total malicious code count

    ##total malicious url count

    # MFdoc = totalMaliciousUrlQuery(request, "uri")
    # res = es.search(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    # totalMaliciousUrlCount = int(res['hits']['total'])

    ##total tody uri analysis count NPC

    MUdoc = todayURLFileCount("uri", "NPC")
    res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MUdoc)
    totalTodayUriAnalySisCountNPC = res['count']

    ##total tody uri analysis count NPC

    MUdoc = todayURLFileCount("uri", "IMAS")
    res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MUdoc)
    totalTodayUriAnalySisCountIMAS = res['count']



    ##total today file analysis count NPC
    MFdoc = todayURLFileCount("file", "NPC")
    res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    totalTodayMaliciousFileCountNPC = res['count']

    ##total today file analysis count IMAS
    MFdoc = todayURLFileCount("file", "IMAS")
    res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    totalTodayMaliciousFileCountIMAS = res['count']

    ##total today file analysis count ZombieZero
    MFdoc = todayURLFileCount("file", "zombie zero")
    res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    totalTodayMaliciousFileCountZombieZero = res['count']


    # MFdoc = todayFileAnalysis(request, "file")
    # res = es.search(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    # totalTodayMaliciousFileCount = int(res['hits']['total'])



    ##total yesterday malicious url count

    MFdoc = dashboard.yesterdayUrlFileAnalysis(request, "uri")
    res = es.search(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    totalYesterdayMaliciousUrlCount= int(res['hits']['total'])

    ##total yesterday malicious file count

    MFdoc = dashboard.yesterdayUrlFileAnalysis(request, "file")
    res = es.search(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    totalYesterdayMaliciousFileCount = int(res['hits']['total'])


    result = dict()
    result['spread'] = 0
    result['cnc'] = 0
    result['bcode'] = 0
    result['before_spread'] = 0
    result['before_cnc'] = 0
    result['before_bcode'] = 0
    result['link'] = 0
    result['before_link'] = 0
    result['uri'] = 0
    result['before_uri'] = 0
    result['file'] = 0
    result['before_file'] = 0
    result['totalTodayUriAnalysisCount'] = 0
    result['totalTodayUriAnalysisCountNPC'] = 0
    result['totalTodayUriAnalysisCountIMAS'] = 0
    result['totalTodayMaliciousFileCount'] = 0
    result['totalTodayMaliciousFileCountNPC'] = 0
    result['totalTodayMaliciousFileCountIMAS'] = 0
    result['totalTodayMaliciousFileCountZombieZero'] = 0
    result['totalMaliciousUrlQuery'] = 0
    result['totalYesterdayMaliciousUrlCount'] = 0
    result['totalYesterdayMaliciousFileCount'] = 0

    result['TotalCrawledCounts'] = 0

    #region db 쿼리
    for _row in results :
        if _row['date'] == datetime.datetime.now().strftime("%Y-%m-%d"):
            if _row['Code'] == "003":
                result['spread'] = _row['count']
            elif _row['Code'] == "001":
                result['cnc'] = _row['count']
            elif _row['Code'] == "-":
                result['bcode'] = _row['count']
            total += _row['count']
        else:
            if _row['Code'] == "003":
                result['before_spread'] = _row['count']
            elif _row['Code'] == "001":
                result['before_cnc'] = _row['count']
            elif _row['Code'] == "-":
                result['before_bcode'] = _row['count']
                before_total += _row['count']

    #endregion eb 쿼리

    index = app.config['ELASTICSEARCH_INDEX_HEAD'] + datetime.datetime.now().strftime('%Y.%m.%d')

    #region es 쿼리
    query = dashboard.topboardEsQuery("now-1d/d", "now/d")
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    res = es.search(index="gsp*", body=query, request_timeout=30) #url_crawlds 인덱스 문제로 임시 해결책 18-03-06
    for _row in res['aggregations']['types']['buckets']:
        if _row['key'] == "link_dna_tuple5":
            result['link'] = _row['doc_count']
            total += _row['doc_count']
        elif _row['key'] == "url_jobs":
            result['uri'] = _row['doc_count']
            total += _row['doc_count']
        elif _row['key'] == "url_crawleds":
            result['file'] = _row['doc_count']
            total += _row['doc_count']

    index = app.config['ELASTICSEARCH_INDEX_HEAD'] + datetime.datetime.now().strftime('%Y.%m.%d')
    query = dashboard.topboardEsQuery("now-2d/d", "now-1d/d")
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    res = es.search(index="gsp*", body=query, request_timeout=30) #url_crawlds 인덱스 문제로 임시 해결책 18-03-06
    for _row in res['aggregations']['types']['buckets']:
        if _row['key'] == "link_dna_tuple5":
            result['before_link'] = _row['doc_count']
            before_total += _row['doc_count']
        elif _row['key'] == "url_jobs":
            result['before_uri'] = _row['doc_count']
            before_total += _row['doc_count']
        elif _row['key'] == "url_crawleds":
            result['before_file'] = _row['doc_count']
            before_total += _row['doc_count']
    #endregion es 쿼리

    # result['bcode'] = 34
    # result['before_bcode'] = 11
    # result['spread'] = 35
    # result['before_spread'] = 21
    # result['before_cnc'] = 7
    # result['file'] = 1752
    # result['before_file'] = 1127
    result['totalTodayUriAnalysisCount'] = totalTodayUriAnalysisCount
    result['totalTodayMaliciousFileCount'] = totalTodayMaliciousFileCount

    result['todayAnalysisCountElasticsearch']= todayAnalysisCountElasticsearch
    result['totalAnalysisCountElasticsearch']= totalAnalysisCountElasticsearch

    result['totalYesterdayMaliciousUrlCount'] = totalYesterdayMaliciousUrlCount
    result['totalYesterdayMaliciousFileCount'] = totalYesterdayMaliciousFileCount

    result['totalTodayUriAnalysisCountNPC'] = totalTodayUriAnalySisCountNPC
    result['totalTodayUriAnalysisCountIMAS'] = totalTodayUriAnalySisCountIMAS

    result['totalTodayMaliciousFileCountNPC'] = totalTodayMaliciousFileCountNPC
    result['totalTodayMaliciousFileCountIMAS'] = totalTodayMaliciousFileCountIMAS
    result['totalTodayMaliciousFileCountZombieZero'] = totalTodayMaliciousFileCountZombieZero

    result['totalCollectedURLCount'] = totalCollectedURLCount
    result['todayCollectedURLCount'] = todayCollectedURLCount


    result['totalCrawledElementCount'] = totalCrawledElementCount
    result['todayCrawledElementCount'] = todayCrawledElementCount

    result['todayMaliciousFileCountRDBMS'] = todayMaliciousFileCountRDBMS
    result['totalMaliciousFileCountRDBMS'] = totalMaliciousFileCountRDBMS
    result['cnc_before'] = 13

    result['total'] = total
    result['before_total'] = before_total


    return json.dumps(result)


@blueprint_page.route('/getLineChartModif')
def getLineChartDataModif():
    query = dashboard.linechartQuery
    results = db_session.execute(query)
    results_list = []
    for _row in results:
        results_list.append(_row)

    now = datetime.datetime.now()
    timetable = []
    chartdata = OrderedDict()
    series = []

    for _dd in range(0,10):
        _now = datetime.datetime.now() - datetime.timedelta(days=9) + datetime.timedelta(days=_dd)
        _series = dict()
        _series['xaxis'] = _now.strftime('%Y-%m-%d')
        _series['date'] = _now.strftime('%m월%d일')

        isCncExists = False
        isSpreadExists = False
        isCode = False

        for row in results_list:
            if row['date'] == _series['xaxis']:
                if row is not None:
                    if row['Code'] == '001':
                        isCncExists = True
                        _series['CNC'] = row['count']
                    elif row['Code'] == '003':
                        isSpreadExists = True
                        _series['spread'] = row['count']
                    elif row['Code'] == "-":
                        isCode = True
                        _series['bcode'] = row['count']

        if isCncExists != True:
            _series['CNC'] = 0
        if isSpreadExists != True:
            _series['spread'] = 0
        if isCode != True:
            _series['bcode'] = 0

        series.append(_series)

    chartdata['data'] = series
    result = chartdata
    return json.dumps(result)

@blueprint_page.route('/getBarChartModif')
def getBarChartDataModif():
    query = dashboard.barchartQuery
    results = db_session.execute(query)
    results_list = []
    for _row in results:
        results_list.append(_row)

    now = datetime.datetime.now()
    timetable = []
    chartdata = OrderedDict()
    series = []

    for _dd in range(0,10):
        _now = datetime.datetime.now() - datetime.timedelta(days=9) + datetime.timedelta(days=_dd)
        _series = dict()
        _series['xaxis'] = _now.strftime('%Y-%m-%d')
        _series['date'] = _now.strftime('%m월%d일')

        isExists = False

        for row in results_list:
            if row['date'] == _series['xaxis']:
                if row is not None:
                    isExists = True
                    count = row['count']
                    _series['value'] = int(count)

        if isExists != True:
            _series['value'] = 0

        series.append(_series)

    chartdata['data'] = series
    result = chartdata
    return json.dumps(result)

@blueprint_page.route('/getGridModif')
def getGridModif():
    query = dashboard.gridQuery
    results = db_session.execute(query)
    results_list = []
    for _row in results:
        dict_row = dict()
        dict_row['date'] = _row[0]
        dict_row['cnc'] = _row[1]
        dict_row['spread'] = _row[2]
        dict_row['bcode'] = _row[3]
        dict_row['total'] = _row[1] + _row[2] + _row[3]
        results_list.append(dict_row)

    return json.dumps(results_list,cls=DecimalEncoder)


# for _item in res['aggregations']['topn']['hits']['hits']:
#     _series = dict()
#     _series['xaxis'] = _item['_source']['cl_ip']
#     _series['yaxis'] = _item['_source']['cnt']
#     _series['avg'] = res['aggregations']['avg']['value']
#     _series['std_dev'] = res['aggregations']['ex_stats']['std_deviation_bounds']['upper']


@blueprint_page.route('/getWorldChartModif')
def getWorldChartModif():
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    timeSetting = request.args['timeSetting']
    edTime = parser.parse(timeSetting) + datetime.timedelta(days=1)
    str_dt = Local2UTC(parser.parse(timeSetting)).isoformat()
    end_dt = Local2UTC(edTime).isoformat()
    body = getWorldChartQuery(str_dt,end_dt, app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])
    res = es.search(index=app.config['ELASTICSEARCH_INDEX'], doc_type="analysis_results", body=body, request_timeout=30)

    mapData = []
    latlong = dict()
    i = 0

    for doc in res['aggregations']['group_by_country2']['buckets']:
        if doc['key'] == '':
            continue
        _nation = (_nation for _nation in nations if _nation["code"] == doc['key']).next()
        mapData.append({"code": doc['key'], "name": _nation['nation'], 'value': doc['doc_count'], 'color': colorlist[i]})
        if i >= colorlist.__len__()-1:
            i =  0
        else:
            i = i +1
        latlong[doc['key']] = { "latitude" : _nation['latitude'], "longitude" : _nation['longitude']}

    # mapData = []
    # latlong = dict()
    # mapData.append({"code": 'KR', "name": "korea", 'value': 6, 'color': colorlist[0]})
    # mapData.append({"code" : 'CN', "name" : "china", 'value' : 21, 'color' : colorlist[1] } )
    # mapData.append({"code": 'US', "name": "us", 'value': 7, 'color': colorlist[2]})
    # latlong['KR'] = { "latitude" : 37.00, "longitude" : 127.30 }
    # latlong['CN'] = {"latitude": 35.00, "longitude": 105.00}
    # latlong['US'] = {"latitude": 38.00, "longitude": -97.00}

    chartdata = OrderedDict()
    chartdata['latlong'] = latlong
    chartdata['mapData'] = mapData

    return json.dumps(chartdata)

colorlist = [
        '#eea638',
        '#d8854f',
        '#de4c4f',
        '#86a965',
        '#d8854f',
        '#8aabb0',
        '#eea638'
    ]