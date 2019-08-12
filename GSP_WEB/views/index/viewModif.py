#-*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import *
from collections import OrderedDict
import time

from dateutil import parser
from elasticsearch import Elasticsearch
from flask import request, render_template, Blueprint, json
from sqlalchemy import func

from GSP_WEB import login_required, db_session, app
from GSP_WEB.common.encoder.decimalEncoder import DecimalEncoder
from GSP_WEB.common.util.date_util import Local2UTC
# from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Nations import nations
from GSP_WEB.query.secure_log import getMaliciousCodeLogDataCountDashboard, \
    getMaliciousCodeStatisticsDataCountAggsByDays, getMaliciousCodeStatisticsDataCountAggsByMonths
from GSP_WEB.models.Rules_Crawl import Rules_Crawl

# from GSP_WEB.models.Rules_BlackList import Rules_BlackList
# from GSP_WEB.models.Rules_CNC import Rules_CNC
from GSP_WEB.models.malicious_info import malicious_info
from GSP_WEB.query import dashboard
from GSP_WEB.query.dashboard import *
from GSP_WEB.query.link_dna_board import link_dna_board
from GSP_WEB.query import dna_result
from GSP_WEB.views.dna.statistics import stat_list_important_data



import operator

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
    # end_dt = "now/d"
    # str_dt = "now-1d/d"
    end_dt = "now"
    str_dt = "now/d"

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
    # end_dt = "now/d"
    # str_dt = "now-1d/d"
    end_dt = "now"
    str_dt = "now/d"

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
    # end_dt = "now/d"
    # str_dt = "now-1d/d"
    end_dt = "now"
    str_dt = "now/d"


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
    # end_dt = "now/d"
    # str_dt = "now-1d/d"
    end_dt = "now"
    str_dt = "now/d"


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
    # end_dt = "now/d"
    # str_dt = "now-1d/d"
    end_dt = "now"
    str_dt = "now/d"

    if app.config["NEW_ES"]:
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

    else:
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

    if app.config["NEW_ES"]:
        dataFrom = {"match": {"data_from": {"query": device}}}
        analysisType = {"match": {"analysis_type": {"query": type}}}
        range = {"range": {"@timestamp": {"gt": str_dt, "lte": end_dt}}}

    else:
        dataFrom = {"match": {"data_from": {"query": device, "type": "phrase"}}}
        analysisType = {"match": {"analysis_type": {"query": type, "type": "phrase"}}}
        range = {"range": {"@timestamp": {"gt": str_dt, "lte": end_dt}}}


    # dataFrom = {"match" : {"data_from" : {"query":device, "type":"phrase"}}}
    # analysisType = {"match": {"analysis_type": {"query": type, "type": "phrase"}}}
    # range = { "range": {"@timestamp": {"gt": str_dt, "lte": end_dt}}}
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
    totalDistinctMD5Query = dashboard.topboardMaliciousTotalCountByMD5
    totalDistinctMD5Count = db_session.execute(totalDistinctMD5Query)

    totalMaliciousFileCountRDBMS = 0

    for idx, _row in enumerate(totalDistinctMD5Count):
        totalMaliciousFileCountRDBMS = _row if _row is not None else 0
        totalMaliciousFileCountRDBMS = totalMaliciousFileCountRDBMS[0] if totalMaliciousFileCountRDBMS is not 0 else 0
        if idx == 0:
            break

    # totalMaliciousFileCountRDBMS = maliciousCodeQueryResult
    maliciousCodeTodayQueryResult = malicious_info.query.filter(malicious_info.cre_dt.between(start_of_day, nowtime))
    todayMaliciousFileCountRDBMS = maliciousCodeTodayQueryResult.count()


    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    ##Total analysis URL and file count

    # query_type = "analysis_info"

    if app.config['NEW_ES']:
        idx = "gsp-*-analysis_info"
        query_type = "_doc"
    else:
        idx = "gsp-*"
        query_type = "analysis_info"

    doc = getMaliciousCodeLogDataCountDashboard(query_type)
    try:
        # res = es.count(index="gsp-*", doc_type=query_type, body=doc)
        res = es.count(index=idx, doc_type=query_type, body=doc)
        totalAnalysisCountElasticsearch = res['count']
    except Exception as e:
        totalAnalysisCountElasticsearch = 0

    doc = getMaliciousCodeLogDataCountDashboard(query_type, today=True)
    try:
        # res = es.count(index="gsp-*", doc_type=query_type, body=doc)
        res = es.count(index=idx, doc_type=query_type, body=doc)
        todayAnalysisCountElasticsearch = res['count']
    except Exception as e:
        todayAnalysisCountElasticsearch = 0

    ##Total finished crawled element count
    # query_type = "url_crawleds"
    if app.config["NEW_ES"]:
        idx = "gsp-*-url_crawleds"
        query_type = "_doc"
    else:
        idx = "gsp-*"
        query_type = "url_crawleds"

    doc = Rules_Crawl.getCrawlCountDashboard()
    try:
        # res = es.count(index="gsp-*", doc_type=query_type, body=doc)
        res = es.count(index=idx, doc_type=query_type, body=doc)
        totalCrawledElementCount = res['count']
    except Exception as e:
        totalCrawledElementCount = 0
    ##Today crawled element count
    doc = Rules_Crawl.getCrawlCountDashboard(today=True)
    try:
        # res = es.count(index="gsp-*", doc_type=query_type, body=doc)
        res = es.count(index=idx, doc_type=query_type, body=doc)
        todayCrawledElementCount = res['count']
    except Exception as e:
        todayCrawledElementCount = 0

    ##Total collected URL and Today collected URLs.
    # query_type = "url_jobs"
    if app.config["NEW_ES"]:
        idx = "gsp-*-url_jobs"
        query_type = "_doc"
    else:
        idx = "gsp-*"
        query_type = "url_jobs"

    doc = Rules_Crawl.getCrawlCountDashboard()
    try:
        res = es.count(index=idx, doc_type=query_type, body=doc, request_timeout=120)
        totalCollectedURLCount = res['count']
    except Exception as e:
        totalCollectedURLCount = 0



    doc = Rules_Crawl.getCrawlCountDashboard(today=True)
    try:
        # res = es.count(index="gsp-*", doc_type=query_type, body=doc, request_timeout=360)
        res = es.count(index=idx, doc_type=query_type, body=doc, request_timeout=360)
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
    if app.config["NEW_ES"]:
        idx = "gsp-*-link_dna"
        query_type = "_doc"
    else:
        idx = "gsp-*"
        query_type = "link_dna"

    if app.config["NEW_ES"]:
        print "No link Count"
    else:
        # query_type = "link_dna"
        NFdoc = dashboard.DashboardTotalLinkCount("flag_list")
        try:
            # res = es.count(index="gsp-*", doc_type=query_type, body=NFdoc, request_timeout=360)
            res = es.count(index=idx, doc_type=query_type, body=NFdoc, request_timeout=360)
            NetflowCount = res['count']
        except Exception as e:
            NetflowCount = 0

        ##Traffic  total count
        TRdoc = dashboard.DashboardTotalLinkCount("payload")
        try:
            res = es.count(index="gsp-*", doc_type=query_type, body=TRdoc, request_timeout=360)
            TrafficCount = res['count']
        except Exception as e:
            TrafficCount = 0

        ##IDS and APT sub counters to get Syslog count
        idsdoc = dashboard.DashboardTotalLinkCount("ids_*")
        try:
            res = es.count(index="gsp-*", doc_type=query_type, body=idsdoc, request_timeout=360)
            idsCount = res['count']
        except Exception as e:
            idsCount = 0

        aptdoc = dashboard.DashboardTotalLinkCount("apt_*")
        try:
            res = es.count(index="gsp-*", doc_type=query_type, body=aptdoc, request_timeout=360)
            aptCount = res['count']
        except Exception as e:
            aptCount = 0

        # Total syslog count
        SyslogCount = idsCount + aptCount
        totalCollectedLinkCount = NetflowCount + TrafficCount + SyslogCount
        totalCollectedLinkDictionary = {"Netflow": NetflowCount, "Traffic": TrafficCount, "Syslog": SyslogCount}

        highestDNANameTotal = max(totalCollectedLinkDictionary.iteritems(), key=operator.itemgetter((1)))[0]
        highestDNAValueTotal = max(totalCollectedLinkDictionary.iteritems(), key=operator.itemgetter((1)))[1]

        ## Dashboard Link DNA count. Today count second.

        query_type = "link_dna"
        NFdoc = dashboard.DashboardTotalLinkCount("flag_list", today=True)
        try:
            res = es.count(index="gsp-*", doc_type=query_type, body=NFdoc, request_timeout=360)
            NetflowCount = res['count']
        except Exception as e:
            NetflowCount = 0

        ##Traffic  total count
        TRdoc = dashboard.DashboardTotalLinkCount("payload", today=True)
        try:
            res = es.count(index="gsp-*", doc_type=query_type, body=TRdoc, request_timeout=360)
            TrafficCount = res['count']
        except Exception as e:
            TrafficCount = 0

        ##IDS and APT sub counters to get Syslog count
        idsdoc = dashboard.DashboardTotalLinkCount("ids_*", today=True)
        try:
            res = es.count(index="gsp-*", doc_type=query_type, body=idsdoc, request_timeout=360)
            idsCount = res['count']
        except Exception as e:
            idsCount = 0

        aptdoc = dashboard.DashboardTotalLinkCount("apt_*", today=True)
        try:
            res = es.count(index="gsp-*", doc_type=query_type, body=aptdoc, request_timeout=360)
            aptCount = res['count']
        except Exception as e:
            aptCount = 0

        ##Total syslog count
        SyslogCount = idsCount + aptCount
        todayCollectedLinkCount = NetflowCount + TrafficCount + SyslogCount
        todayCollectedLinkDictionary = {"Netflow": NetflowCount, "Traffic": TrafficCount, "Syslog": SyslogCount}

        highestDNANameToday = max(todayCollectedLinkDictionary.iteritems(), key=operator.itemgetter((1)))[0]
        highestDNAValueToday = max(todayCollectedLinkDictionary.iteritems(), key=operator.itemgetter((1)))[1]

        ##Link analysis query
        linkAnalysisCountTotal = 0
        linkAnalysisCountToday = 0
        link_dna_doc_Total = link_dna_board.getLinkDnaCount()
        query_type = "link_dna"
        try:
            res = es.count(index="gsp-link_dna", doc_type=query_type, body=link_dna_doc_Total, request_timeout=360)
            linkAnalysisCountTotal = res['count']
        except Exception as e:
            linkAnalysisCountTotal = 0

        link_dna_doc_Today = link_dna_board.getLinkDnaCount(today=True)
        try:
            res = es.count(index="gsp-link_dna", doc_type=query_type, body=link_dna_doc_Today, request_timeout=360)
            linkAnalysisCountToday = res['count']
        except Exception as e:
            linkAnalysisCountToday = 0

        ##Link DNA Result query
        linkDNAResultCountTotal = 0
        linkDNAResultCountToday = 0
        link_result_doc_Total = dna_result.linkDNAResultCount()
        query_type = "dna_result"
        try:
            res = es.count(index="gsp-link_result", doc_type=query_type, body=link_result_doc_Total,
                           request_timeout=360)
            linkDNAResultCountTotal = res['count']
        except Exception as e:
            linkDNAResultCountTotal = 0

        link_result_doc_Today = dna_result.linkDNAResultCount(today=True)
        try:
            res = es.count(index="gsp-link_result", doc_type=query_type, body=link_result_doc_Today,
                           request_timeout=360)
            linkDNAResultCountToday = res['count']
        except Exception as e:
            linkDNAResultCountToday = 0

        ##Important DNAs
        try:
            importantDNA = stat_list_important_data()
            maxSectorCountItem = max(importantDNA, key=lambda x: x['sector_count'])
            minSectorCountItem = min(importantDNA, key=lambda x: x['sector_count'])
        except Exception as e:
            maxSectorCountItem = 0









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
    if app.config["NEW_ES"]:
        idx = "gsp-*-analysis_results"
        query_type = "_doc"
    else:
        idx = "gsp-*"
        query_type = "analysis_results"

    # if app.config["NEW_ES"]:
    #     idx = "gsp-*-analysis_results"
    #     query_type = "_doc"
    # else:
    #     idx = "gsp-*"
    #     query_type = "analysis_results"

    MUdoc = todayURLFileCount("uri", "NPC")
    # res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MUdoc)
    res = es.count(index=idx, doc_type=query, body=MUdoc)
    if app.config["NEW_ES"]:
        totalTodayUriAnalySisCountNPC = res['count']
    else:
        totalTodayUriAnalySisCountNPC = res['count']

    ##total tody uri analysis count NPC

    MUdoc = todayURLFileCount("uri", "IMAS")
    # res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MUdoc)
    res = es.count(index=idx, doc_type=query, body=MUdoc)
    totalTodayUriAnalySisCountIMAS = res['count']



    ##total today file analysis count NPC
    MFdoc = todayURLFileCount("file", "NPC")
    # res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    res = es.count(index=idx, doc_type=query, body=MFdoc)
    totalTodayMaliciousFileCountNPC = res['count']

    ##total today file analysis count IMAS
    MFdoc = todayURLFileCount("file", "IMAS")
    # res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    res = es.count(index=idx, doc_type=query, body=MFdoc)
    totalTodayMaliciousFileCountIMAS = res['count']

    ##total today file analysis count ZombieZero
    MFdoc = todayURLFileCount("file", "zombie zero")
    # res = es.count(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    res = es.count(index=idx, doc_type=query, body=MFdoc)
    totalTodayMaliciousFileCountZombieZero = res['count']


    # MFdoc = todayFileAnalysis(request, "file")
    # res = es.search(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    # totalTodayMaliciousFileCount = int(res['hits']['total'])



    ##total yesterday malicious url count

    MFdoc = dashboard.yesterdayUrlFileAnalysis(request, "uri")
    # res = es.search(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    res = es.search(index=idx, doc_type=query_type, body=MFdoc)
    totalYesterdayMaliciousUrlCount= int(res['hits']['total'])

    ##total yesterday malicious file count

    MFdoc = dashboard.yesterdayUrlFileAnalysis(request, "file")
    # res = es.search(index="gsp*" + "", doc_type="analysis_results", body=MFdoc)
    res = es.search(index=idx, doc_type=query_type, body=MFdoc)
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

    result['totalCollectedLink'] = 0
    result['todayCollectedLink'] = 0

    result['highestDNANameTotal'] = 0
    result['highestDNAValueTotal'] = 0

    result['highestDNANameToday'] = 0
    result['highestDNAValueToday'] = 0

    result['highestImportantDNATotalCount'] = 0
    result['highestImportantDNAWhitelistedCount'] = 0

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
    if app.config["NEW_ES"]:
        query = dashboard.NewtopboardEsQuery("now-1d/d", "now/d")
    else:
        query = dashboard.topboardEsQuery("now-1d/d", "now/d")
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])

    if app.config["NEW_ES"]:
        indices = ['gsp-*-link_dna_tuple5', 'gsp-*-url_jobs', 'gsp-*-url_crawleds']
        for idx in indices:
            res = es.search(index=idx, body=query, request_timeout=30)  # url_crawlds 인덱스 문제로 임시 해결책 18-03-06
            total += res["hits"]["total"]
    else:
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

    if app.config["NEW_ES"]:
        query = dashboard.NewtopboardEsQuery("now-2d/d", "now-1d/d")
    else:
        query = dashboard.topboardEsQuery("now-2d/d", "now-1d/d")

    # query = dashboard.topboardEsQuery("now-2d/d", "now-1d/d")
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])

    if app.config["NEW_ES"]:
        indices = ['gsp-*-link_dna_tuple5', 'gsp-*-url_jobs', 'gsp-*-url_crawleds']
        for idx in indices:
            res = es.search(index=idx, body=query, request_timeout=30)  # url_crawlds 인덱스 문제로 임시 해결책 18-03-06
            before_total += res["hits"]["total"]
    else:
        res = es.search(index="gsp*", body=query, request_timeout=30)
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


    # res = es.search(index="gsp*", body=query, request_timeout=30) #url_crawlds 인덱스 문제로 임시 해결책 18-03-06
    # for _row in res['aggregations']['types']['buckets']:
    #     if _row['key'] == "link_dna_tuple5":
    #         result['before_link'] = _row['doc_count']
    #         before_total += _row['doc_count']
    #     elif _row['key'] == "url_jobs":
    #         result['before_uri'] = _row['doc_count']
    #         before_total += _row['doc_count']
    #     elif _row['key'] == "url_crawleds":
    #         result['before_file'] = _row['doc_count']
    #         before_total += _row['doc_count']
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



    # result['highestDNANameTotal'] = highestDNANameTotal
    # result['highestDNAValueTotal'] = highestDNAValueTotal
    #
    # result['highestDNANameToday'] = highestDNANameToday
    # result['highestDNAValueToday'] = highestDNAValueToday
    if app.config["NEW_ES"]:
        result['highestImportantDNATotalCount'] = 0
        result['highestImportantDNAWhitelistedCount'] = 0
        result['highestImportantDNAName'] = 0

        result['totalLinkResultCount'] = 0
        result['todayLinkResultCount'] = 0

        result['totalLinkAnalysisCount'] = 0
        result['todayLinkAnalysisCount'] = 0

        result['totalCollectedLink'] = 0
        result['todayCollectedLink'] = 0

    else:
        #Link DNA removed and 0s are assigned to all those link related variables.
        # result['highestImportantDNATotalCount'] = maxSectorCountItem['sector_count']
        # result['highestImportantDNAWhitelistedCount'] = maxSectorCountItem["sector_count_whitelist"]
        # result['highestImportantDNAName'] = maxSectorCountItem['dna']
        #
        # result['totalLinkResultCount'] = linkDNAResultCountTotal
        # result['todayLinkResultCount'] = linkDNAResultCountToday
        #
        # result['totalLinkAnalysisCount'] = linkAnalysisCountTotal
        # result['todayLinkAnalysisCount'] = linkAnalysisCountToday
        #
        # result['totalCollectedLink'] = totalCollectedLinkCount
        # result['todayCollectedLink'] = todayCollectedLinkCount
        result['highestImportantDNATotalCount'] = 0
        result['highestImportantDNAWhitelistedCount'] = 0
        result['highestImportantDNAName'] = 0
        #
        result['totalLinkResultCount'] = 0
        result['todayLinkResultCount'] = 0
        #
        result['totalLinkAnalysisCount'] = 0
        result['todayLinkAnalysisCount'] = 0
        #
        result['totalCollectedLink'] = 0
        result['todayCollectedLink'] = 0



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


