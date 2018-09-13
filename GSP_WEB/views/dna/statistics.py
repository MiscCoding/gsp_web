#-*- coding: utf-8 -*-
import datetime

from elasticsearch import Elasticsearch
from flask import request, Response, render_template, Blueprint, json, make_response, g, session
from sqlalchemy import or_, and_

from GSP_WEB import db_session, login_required, app
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.DNA_Element import DNA_Element
from GSP_WEB.models.DNA_Schedule import DNA_Schedule
from GSP_WEB.query import dna_result

from GSP_WEB.views.dna import blueprint_page

@blueprint_page.route('/statistics', methods=['GET'])
#@login_required
def stat_view():
    #logUtil.addLog(request.remote_addr,1,'links > list ')
    #type_list = CommonCode.query.filter_by(GroupCode = 'raw_data_type').all()

    return render_template('dna/statistics.html')

@blueprint_page.route('/statistics/list', methods=['POST'])
def stat_list():
    #logUtil.addLog(request.remote_addr,1,'links > list ')
    #type_list = CommonCode.query.filter_by(GroupCode = 'raw_data_type').all()

    dnaList = list()
    dnaNames = list()
    whiteListedCountDict = dict()
    dnaScheduleListInUse = DNA_Schedule.query.filter(and_(DNA_Schedule.del_yn == "N")).with_entities(DNA_Schedule.dna_id).all()
    dnaScheduleListInUseInt = list()
    for x in dnaScheduleListInUse:
        dnaScheduleListInUseInt.append(x[0])

    dnaElementInUse = DNA_Element.query.filter(DNA_Element.id.in_(dnaScheduleListInUseInt)).all()

    dnaElementList = DNA_Element.query.filter(
        and_(DNA_Element.use_yn == 'Y', DNA_Element.del_yn == 'N')).all()

    for _dna in dnaElementList:
        dnaList.append(_dna)

    draw = int(request.form.get('draw'))
    doc = dna_result.getStatistics(dnaList)
    #docwhitelistValue = dna_result.getStatistics(dnaList, whitelist=True)

    # for _dna in dnaList:
    #     es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    #     docWhiteList = dna_result.getStatisticsEachElementWhiteList(str(_dna.dna_name), whitelist=True)
    #     countValue = es.search(index="gsp-link_result", doc_type="dna_result", body=docWhiteList, request_timeout=30)
       # whiteListedCountDict[str(_dna.dna_name), int(countValue['aggregations'][_dna.dna_name]["buckets"])]


    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': int(app.config['ELASTICSEARCH_PORT'])}])
    statList = es.search(index="gsp-link_result", doc_type="dna_result", body=doc, request_timeout=30)
    #statListWhiteList = es.search(index="gsp-link_result", doc_type="dna_result", body=docwhitelistValue, request_timeout=30)

    total = statList['hits']['total']
    totalLinkCount = getTotalLinkCount()
    #WhiteListCount = getTotalLinkCount(whiteList=True)

    resultData = list()
    dna_name_list = list()

    for _dna in dnaList:

        docWhitelistCount = dna_result.getStatisticsEachElementWhiteListCount(_dna.dna_name, whitelist=True)
        statListWhiteListCount = es.search(index="gsp-link_result", doc_type="dna_result", body=docWhitelistCount, request_timeout=30)
        agg = statList['aggregations'][_dna.dna_name]["buckets"]
        #aggWhiteList = statListWhiteList['aggregations'][_dna.dna_name]["buckets"]
        aggWhiteListCount = statListWhiteListCount['aggregations'][_dna.dna_name]["buckets"]
        _op_func = json.loads(_dna.operate_function)
        sector_list = _op_func["dna_name_list"]
        dna_count = 0

        for _dna_row in agg:
            dna_count += int(_dna_row['doc_count'])

        for _dna_row in agg:
            if index_of(_dna_row['key'], dna_name_list) == -1:
                dna_name_list.append(_dna_row['key'])

            isImportant = next((d['isImportantDNA'] for (index, d) in enumerate(sector_list) if d["dna_name"] == _dna_row['key']), None)
            isWhiteListApplied = next((d['isWhiteListApplied'] for (index, d) in enumerate(sector_list) if d["dna_name"] == _dna_row['key']), None)
            desc = next((d.get('desc') for (index, d) in enumerate(sector_list) if d["dna_name"] == _dna_row['key']),None)
            comment = next((d.get('comment') for (index, d) in enumerate(sector_list) if d["dna_name"] == _dna_row['key']),None)
            tempvalueWhiteCount = 0
            # for whiteListedRow in aggWhiteList:
            #     if whiteListedRow['key'] == _dna_row['key']:
            #         tempvalueWhiteCount[str(_dna_row['key'])] = int(whiteListedRow['doc_count'])
            #     else:
            #         tempvalueWhiteCount[str(_dna_row['key'])] = 0
            for whitelistRow in aggWhiteListCount:
                if _dna_row['key'] == whitelistRow["key"]:
                    tempvalueWhiteCount = whitelistRow['doc_count']

            dnaNames.append( _dna.dna_name)

            resultData.append({
                    "dna" : _dna.dna_name,
                    "dna_id" : _dna.id,
                    "dna_count" : dna_count,
                    "sector" : _dna_row['key'],
                    "sector_count" : _dna_row['doc_count'],
                    "sector_count_whitelist" : tempvalueWhiteCount,
                    "sector_percent" : float(_dna_row['doc_count'] * 100 / dna_count),
                    "total" : total,
                    "totalLinkCount" : totalLinkCount,
                    "isimportant" : isImportant,
                    "isWhiteListApplied" : isWhiteListApplied,
                    "desc" : desc,
                    "comment" : comment
            })


    unique_list = []
    #traverse for all elements
    for x in dnaNames:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = resultData.__len__()
    result["recordsFiltered"] = unique_list.__len__()
    result["dna_name_count"] = unique_list.__len__()
    result["data"] = resultData
    result["dna_count"] = dna_name_list.__len__()

    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

def getTotalLinkCount(whiteList=False):

    doc = {
        "query": {"bool": { "must": [] } }
        , "from": 0, "size": 0
    }

    if (whiteList == True):
        whitelistFieldName = "isWhiteListApplied"
        whitelistFieldBooleanValue = "True"
        keyword = {"term" : {whitelistFieldName: whitelistFieldBooleanValue}}
        doc["query"]["bool"]["must"].append(keyword)

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    res = es.search(index="gsp-link_dna" + "", doc_type="link_dna", body=doc, request_timeout=60)

    return res["hits"]["total"]

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1