#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil import parser
from elasticsearch import Elasticsearch
from flask import json

from GSP_WEB import db_session, app
from GSP_WEB.models.Rules_Profile import Rules_Profile

typeName = 'ip_uri_map'

def GetIpUriMapQuery(request):
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    per_page = int(request.form.get('perpage'))
    start_idx = int(request.form.get('start'))
    keywordType = request.form.get('keywordType')
    keyword = request.form.get('search_keyword').strip()

    if per_page == None:
        per_page = int(request.form['perpage'])
    if start_idx == None:
        start_idx = int(request.form['start'])
    page_no = int(start_idx / per_page)


    doc = {
        "query": {
            "bool": {
                "must": [
                ]
            }
        },
        "size": per_page,
        "from": start_idx
    }

    if keyword != "":
        if keywordType == 'uri':
            sourceNode = {"term": {"uri.keyword": keyword}}
            doc["query"]["bool"]["must"].append(sourceNode)
        else:
            sourceNode = {"term": {"dst_ip.keyword": keyword}}
            doc["query"]["bool"]["must"].append(sourceNode)

    return doc