#Link DNA collection chart data provider
@blueprint_page.route('/getLineChartModif')
def getLineChartDataModif():
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])


    ## syslog subcount variables
    idsCount = 0
    aptCount = 0



    query_type = "link_dna"
    NFdoc = dashboard.DashboardDNALinkCountAggsByDays(field="flag_list", days=7)
    try:
        res = es.search(index="gsp-link*", doc_type=query_type, body=NFdoc, request_timeout=360)
        NetflowCountList = res['aggregations']['byday']['buckets']
    except Exception as e:
        NetflowCountList = []




    ##Traffic  total count ** there is a problem with this search. any of " proto, event_type, payload" works for search
    TRdoc = dashboard.DashboardDNALinkCountAggsByDays(field="payload", days=7)
    try:
        res = es.search(index="gsp-*", doc_type=query_type, body=TRdoc, request_timeout=360)
        TrafficCountList = res['aggregations']['byday']['buckets']
    except Exception as e:
        TrafficCountList = []

    ##IDS and APT sub counters to get Syslog count
    idsdoc = dashboard.DashboardDNALinkCountAggsByDays(field="ids_*", days=7)
    try:
        res = es.search(index="gsp-*", doc_type=query_type, body=idsdoc, request_timeout=360)
        idsCountList = res['aggregations']['byday']['buckets']
    except Exception as e:
        idsCountList = []

    aptdoc = dashboard.DashboardDNALinkCountAggsByDays("apt_cnc_sname", days=7)
    try:
        res = es.search(index="gsp-*", doc_type=query_type, body=aptdoc, request_timeout=360)
        aptCountList = res['aggregations']['byday']['buckets']
    except Exception as e:
        aptCountList = []


    for _dd in range(0,8):
        emptyDicElement = dict()
        emptyDicElement[u'key_as_string'] = 0
        emptyDicElement[u'key'] = 0
        emptyDicElement[u'doc_count'] = 0
        _now = datetime.datetime.now() - datetime.timedelta(days=7) + datetime.timedelta(days=_dd)
        if any(_now.strftime('%Y-%m-%d') in str(alist) for alist in NetflowCountList):
            pass
            # for tuple in :
            #     if tuple[0] == _now.strftime('%Y-%m'):
            #         dict_row['analyzed'] = tuple[1]

        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m-%d')
            NetflowCountList.append(emptyDicElement)


        if any(_now.strftime('%Y-%m-%d') in str(alist) for alist in TrafficCountList):
            pass
        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m-%d')
            TrafficCountList.append(emptyDicElement)


        if any(_now.strftime('%Y-%m-%d') in str(alist) for alist in idsCountList):
            pass
        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m-%d')
            idsCountList.append(emptyDicElement)

        if any(_now.strftime('%Y-%m-%d') in str(alist) for alist in aptCountList):
            pass
        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m-%d')
            aptCountList.append(emptyDicElement)


    # Total syslog count
    SyslogValueList = list()
    if idsCountList is not 0 or aptCountList is not 0:
        for idx, value in enumerate(idsCountList):
            SyslogValueList.append((value["doc_count"] +  idsCountList[idx]["doc_count"]))
    # SyslogCount = idsCount + aptCount
    # totalCollectedLinkCount = NetflowCount + TrafficCount + SyslogCount
    # totalCollectedLinkDictionary = {"Netflow": NetflowCount, "Traffic": TrafficCount, "Syslog": SyslogCount}





    query = dashboard.linechartQuery
    results = db_session.execute(query)
    results_list = []
    for _row in results:
        results_list.append(_row)

    now = datetime.datetime.now()
    timetable = []
    chartdata = OrderedDict()
    series = []

    for _dd in range(0,8):
        _now = datetime.datetime.now() - datetime.timedelta(days=7) + datetime.timedelta(days=_dd)
        _series = dict()
        _tempSeries = dict()
        _series['xaxis'] = _now.strftime('%Y-%m-%d')
        _series['date'] = _now.strftime('%m월%d일')

        isCncExists = False
        isSpreadExists = False
        isCode = False

        # for idx, row in enumerate(NetflowCountList):

            # if row['date'] == _series['xaxis']:
            #     if row is not None:
        if NetflowCountList:


            isCncExists = True
            _series['netflowCount'] = NetflowCountList[_dd]['doc_count']
        else:
            _series['netflowCount'] = 0

        if TrafficCountList:

            isSpreadExists = True
            _series['trafficCount'] = TrafficCountList[_dd]['doc_count']
        else:
            _series['trafficCount'] = 0

        if SyslogValueList:

            isCode = True
            _series['syslogCount'] = SyslogValueList[_dd]
        else:
            _series['syslogCount'] = 0


        if isCncExists != True:
            _series['netflowCount'] = 0
        if isSpreadExists != True:
            _series['trafficCount'] = 0
        if isCode != True:
            _series['syslogCount'] = 0

        series.append(_series)

    chartdata['data'] = series
    result = chartdata
    return json.dumps(result)

