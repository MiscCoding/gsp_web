#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil import parser
from elasticsearch import Elasticsearch
from flask import json


def getStatisticsEachElementWhiteListCount(dnaElement, whitelist=False):

    query =  {
        "query": {
            "bool": {
                "must": [

                ]
            }
        },
        "size" : 0,
        "from" : 0,
        "aggs" :{

        }
    }
    if (whitelist == True):
        whiteListFieldChecker = {"exists": {"field": dnaElement + ".isWhiteListApplied"}}
        sourceNode = {"match": {dnaElement+".isWhiteListApplied": "false"}}
        query["query"]["bool"]["must"].append(whiteListFieldChecker)
        query["query"]["bool"]["must"].append(sourceNode)


    query["aggs"][dnaElement] = {
          "terms" : {
                "field" : dnaElement + ".sector.keyword"
            }
    }



    # typeQuery = {"range": {"security_level": {"gte": 4}}}
    # query["query"]["bool"]["must"].append(typeQuery)


    return query

def getStatistics(dna_list, whitelist=False):

    query =  {
        "query": {
            "bool": {
                "must": [

                ],
                "should": [

                ]
            }
        },
        "size" : 0,
        "from" : 0,
        "aggs" :{

        }
    }


    for _dna in dna_list:
        if (whitelist == True):
            sourceNode = {"match": {_dna.dna_name+".isWhiteListApplied": "true"}}
            query["query"]["bool"]["should"].append(sourceNode)

        query["aggs"][_dna.dna_name] = {
            "terms" : {
                "field" : _dna.dna_name + ".sector.keyword"
            }
        }



    # typeQuery = {"range": {"security_level": {"gte": 4}}}
    # query["query"]["bool"]["must"].append(typeQuery)

    return query

def getAnalysisResult( request):
    per_page = int(request.form.get('perpage'))
    start_idx = int(request.form.get('start'))
    search_type = request.form.get('search_type')
    src_ip = request.form.get('search_src_ip')
    dst_ip = request.form.get('search_dst_ip')
    search_dna = request.form.get('search_dna')
    search_dna_name = request.form.get('search_dna_name')
    search_sector = request.form.get('search_sector')
    whiteList = request.form.get('whiteList')
    showWhiteListFalse = request.form.get('showWhiteListFalse')


    if per_page == None:
        per_page = int(request.form['perpage'])
    if start_idx == None:
        start_idx = int(request.form['start'])
    page_no = int(start_idx / per_page)


    doc = {
        "query": {
            "bool": {
                "should": [
                ],
                "must": [

                ]
            }
        },
        "size": per_page,
        "from": start_idx
    }

    if src_ip is not None and src_ip != "":
        sourceNode = {"term": {"src_ip.keyword": src_ip}}
        doc["query"]["bool"]["must"].append(sourceNode)

    if dst_ip is not None and dst_ip != "":
        sourceNode = {"term": {"dst_ip.keyword": dst_ip}}
        doc["query"]["bool"]["must"].append(sourceNode)

    if ( search_dna != ""):
        sourceNode = {"exists" : {"field" : search_dna_name } }
        doc["query"]["bool"]["must"].append(sourceNode)

    if (search_sector != ""):
        sourceNode = {"term": { search_dna_name+".sector.keyword" : search_sector}}
        doc["query"]["bool"]["must"].append(sourceNode)

    if (whiteList == "true"):
        whiteListFieldChecker = {"exists": {"field": search_dna_name + ".isWhiteListApplied"}}
        if(showWhiteListFalse == 'true'):
            sourceNode = {"match": {search_dna_name + ".isWhiteListApplied": "false"}}
        else:
            sourceNode = {"match": {search_dna_name + ".isWhiteListApplied": whiteList}}
        doc["query"]["bool"]["must"].append(whiteListFieldChecker)
        doc["query"]["bool"]["must"].append(sourceNode)
        # sourceNode = {"term": {search_dna_name + ".sector.keyword": search_sector}}
        # doc["query"]["bool"]["must"].append(sourceNode)

    return doc



def linkDNAResultCount(today=False):

        end_dt = "now/d"
        str_dt = "now-1d/d"

        query = {
            "query": {
                "bool": {
                    "must": [

                    ],
                    "should": [

                    ]

                }

            }

        }

        if today is True:
            timeQuery = {"range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}}
            query["query"]["bool"]["must"].append(timeQuery)



        return query