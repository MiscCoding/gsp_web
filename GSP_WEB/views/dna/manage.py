#-*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

from flask import request, Response, render_template, Blueprint, json, make_response, g, session
from sqlalchemy import or_, and_

import flask_excel as excel

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.DNA_Element import DNA_Element

from GSP_WEB.views.dna import blueprint_page

@blueprint_page.route('/manage', methods=['GET'])
@login_required
def dnaList():
    #logUtil.addLog(request.remote_addr,1,'links > list ')
    type_list = CommonCode.query.filter_by(GroupCode = 'raw_data_type').all()

    return render_template('dna/manage.html', type_list = type_list)

@blueprint_page.route('/list', methods=['POST'])
#@login_required
def get_list():
    #logUtil.addLog(request.remote_addr,1,'links > list ')

    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    search_type = request.form.get('search_type')
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()

    query = DNA_Element.query.filter(DNA_Element.del_yn == 'N')

    if keyword != "":
        query = query.filter(DNA_Element.dna_name.like('%' + keyword + '%'))

    curpage = int(start_idx / per_page) + 1
    dndList = query.order_by(DNA_Element.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(dndList.total)
    result["recordsFiltered"] = str(dndList.total)
    result["data"] = DNA_Element.serialize_list(dndList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')


@blueprint_page.route('/list/excel-list', methods=['GET','POST'])
#@login_required
def get_excel_list():
    #logUtil.addLog(request.remote_addr,1,'links > list ')

    per_page = int(request.form.get('perpage'))

    start_idx = int(request.form.get('start'))

    keyword = request.form.get('search_keyword').strip()

    query = DNA_Element.query.filter(DNA_Element.del_yn == 'N')

    if keyword != "":
        query = query.filter(DNA_Element.dna_name.like('%' + keyword + '%'))

    curpage = int(start_idx / per_page) + 1
    dndList = query.order_by(DNA_Element.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    result = OrderedDict()

    result['DNA 명'] = list()
    result['섹터목록'] = list()
    result['등록일'] = list()
    result['수정일'] = list()

    for _item in dndList.items:
        result['DNA 명'].append(_item.dna_name)
        result['섹터목록'].append(_item.operate_function)
        result['등록일'].append(_item.cre_dt)
        result['수정일'].append(_item.mod_dt)


    # result = dict()
    # result["draw"] = str(draw)
    # result["recordsTotal"] = str(dndList.total)
    # result["recordsFiltered"] = str(dndList.total)
    # result["data"] = DNA_Element.serialize_list(dndList.items)
    # str_json = json.dumps(result)
    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")



@blueprint_page.route('/get-list', methods=['GET'])
#@login_required
def get_full_list():
    #logUtil.addLog(request.remote_addr,1,'links > list ')

    query = DNA_Element.query.filter(DNA_Element.del_yn == 'N')
    dnaList = query.order_by(DNA_Element.cre_dt.desc()).all()

    result = dict()
    result["data"] = DNA_Element.serialize_list(dnaList)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/manage', methods=['POST'])
#@login_required
def add_dna():
    #logUtil.addLog(request.remote_addr,1,'links > list ')

    jsondata = request.form.get("dna_config");
    try:
        dna = DNA_Element()
        dna.dna_name = request.form.get("dna_name")
        dna.operate_function = jsondata
        dna.del_yn = 'N'
        db_session.add(dna)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code=501)

    return ""

@blueprint_page.route('/manage/<int:seq>', methods=['PUT'])
#@login_required
def edit_dna(seq):
    #logUtil.addLog(request.remote_addr,1,'links > list ')

    try:
        dna = db_session.query(DNA_Element).filter_by(id=seq).first()
        dna.dna_name = request.form.get("dna_name")
        dna.operate_function = request.form.get("dna_config");
        dna.del_yn = 'N'
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code=501)
    return ""

@blueprint_page.route('/manage/<int:seq>', methods=['DELETE'])
def delete_dna(seq):
    dna = db_session.query(DNA_Element).filter_by(id=seq).first()
    if dna is not None :
        dna.del_yn = 'Y'
        db_session.commit()
    return ""