@blueprint_page.route('/getBarChartModif')
def getBarChartDataModif():
    importantDNAs = stat_list_important_data()

    query = dashboard.barchartQuery
    results = db_session.execute(query)
    results_list = []
    for _row in results:
        results_list.append(_row)

    now = datetime.datetime.now()
    timetable = []
    chartdata = OrderedDict()
    newchartdata = OrderedDict()
    series = []
    new_series = []



    for DNAelement in importantDNAs:
        _new_series = dict()
        _new_series['DNA_name'] = DNAelement['sector']
        _new_series['DNA_count'] = DNAelement['sector_count']

        new_series.append(_new_series)

    newchartdata['data'] = new_series
    newresult = newchartdata

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
    # result = chartdata
    result = newchartdata
    return json.dumps(result)

@blueprint_page.route('/getGridModif')
def getGridModif():
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    emptyDicElement = dict()
    emptyDicElement[u'key_as_string'] = 0
    emptyDicElement[u'key'] = 0
    emptyDicElement[u'doc_count'] = 0

    query_type = "link_dna"
    NFdoc = dashboard.DashboardDNALinkCountAggsByMonth(field="flag_list", months=2)
    try:
        res = es.search(index="gsp-link*", doc_type=query_type, body=NFdoc, request_timeout=360)
        NetflowCountList = res['aggregations']['bymonth']['buckets']
    except Exception as e:
        NetflowCountList = []

    if len(NetflowCountList) != 3:
        for idx in range(0, 3-len(NetflowCountList)):
            NetflowCountList.append(emptyDicElement)


    ##Traffic  total count ** there is a problem with this search. any of " proto, event_type, payload" works for search
    TRdoc = dashboard.DashboardDNALinkCountAggsByMonth(field="payload", months=2)
    try:
        res = es.search(index="gsp-*", doc_type=query_type, body=TRdoc, request_timeout=360)
        TrafficCountList = res['aggregations']['bymonth']['buckets']
    except Exception as e:
        TrafficCountList = []

    if len(TrafficCountList) != 3:
        for idx in range(0, 3-len(TrafficCountList)):
            TrafficCountList.append(emptyDicElement)

    ##IDS and APT sub counters to get Syslog count
    idsdoc = dashboard.DashboardDNALinkCountAggsByMonth(field="ids_*", months=2)
    try:
        res = es.search(index="gsp-*", doc_type=query_type, body=idsdoc, request_timeout=360)
        idsCountList = res['aggregations']['bymonth']['buckets']
    except Exception as e:
        idsCountList = []

    if len(idsCountList) != 3:
        for idx in range(0, 3-len(idsCountList)):
            idsCountList.append(emptyDicElement)

    aptdoc = dashboard.DashboardDNALinkCountAggsByMonth("apt_cnc_sname", months=2)
    try:
        res = es.search(index="gsp-*", doc_type=query_type, body=aptdoc, request_timeout=360)
        aptCountList = res['aggregations']['bymonth']['buckets']
    except Exception as e:
        aptCountList = []


    for idx in range(0,3):

        _now = datetime.datetime.now() - relativedelta(months=+(3-1)) + (relativedelta(months=+idx))
        emptyDicElement = dict()
        emptyDicElement[u'key_as_string'] = 0
        emptyDicElement[u'key'] = 0
        emptyDicElement[u'doc_count'] = 0
        _now = datetime.datetime.now() - datetime.timedelta(days=7) + datetime.timedelta(days=idx)
        if any(_now.strftime('%Y-%m') in str(alist) for alist in NetflowCountList):
            pass
            # for tuple in :
            #     if tuple[0] == _now.strftime('%Y-%m'):
            #         dict_row['analyzed'] = tuple[1]

        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m')
            NetflowCountList.append(emptyDicElement)

        if any(_now.strftime('%Y-%m') in str(alist) for alist in TrafficCountList):
            pass
            # for tuple in :
            #     if tuple[0] == _now.strftime('%Y-%m'):
            #         dict_row['analyzed'] = tuple[1]

        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m')
            TrafficCountList.append(emptyDicElement)


        if any(_now.strftime('%Y-%m') in str(alist) for alist in TrafficCountList):
            pass
            # for tuple in :
            #     if tuple[0] == _now.strftime('%Y-%m'):
            #         dict_row['analyzed'] = tuple[1]

        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m')
            TrafficCountList.append(emptyDicElement)

        if any(_now.strftime('%Y-%m') in str(alist) for alist in idsCountList):
            pass
            # for tuple in :
            #     if tuple[0] == _now.strftime('%Y-%m'):
            #         dict_row['analyzed'] = tuple[1]

        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m')
            idsCountList.append(emptyDicElement)

        if any(_now.strftime('%Y-%m') in str(alist) for alist in aptCountList):
            pass
            # for tuple in :
            #     if tuple[0] == _now.strftime('%Y-%m'):
            #         dict_row['analyzed'] = tuple[1]

        else:
            emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m')
            aptCountList.append(emptyDicElement)



    if len(idsCountList) != 3:

        for idx in range(0, 3 - len(idsCountList)):

            idsCountList.append(emptyDicElement)


        # Total syslog count
    SyslogValueList = list()
    if idsCountList:

        for idx, value in enumerate(idsCountList):

            SyslogValueList.append((value["doc_count"] + aptCountList[idx]["doc_count"]))

    results_list = []

    for idx in range(0,3):

        _now = datetime.datetime.now() - relativedelta(months=+(3-1)) + (relativedelta(months=+idx))
        dict_row = dict()
        dict_row['date'] = _now.strftime('%Y-%m')
        if NetflowCountList:
            dict_row['Netflow'] = NetflowCountList[idx]['doc_count']
        else:
            dict_row['Netflow'] = 0

        if SyslogValueList:
            dict_row['Syslog'] = SyslogValueList[idx]
        else:
            dict_row['Syslog'] = 0

        if TrafficCountList:
            dict_row['Traffic'] = TrafficCountList[idx]['doc_count']
        else:
            dict_row['Traffic'] = 0


        dict_row['total'] = NetflowCountList[idx]['doc_count'] + SyslogValueList[idx] + TrafficCountList[idx]['doc_count']
        results_list.append(dict_row)

    query = dashboard.gridQuery
    results = db_session.execute(query)

    # for _row in results:
    #     dict_row = dict()
    #     dict_row['date'] = _row[0]
    #     dict_row['cnc'] = _row[1]
    #     dict_row['spread'] = _row[2]
    #     dict_row['bcode'] = _row[3]
    #     dict_row['total'] = _row[1] + _row[2] + _row[3]
    #     results_list.append(dict_row)

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


