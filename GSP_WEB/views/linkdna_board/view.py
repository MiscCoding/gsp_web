#-*- coding: utf-8 -*-
import datetime
from GSP_WEB.common.util.date_util import Local2UTC, UTC2Local
from elasticsearch import Elasticsearch
from flask import Blueprint, request, render_template, json, Response
from dateutil import parser

from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB import app, login_required
import json

from GSP_WEB.models.Rules_Profile_Group import Rules_Profile_Group
from GSP_WEB.query.link_dna_board import link_dna_board

blueprint_page = Blueprint('bp_linkdna_board', __name__, url_prefix='/linkdnaboard')

@blueprint_page.route('/', methods=['GET'])
#@login_required
def getLinkDnaLog():
    #logUtil.addLog(request.remote_addr, 1, 'linkdna-board/log')

    return render_template('linkdna_board/list.html')

@blueprint_page.route('/grouplist', methods=['GET'])
#@login_required
def getLinkDnaLogGroupList():
    #logUtil.addLog(request.remote_addr, 1, 'linkdna-board/log')
    columns = list()

    profileGroupList = Rules_Profile_Group.query.filter_by(del_yn='N').order_by(Rules_Profile_Group.name.asc()).all()
    col_sip = {
        "data": "_source.src_ip",
        "title": "출발 IP",
        "width" : "200px"
    }

    col_dip = {
        "data": "_source.dst_ip",
        "title": "목적 IP",
        "width" : "200px"
    }
    columns.append(col_sip)
    columns.append(col_dip)

    for _row in profileGroupList:
        col = {
            "data" : "_source.linkdna.data_"+ str(_row.seq),
            "title" : _row.name,
            "width" : "300px"
        }
        columns.append(col)

    str_json = json.dumps(columns, encoding='utf-8')
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/list', methods=['POST'])
#@login_required
def getLinkDnaLog_List():
    draw = int(request.form.get('draw'))
    link_dna_board_list = link_dna_board.getList("gsp-*", request)

    total = int(link_dna_board_list['hits']['total'])
    if total > 10000:
        total = 10000

    groupList = Rules_Profile_Group.query.filter_by(del_yn='N').order_by(Rules_Profile_Group.name.asc()).all()
    for row in link_dna_board_list['hits']['hits']:
        for _group in groupList:
            profiles =  row['_source']['linkdna'].get(str(_group.seq))
            if profiles is None:
                #각 row 데이터에 datatable에 표시할 값을 생성한다.
                row['_source']['linkdna']["data_" + str(_group.seq) ] = '-'
            else:
                for idx, _profile in enumerate(profiles):

                    if idx == 0:
                        row['_source']['linkdna']["data_" + str(_group.seq)] = _profile['profile_name']
                    else:
                        row['_source']['linkdna']["data_" + str(_group.seq)] += ", " + _profile['profile_name']

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = link_dna_board_list['hits']['hits']

    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')