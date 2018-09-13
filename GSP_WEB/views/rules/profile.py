#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_Profile import Rules_Profile
from GSP_WEB.models.Rules_Profile_Group import Rules_Profile_Group
from GSP_WEB.query.link_dna import GetLinkDnaListQueryEs, GetLinkDnaListQueryForProfile, GetProfileOperation
from GSP_WEB.views.rules import blueprint_page

@blueprint_page.route('/profile', methods=['GET'])
@login_required
def profile_List():
    logUtil.addLog(request.remote_addr,1,'rules > profile ')
    pattern_list = CommonCode.query.filter_by(GroupCode = 'rul_input_source').all()
    typeList = CommonCode.query.filter_by(GroupCode="DATA_TYPE").all()
    analyzer_timespan = CommonCode.query.filter_by(Name = 'anlyzer setting').first().EXT1

    return render_template('rules/profile_list.html', pattern_list = pattern_list, typeList =typeList, analyzer_timespan = analyzer_timespan)

@blueprint_page.route('/profile/list',methods=['POST'] )
def profile_getlist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()


    query = Rules_Profile.query.filter(Rules_Profile.group_code == None)

    if search_source != '':
        query = query.filter_by(source = search_source)
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

@blueprint_page.route('/profile', methods=['POST'])
@login_required
def addprofile():

    existResult = db_session.query(Rules_Profile).filter_by(name=request.form['name']).first()

    try:
        _pattern = None
        #같은 이름의 룰이 존재한다면 추가 대신 수정한다.
        if( existResult == None):
            _pattern = Rules_Profile()
        else:
            _pattern = existResult

        _pattern.group_code = request.form.get('group_code')
        _pattern.name =request.form['name']
        _pattern.description = request.form['description']
        _pattern.pattern_ui = request.form['pattern_ui']
        _pattern.pattern_query = GetLinkDnaListQueryForProfile(_pattern.pattern_ui)
        _pattern.pattern_operation = GetProfileOperation(_pattern.pattern_ui, request.form['name'], request.form.get('group_code'))
        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

def makeProfileForm():
    request.form['']

@blueprint_page.route('/profile/<int:seq>', methods=['PUT'])
@login_required
def editprofile(seq):
    _pattern = db_session.query(Rules_Profile).filter_by(seq=seq).first()
    try:
        _pattern.group_code = request.form.get('group_code')
        _pattern.name = request.form['name']
        _pattern.description = request.form['description']
        _pattern.pattern_ui = request.form['pattern_ui']
        _pattern.pattern_query = GetLinkDnaListQueryForProfile(_pattern.pattern_ui)
        _pattern.pattern_operation = GetProfileOperation(_pattern.pattern_ui, request.form['name'], request.form.get('group_code'))
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/profile/<int:seq>', methods=['DELETE'])
@login_required
def deleteprofile(seq):
    _pattern = db_session.query(Rules_Profile).filter_by(seq=seq).first()
    if _pattern is not None :
        db_session.delete(_pattern)
        db_session.commit()
    return ""

@blueprint_page.route('/profile/<int:seq>', methods=['GET'])
@login_required
def getprofiledetail(seq):
    _profileList = db_session.query(Rules_Profile).filter_by(seq=seq).all()
    _profile = Rules_Profile.serialize_list(_profileList)[0]
    str_json = json.dumps(_profile)

    return str_json