##
##1st chart of the 1st line and stacked bar chart graphs for file/url collection status chart
@blueprint_page.route('/getLineChartModifMaliciousCodeInfoDaily')
def getLineChartDataModifMaliciousCodeInfoDaily():


    chartdata = OrderedDict()
    dataResult = []
    urlCollectionList = []
    fileCollectionList = []

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    if app.config["NEW_ES"]:
        idx = "gsp-*-url_jobs"
        query_type = "_doc"
    else:
        query_type = "url_jobs"

    # query_type = "url_jobs"
    doc = Rules_Crawl.urlCollectionStatisticsByDailyAggregation(query_type, days=7)
    try:
        if app.config["NEW_ES"]:
            res = es.search(index=idx, doc_type=query_type, body=doc, request_timeout=360)
        else:
            res = es.search(index="gsp*", doc_type=query_type, body=doc, request_timeout=360)

        # res = es.search(index="gsp*", doc_type=query_type, body=doc, request_timeout=360)
        urlCollectionList = res['aggregations']['byday']['buckets']
    except Exception as e:
        urlCollectionList = []

    if app.config["NEW_ES"]:
        idx = "gsp-*-url_crawleds"
        query_type = "_doc"
    else:
        query_type = "url_crawleds"

    # query_type = "url_crawleds"
    docFileCollection = Rules_Crawl.urlCollectionStatisticsByDailyAggregation(query_type, days=7)
    try:
        if app.config["NEW_ES"]:
            res = es.search(index=idx, doc_type=query_type, body=docFileCollection, request_timeout=360)
        else:
            res = es.search(index="gsp*", doc_type=query_type, body=docFileCollection, request_timeout=360)

        # res = es.search(index="gsp*", doc_type=query_type, body=docFileCollection, request_timeout=360)
        fileCollectionList = res['aggregations']['byday']['buckets']
    except Exception as e:
        fileCollectionList = []

    if urlCollectionList:
        for adict in urlCollectionList:
            for k,v in adict.iteritems():
                if k == 'key_as_string':
                    # print datetime.datetime.strptime(adict[k], "%Y-%m-%dT%H:%M:%S.%fZ")
                    DateTimeObject = datetime.datetime.strptime(adict[k], "%Y-%m-%dT%H:%M:%S.%fZ")
                    newDateFormat = ''
                    # date_string = newFormattedDate.strptime("%Y-%m-%d")
                    day = DateTimeObject.strftime("%d")
                    month = DateTimeObject.strftime("%m")
                    year = DateTimeObject.strftime("%Y")
                    newDateFormat = str(year)+"-"+str(month)+"-"+str(day)

                    # newFormattedDate.strptime("%Y-%m-%d")
                    adict[k] = newDateFormat


                    # adict[k] = newFormattedDate



    if fileCollectionList:
        for adict in fileCollectionList:
            for k, v in adict.iteritems():
                if k == 'key_as_string':
                    DateTimeObject = datetime.datetime.strptime(adict[k], "%Y-%m-%dT%H:%M:%S.%fZ")
                    newDateFormat = ''
                    # date_string = newFormattedDate.strptime("%Y-%m-%d")
                    day = DateTimeObject.strftime("%d")
                    month = DateTimeObject.strftime("%m")
                    year = DateTimeObject.strftime("%Y")
                    newDateFormat = str(year) + "-" + str(month) + "-" + str(day)

                    # newFormattedDate.strptime("%Y-%m-%d")
                    adict[k] = newDateFormat




    for _dd in range(0,7):
        _now = datetime.datetime.now() - datetime.timedelta(days=6) + datetime.timedelta(days=_dd)
        _series = dict()
        _series['xaxis'] = _now.strftime('%Y-%m-%d')
        _series['date'] = _now.strftime('%m월%d일')

        if urlCollectionList:


            for aDict in urlCollectionList:
                if aDict['key_as_string'] == _series['xaxis']:
                    _series['totalUrlCollectionCount'] = aDict['doc_count']


            # if TotalMalFileCountsDailyList[_dd]['doc_count']:
            #     _series['TotalDailyMalFileCount'] = TotalMalFileCountsDailyList[_dd]['doc_count']
            # else:
            #     _series['TotalDailyMalFileCount'] = 0

        else:
            _series['totalUrlCollectionCount'] = 0


        if fileCollectionList:

            for aDict in fileCollectionList:
                if aDict['key_as_string'] == _series['xaxis']:
                    _series['totalFileCollectionCount'] = aDict['doc_count']

        #     if TotalFileCountsDailyList[_dd]['doc_count']:
        #         _series['TotalDailyFileCount'] = TotalFileCountsDailyList[_dd]['doc_count']
        #     else:
        #         _series['TotalDailyFileCount'] = 0
        #
        else:
            _series['totalFileCollectionCount'] = 0

        if not _series.has_key("totalUrlCollectionCount"):
            _series["totalUrlCollectionCount"] = 0

        if not _series.has_key('totalFileCollectionCount'):
            _series["totalFileCollectionCount"] = 0

        dataResult.append(_series)
    ##Elasticsearch code to URL/File collection statistics graph.
    # es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    #
    # ## syslog subcount variables
    # idsCount = 0
    # aptCount = 0
    #
    # query_type = "link_dna"
    # NFdoc = dashboard.DashboardDNALinkCountAggsByDays(field="flag_list", days=7)
    # try:
    #     res = es.search(index="gsp-link*", doc_type=query_type, body=NFdoc, request_timeout=360)
    #     NetflowCountList = res['aggregations']['byday']['buckets']
    # except Exception as e:
    #     NetflowCountList = []



    ## Malware detect by each collection point from MySQL.
    # query = dashboard.lineChartMaliciousCodeWithCollection_Point_imas
    # imas_results = db_session.execute(query)
    # imas_results_list = []
    # for _row in imas_results:
    #     imas_results_list.append(_row)
    #
    # query = dashboard.lineChartMaliciousCodeWithCollection_Point_Zombie
    # zombie_results = db_session.execute(query)
    # zombie_results_list = []
    # for _row in zombie_results:
    #     zombie_results_list.append(_row)
    #
    # now = datetime.datetime.now()
    # timetable = []
    # chartdata = OrderedDict()
    # series = []
    # emptyRowTuple = []
    #
    # for _dd in range(0,8):
    #     _now = datetime.datetime.now() - datetime.timedelta(days=7) + datetime.timedelta(days=_dd)
    #     _series = dict()
    #     _tempSeries = dict()
    #     _series['xaxis'] = _now.strftime('%Y-%m-%d')
    #     _series['date'] = _now.strftime('%m월%d일')
    #
    #
    #
    #     ##Imas count
    #     if any(_now.strftime('%Y-%m-%d') in str(alist) for alist in imas_results_list):
    #         pass
    #
    #
    #     else:
    #         emptyRowTuple = []
    #         emptyRowTuple = (unicode(_now.strftime('%Y-%m-%d')), 0, u'imas')
    #         # for row in imas_results_list:
    #         #     imas_result_date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
    #
    #         imas_results_list = [emptyRowTuple] + imas_results_list
    #
    #     ##Zombiezero count
    #     if any(_now.strftime('%Y-%m-%d') in str(alist) for alist in zombie_results_list):
    #         pass
    #
    #
    #     else:
    #         emptyRowTuple = []
    #         emptyRowTuple = (unicode(_now.strftime('%Y-%m-%d')), 0, u'zombiezero')
    #         zombie_results_list = [emptyRowTuple] + zombie_results_list
    #
    #
    #     # if GSP_results_list:
    #     #     for aResult in GSP_results_list:
    #     #         _series['count'] =  aResult[1]
    #
    # imas_results_list.sort(key=lambda x: time.mktime(time.strptime(x[0], "%Y-%m-%d")))
    # zombie_results_list.sort(key =lambda x: time.mktime(time.strptime(x[0], "%Y-%m-%d")))
    #
    #
    # for idx in range(0, 8):
    #     _new_series = dict()
    #     _new_series['date'] = imas_results_list[idx][0]
    #     _new_series['imas_count'] = imas_results_list[idx][1]
    #     _new_series['imas_detection_point'] = imas_results_list[idx][2]
    #     _new_series['zombie_count'] = zombie_results_list[idx][1]
    #     _new_series['zombie_detection_point'] = zombie_results_list[idx][2]
    #     series.append(_new_series)


    # es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    #
    #
    # ## syslog subcount variables
    # idsCount = 0
    # aptCount = 0
    #
    # query_type = "analysis_info"
    # analysisInfodoc = dashboard.DashboardMalCodeCountAggsByDays(days=9)
    # try:
    #     res = es.search(index="gsp-*", doc_type=query_type, body=analysisInfodoc, request_timeout=360)
    #     MaliciousAnalysisCountList = res['aggregations']['byday']['buckets']
    # except Exception as e:
    #     MaliciousAnalysisCountList = []
    #
    # for _dd in range(0,9):
    #     emptyDicElement = dict()
    #     emptyDicElement[u'key_as_string'] = 0
    #     emptyDicElement[u'key'] = 0
    #     emptyDicElement[u'doc_count'] = 0
    #     _now = datetime.datetime.now() - datetime.timedelta(days=9) + datetime.timedelta(days=_dd)
    #     if any(_now.strftime('%Y-%m-%d') in str(alist) for alist in MaliciousAnalysisCountList):
    #         pass
    #         # for tuple in :
    #         #     if tuple[0] == _now.strftime('%Y-%m'):
    #         #         dict_row['analyzed'] = tuple[1]
    #
    #     else:
    #         emptyDicElement[u'key_as_string'] = _now.strftime('%Y-%m-%d')
    #         MaliciousAnalysisCountList.append(emptyDicElement)
    # # ##Traffic  total count ** there is a problem with this search. any of " proto, event_type, payload" works for search
    # # TRdoc = dashboard.DashboardDNALinkCountAggsByDays(field="proto*", days=9)
    # # try:
    # #     res = es.search(index="gsp-*", doc_type=query_type, body=TRdoc, request_timeout=360)
    # #     TrafficCountList = res['aggregations']['byday']['buckets']
    # # except Exception as e:
    # #     TrafficCountList = 0
    # #
    # # ##IDS and APT sub counters to get Syslog count
    # # idsdoc = dashboard.DashboardDNALinkCountAggsByDays(field="ids_*", days=9)
    # # try:
    # #     res = es.search(index="gsp-*", doc_type=query_type, body=idsdoc, request_timeout=360)
    # #     idsCountList = res['aggregations']['byday']['buckets']
    # # except Exception as e:
    # #     idsCountList = 0
    # #
    # # aptdoc = dashboard.DashboardDNALinkCountAggsByDays("apt_*", days=9)
    # # try:
    # #     res = es.count(index="gsp-*", doc_type=query_type, body=aptdoc, request_timeout=360)
    # #     aptCountList = res['aggregations']['byday']['buckets']
    # # except Exception as e:
    # #     aptCountList = 0
    # #
    # # # Total syslog count
    # # SyslogValueList = list()
    # # if idsCountList is not 0 or aptCountList is not 0:
    # #     for idx, value in enumerate(idsCountList):
    # #         SyslogValueList.append((value["doc_count"] +  idsCountList[idx]["doc_count"]))
    # # SyslogCount = idsCount + aptCount
    # # totalCollectedLinkCount = NetflowCount + TrafficCount + SyslogCount
    # # totalCollectedLinkDictionary = {"Netflow": NetflowCount, "Traffic": TrafficCount, "Syslog": SyslogCount}
    #
    #
    #
    #
    # query = dashboard.linechartQuery
    # results = db_session.execute(query)
    # results_list = []
    # for _row in results:
    #     results_list.append(_row)
    #
    # now = datetime.datetime.now()
    # timetable = []
    # chartdata = OrderedDict()
    # series = []
    #
    # for _dd in range(0,9):
    #     _now = datetime.datetime.now() - datetime.timedelta(days=9) + datetime.timedelta(days=_dd)
    #     _series = dict()
    #     _tempSeries = dict()
    #     _series['xaxis'] = _now.strftime('%Y-%m-%d')
    #     _series['date'] = _now.strftime('%m월%d일')
    #
    #     isCncExists = False
    #     isSpreadExists = False
    #     isCode = False
    #
    #     # for idx, row in enumerate(NetflowCountList):
    #
    #         # if row['date'] == _series['xaxis']:
    #         #     if row is not None:
    #     if MaliciousAnalysisCountList:
    #
    #
    #         isCncExists = True
    #         _series['analysisinfo_count'] = MaliciousAnalysisCountList[_dd]['doc_count']
    #     else:
    #         _series['analysisinfo_count'] = 0
    #
    #     # if TrafficCountList is not 0 or TrafficCountList is not None:
    #     #
    #     #     isSpreadExists = True
    #     #     _series['trafficCount'] = TrafficCountList[_dd]['doc_count']
    #     #
    #     # if SyslogValueList is not 0 or SyslogValueList is not None:
    #     #
    #     #     isCode = True
    #     #     _series['syslogCount'] = SyslogValueList[_dd]
    #
    #
    #     if isCncExists != True:
    #         _series['analysisinfo_count'] = 0
    #     # if isSpreadExists != True:
    #     #     _series['trafficCount'] = 0
    #     # if isCode != True:
    #     #     _series['syslogCount'] = 0
    #
    #     series.append(_series)

    chartdata['data'] = dataResult
    result = chartdata
    return json.dumps(result)

