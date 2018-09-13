#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_Profile import Rules_Profile
from GSP_WEB.models.Rules_Profile_Group import Rules_Profile_Group
from GSP_WEB.query.link_dna import GetLinkDnaListQueryEs, GetLinkDnaListQueryForProfile
from GSP_WEB.views.rules import blueprint_page

@blueprint_page.route('/linkdna', methods=['GET'])
@login_required
def link_dna_List():
    #logUtil.addLog(request.remote_addr,1,'rules > link-dna ')
    group_list = Rules_Profile_Group.query.all()

    return render_template('rules/link_dna_list.html', group_list = group_list)

@blueprint_page.route('/linkdna/list',methods=['POST'] )
def link_dna_getlist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    group_code = request.form.get('group_code')
    keyword = request.form.get('search_keyword').strip()

    query = Rules_Profile.query.filter_by(del_yn = 'N')

    if group_code != '' and group_code is not None:
        query = query.filter_by(group_code = group_code)
    else:
        query = query.filter(Rules_Profile.group_code != None)
    if keyword != "":
        query = query.filter(Rules_Profile.name.like('%'+keyword+'%'))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_Profile.cre_dt.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = Rules_Profile.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/linkdna/group/namelist',methods=['GET'] )
def link_dna_getGroupNameList():
    query = Rules_Profile_Group.query.filter_by(del_yn = 'N')
    cncList = query.order_by(Rules_Profile_Group.cre_dt.desc()).all()

    result = dict()
    result["data"] = Rules_Profile_Group.serialize_list(cncList)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/linkdna/group/list',methods=['POST'] )
def link_dna_getGrouplist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))

    query = Rules_Profile_Group.query.filter_by(del_yn = 'N')

    curpage = int(start_idx / per_page) + 1
    groupList = query.order_by(Rules_Profile_Group.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(groupList.total)
    result["recordsFiltered"] = str(groupList.total)
    result["data"] = Rules_Profile.serialize_list(groupList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/linkdna/group', methods=['POST'])
#@login_required
def addGroup():

    try:
        _pattern = Rules_Profile_Group()
        _pattern.time_gubun = request.form['time_gubun']
        _pattern.time_value = request.form['time_value']
        _pattern.name =request.form['name']
        _pattern.description = request.form['description']
        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/linkdna/group/<int:seq>', methods=['PUT'])
#@login_required
def editGroup(seq):
    _pattern = db_session.query(Rules_Profile_Group).filter_by(seq=seq).first()
    try:
        _pattern.name = request.form['name']
        _pattern.time_gubun = request.form['time_gubun']
        _pattern.time_value = request.form['time_value']
        _pattern.description = request.form['description']
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/linkdna/group/<int:seq>', methods=['DELETE'])
#@login_required
def deleteGroup(seq):
    _pattern = db_session.query(Rules_Profile_Group).filter_by(seq=seq).first()
    if _pattern is not None :
        _pattern.del_yn = 'Y'
        db_session.commit()
    return ""