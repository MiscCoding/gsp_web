#-*- coding: utf-8 -*-
from flask import json


def GetSearchByColumnWithLimits(columnName, eachCount):
    doc = {
        "size" : 0,
        "query" : {
            "bool": {
                "should" : [
                    {"prefix": {"src_ip" : "8.8.8.8" } },
                    { "prefix" : { "src_ip" : "192.168.10.134"} }
                ] }
        },
        "aggs": {
            "src_ip": {
                "filter": {

                },
                "aggs": {
                    "group_result": {
                        "terms": {
                            "field": columnName +".keyword",
                            "size": eachCount
                        },
                        "aggs": {
                            "top": {
                                "top_hits": {
                                    "size": eachCount
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return doc

def CreateFilterQuery(operator, column, value):

    if operator == ">" :
        esOperator = "gt"
    elif operator == ">=" :
        esOperator = "gte"
    elif operator == "<" :
        esOperator = "lt"
    elif operator == "<=" :
        esOperator = "lte"

    if operator == '=' or operator == '!=':
        equalQuery = { "term" : { column : value } }
        return equalQuery
    if operator == "like" or operator == "notlike":
        equalQuery = {"wildcard": {column: value}}
        return equalQuery
    else:
        rangeQuery = { "range":  {  column : { esOperator : value } } }
        return rangeQuery

def CreateFilterQuery_IP(operator, column, value):
    iplist = value.split(',')

    equalQuery = {
				"bool" : {
				"should" :
				[

				]
				}
			}
    for _ip in iplist:
        rowQuery = { "term": {column : _ip.strip()} }
        equalQuery["bool"]["should"].append(rowQuery)

    return equalQuery

def CreateFilterQuery_AdditionalIP(value):
    iplist = value

    equalQuery = {
				"bool" : {
				"should" :
				[

				]
				}
			}

    rowSvrQuery = {"terms": {"src_ip": []}}
    rowClQuery = {"terms": {"dst_ip": []}}

    for _ip in iplist:
        rowSvrQuery["terms"]["src_ip"].append(_ip)
        rowClQuery["terms"]["dst_ip"].append(_ip)

    equalQuery["bool"]["should"].append(rowSvrQuery)
    equalQuery["bool"]["should"].append(rowClQuery)

    return equalQuery

def CreateEsQuery( pagesize, pagenum, mustlist, notmustlist,shouldlist ):

    queryformat = \
    {
        "size": str(pagesize), "from": str(pagenum),
        "query": {
            "bool": {
                "must": [
                ],
                "must_not": [
                    {
                    }
                ],
                "should": [
                    {}
                ]
            }
        }
    }

    for idx, _must in enumerate(mustlist):
        queryformat['query']['bool']['must'].append(_must)
    for idx, _mustnot in enumerate(notmustlist):
        queryformat['query']['bool']['must_not'].append(_mustnot)
    for idx, should in enumerate(shouldlist):
        queryformat['query']['bool']['should'].append(should)
    return json.dumps(queryformat)