#2nd box of the 1st line to show statistics for malicious code
@blueprint_page.route('/getBarChartModifMalcode')
def getBarChartDataModifMalCode():
    # importantDNAs = stat_list_important_data()
    #Elasticsearch code to URL/File collection statistics graph.

    TotalFileCountsDailyList = []
    TotalMalFileCountsDailyList=[]



    chartdata = OrderedDict()
    dataResult = []

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    if app.config["NEW_ES"]:
        idx = "gsp-*-analysis_info"
        docT = "_doc"
        query_type = "analysis_info"
    else:
        idx = "gsp*"
        query_type = "analysis_info"

    # query_type = "analysis_info"
    doc = getMaliciousCodeStatisticsDataCountAggsByDays(query_type, days=7)
    try:
        if app.config["NEW_ES"]:
            res = es.search(index=idx, doc_type=docT, body=doc, request_timeout=360)
        else:
            res = es.search(index="gsp*", doc_type="analysis_info", body=doc, request_timeout=360)

        # res = es.search(index="gsp*", doc_type="analysis_info", body=doc, request_timeout=360)
        TotalFileCountsDailyList = res['aggregations']['byday']['buckets']
    except Exception as e:
        TotalFileCountsDailyList = []

    docMaliciousCode = getMaliciousCodeStatisticsDataCountAggsByDays(query_type, days=7, detectedMalFileCount="yes")
    try:
        if app.config["NEW_ES"]:
            res = es.search(index=idx, doc_type=docT, body=docMaliciousCode, request_timeout=360)
        else:
            res = es.search(index="gsp*", doc_type="analysis_info", body=docMaliciousCode, request_timeout=360)

        TotalMalFileCountsDailyList = res['aggregations']['byday']['buckets']
    except Exception as e:
        TotalMalFileCountsDailyList = []

    ##Date reformatting
    if TotalFileCountsDailyList:
        for adict in TotalFileCountsDailyList:
            for k,v in adict.iteritems():
                if k == 'key_as_string':
                    # print datetime.datetime.strptime(adict[k], "%Y-%m-%dT%H:%M:%S.%fZ")
                    DateTimeObject = datetime.datetime.strptime(adict[k], "%Y-%m-%dT%H:%M:%S.%fZ")
                    newDateFormat = ''
                    # date_string = newFormattedDate.strptime("%Y-%m-%d")
                    day = DateTimeObject.strftime("%d")
                    month = DateTimeObject.strftime("%m")
                    year = DateTimeObject.strftime("%Y")
                    newDateFormat = str(year)+"-"+str(month)+"-"+str(day)

                    # newFormattedDate.strptime("%Y-%m-%d")
                    adict[k] = newDateFormat


                    # adict[k] = newFormattedDate



    if TotalMalFileCountsDailyList:
        for adict in TotalMalFileCountsDailyList:
            for k, v in adict.iteritems():
                if k == 'key_as_string':
                    DateTimeObject = datetime.datetime.strptime(adict[k], "%Y-%m-%dT%H:%M:%S.%fZ")
                    newDateFormat = ''
                    # date_string = newFormattedDate.strptime("%Y-%m-%d")
                    day = DateTimeObject.strftime("%d")
                    month = DateTimeObject.strftime("%m")
                    year = DateTimeObject.strftime("%Y")
                    newDateFormat = str(year) + "-" + str(month) + "-" + str(day)

                    # newFormattedDate.strptime("%Y-%m-%d")
                    adict[k] = newDateFormat



    for _dd in range(0,7):
        _now = datetime.datetime.now() - datetime.timedelta(days=6) + datetime.timedelta(days=_dd)
        _series = dict()
        _series['xaxis'] = _now.strftime('%Y-%m-%d')
        _series['date'] = _now.strftime('%m월%d일')

        if TotalMalFileCountsDailyList:


            for aDict in TotalMalFileCountsDailyList:
                if aDict['key_as_string'] == _series['xaxis']:
                    _series['TotalDailyMalFileCount'] = aDict['doc_count']


            # if TotalMalFileCountsDailyList[_dd]['doc_count']:
            #     _series['TotalDailyMalFileCount'] = TotalMalFileCountsDailyList[_dd]['doc_count']
            # else:
            #     _series['TotalDailyMalFileCount'] = 0

        else:
            _series['TotalDailyMalFileCount'] = 0


        if TotalFileCountsDailyList:

            for aDict in TotalFileCountsDailyList:
                if aDict['key_as_string'] == _series['xaxis']:
                    _series['TotalDailyFileCount'] = aDict['doc_count']

        #     if TotalFileCountsDailyList[_dd]['doc_count']:
        #         _series['TotalDailyFileCount'] = TotalFileCountsDailyList[_dd]['doc_count']
        #     else:
        #         _series['TotalDailyFileCount'] = 0
        #
        else:
            _series['TotalDailyFileCount'] = 0

        if not _series.has_key("TotalDailyMalFileCount"):
            _series["TotalDailyMalFileCount"] = 0

        if not _series.has_key('TotalDailyFileCount'):
            _series["TotalDailyFileCount"] = 0

        dataResult.append(_series)


    chartdata['data'] = dataResult
    result = chartdata
    return json.dumps(result)






    # query = dashboard.barchartMalwareTrendInfo
    # results = db_session.execute(query)
    # results_list = []
    # for _row in results:
    #     results_list.append(_row)
    #
    # now = datetime.datetime.now()
    # timetable = []
    # chartdata = OrderedDict()
    # # newchartdata = OrderedDict()
    # series = []
    # # new_series = []
    #
    #
    #
    # for idx, tuple in enumerate(results_list):
    #     _new_series = dict()
    #     _new_series['detect_info'] = tuple[0]
    #     _new_series['md5'] = tuple[1]
    #     _new_series['count'] = tuple[2]
    #
    #
    #     series.append(_new_series)
    #
    # chartdata['data'] = series
    # newresult = newchartdata

    # for _dd in range(0,10):
    #     _now = datetime.datetime.now() - datetime.timedelta(days=9) + datetime.timedelta(days=_dd)
    #     _series = dict()
    #     _series['xaxis'] = _now.strftime('%Y-%m-%d')
    #     _series['date'] = _now.strftime('%m월%d일')
    #
    #     isExists = False
    #
    #     for row in results_list:
    #         if row['date'] == _series['xaxis']:
    #             if row is not None:
    #                 isExists = True
    #                 count = row['count']
    #                 _series['value'] = int(count)
    #
    #     if isExists != True:
    #         _series['value'] = 0
    #
    #     series.append(_series)

    # chartdata['data'] = series
    # result = chartdata
    # # result = newchartdata
    # return json.dumps(result)


#Bottom table to show last 3 months amounts of malcode collection, file analysis request, and malicious detected files
@blueprint_page.route('/getGridModifTotalMalCodeByMonth')
def getGridModifTotalMalCodeByMonth():
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    # query_type = "analysis_info"
    # monthdoc = dashboard.DashboardMalCodeCountAggsByMonth(months=2)
    # try:
    #     if app.config["NEW_ES"]:
    #         idx = "gsp-*-analysis_info"
    #         docT = "_doc"
    #         res = es.search(index=idx, doc_type=docT, body=monthdoc, request_timeout=360)
    #     else:
    #         res = es.search(index="gsp-*", doc_type=query_type, body=monthdoc, request_timeout=360)
    #
    #     # res = es.search(index="gsp-*", doc_type=query_type, body=monthdoc, request_timeout=360)
    #     maliciousCodeAnalysisMonth = res['aggregations']['bymonth']['buckets']
    # except Exception as e:
    #     maliciousCodeAnalysisMonth = []
    #File collection counts by month
    if app.config["NEW_ES"]:
        idx = "gsp-*-url_crawleds"
        query_type = "_doc"
    else:
        query_type = "url_crawleds"

    # query_type = "url_crawleds"
    docFileCollection = Rules_Crawl.urlCollectionStatisticsByMonthlyAggregation(query_type, months=2)
    try:
        if app.config["NEW_ES"]:
            res = es.search(index=idx, doc_type=query_type, body=docFileCollection, request_timeout=360)
        else:
            res = es.search(index="gsp*", doc_type=query_type, body=docFileCollection, request_timeout=360)

        # res = es.search(index="gsp*", doc_type=query_type, body=docFileCollection, request_timeout=360)
        fileCollectionMonthlyList = res['aggregations']['byday']['buckets']
    except Exception as e:
        fileCollectionMonthlyList = []

    #Total file analysis request counts
    if app.config["NEW_ES"]:
        idx = "gsp-*-analysis_info"
        docT = "_doc"
        query_type = "analysis_info"
    else:
        idx = "gsp*"
        query_type = "analysis_info"

    #Total file analysis request counts
    doc = getMaliciousCodeStatisticsDataCountAggsByMonths(query_type, months=2)
    try:
        if app.config["NEW_ES"]:
            res = es.search(index=idx, doc_type=docT, body=doc, request_timeout=360)
        else:
            res = es.search(index="gsp*", doc_type="analysis_info", body=doc, request_timeout=360)

        # res = es.search(index="gsp*", doc_type="analysis_info", body=doc, request_timeout=360)
        TotalFileAnalysisRequestCountsMonthlyList = res['aggregations']['byday']['buckets']
    except Exception as e:
        TotalFileAnalysisRequestCountsMonthlyList = []

    #Total file malicious detected counts
    docMaliciousCode = getMaliciousCodeStatisticsDataCountAggsByMonths(query_type, months=2, detectedMalFileCount="yes")
    try:
        if app.config["NEW_ES"]:
            res = es.search(index=idx, doc_type=docT, body=docMaliciousCode, request_timeout=360)
        else:
            res = es.search(index="gsp*", doc_type="analysis_info", body=docMaliciousCode, request_timeout=360)

        TotalFileMaliciousDetectedCountsMonthlyList = res['aggregations']['byday']['buckets']
    except Exception as e:
        TotalFileMaliciousDetectedCountsMonthlyList = []





    # query = dashboard.barchartMaliciousCodeQuery
    # results = db_session.execute(query)
    # results_list = []
    # for _row in results:
    #     results_list.append(_row)
    #
    # now = datetime.datetime.now()
    # timetable = []
    # chartdata = OrderedDict()
    # # newchartdata = OrderedDict()
    # series = []
    # # new_series = []
    #
    # for idx, tuple in enumerate(results_list):
    #     _new_series = dict()
    #     _new_series['date'] = str(tuple[0])
    #     _new_series['count'] = tuple[1]
    #
    #     series.append(_new_series)
    # ##Traffic  total count ** there is a problem with this search. any of " proto, event_type, payload" works for search
    # TRdoc = dashboard.DashboardDNALinkCountAggsByMonth(field="proto*", months=2)
    # try:
    #     res = es.search(index="gsp-*", doc_type=query_type, body=TRdoc, request_timeout=360)
    #     TrafficCountList = res['aggregations']['bymonth']['buckets']
    # except Exception as e:
    #     TrafficCountList = 0

    # ##IDS and APT sub counters to get Syslog count
    # idsdoc = dashboard.DashboardDNALinkCountAggsByMonth(field="ids_*", months=2)
    # try:
    #     res = es.search(index="gsp-*", doc_type=query_type, body=idsdoc, request_timeout=360)
    #     idsCountList = res['aggregations']['bymonth']['buckets']
    # except Exception as e:
    #     idsCountList = 0
    #
    # aptdoc = dashboard.DashboardDNALinkCountAggsByMonth("apt_*", months=2)
    # try:
    #     res = es.count(index="gsp-*", doc_type=query_type, body=aptdoc, request_timeout=360)
    #     aptCountList = res['aggregations']['bymonth']['buckets']
    # except Exception as e:
    #     aptCountList = 0
    #
    #     # Total syslog count
    # SyslogValueList = list()
    # if idsCountList is not 0 or aptCountList is not 0:
    #
    #     for idx, value in enumerate(idsCountList):
    #
    #         SyslogValueList.append((value["doc_count"] + idsCountList[idx]["doc_count"]))

    return_list = []

    for idx, _row in enumerate(fileCollectionMonthlyList):

        _now = datetime.datetime.now() - relativedelta(months=+(len(fileCollectionMonthlyList)-1)) + (relativedelta(months=+idx))
        dict_row = dict()
        dict_row['date'] = _now.strftime('%Y-%m')
        dict_row['collection'] = _row['doc_count']
        dict_row['analysisRequest'] = TotalFileAnalysisRequestCountsMonthlyList[idx]['doc_count']
        dict_row['maliciousDetected'] =  TotalFileMaliciousDetectedCountsMonthlyList[idx]['doc_count']
        # if any(_now.strftime('%Y-%m') in str(alist) for alist in results_list):
        #     for tuple in results_list:
        #         if tuple[0] == _now.strftime('%Y-%m'):
        #             dict_row['analyzed'] = tuple[1]
        #
        # else:
        #     dict_row['analyzed'] = 0

        # dict_row['Traffic'] = TrafficCountList[idx]['doc_count']
        # dict_row['total'] = _row['doc_count'] + dict_row['analyzed']
        return_list.append(dict_row)

    # query = dashboard.gridQuery
    # results = db_session.execute(query)

    # for _row in results:
    #     dict_row = dict()
    #     dict_row['date'] = _row[0]
    #     dict_row['cnc'] = _row[1]
    #     dict_row['spread'] = _row[2]
    #     dict_row['bcode'] = _row[3]
    #     dict_row['total'] = _row[1] + _row[2] + _row[3]
    #     results_list.append(dict_row)

    return json.dumps(return_list,cls=DecimalEncoder)







colorlist = [
        '#eea638',
        '#d8854f',
        '#de4c4f',
        '#86a965',
        '#d8854f',
        '#8aabb0',
        '#eea638'
    ]