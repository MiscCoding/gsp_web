#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_WhiteList import Rules_WhiteList
from GSP_WEB.views.rules import blueprint_page

@blueprint_page.route('/white-list', methods=['GET'])
@login_required
def whitelist_List():
    logUtil.addLog(request.remote_addr,1,'rules > white-list ')
    pattern_list = CommonCode.query.filter_by(GroupCode = 'rul_input_source').all()

    return render_template('rules/whitelist_list.html', pattern_list = pattern_list)

@blueprint_page.route('/white-list/list',methods=['POST'] )
def whitelist_getlist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()


    query = Rules_WhiteList.query

    if search_source != '':
        query = query.filter_by(source = search_source)
    if keyword != "":
        query = query.filter(Rules_WhiteList.pattern_uri.like('%'+keyword+'%'))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_WhiteList.cre_dt.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = Rules_WhiteList.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/white-list', methods=['POST'])
#@login_required
def addwhitelist():
    # dupCheckResult = db_session.query(Account).filter_by(id=id).first()
    # if dupCheckResult is not None:
    #     raise InvalidUsage('중복된 아이디가 있습니다.', status_code=500)
    try:
        _pattern = Rules_WhiteList()
        _pattern.md5 =request.form['pattern']
        _pattern.description = request.form['desc']
        _pattern.source = request.form['source']
        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/white-list/<int:seq>', methods=['PUT'])
#@login_required
def editwhitelist(seq):
    _pattern = db_session.query(Rules_WhiteList).filter_by(seq=seq).first()
    try:
        _pattern.md5 = request.form['pattern']
        _pattern.description = request.form['desc']
        _pattern.source = request.form['source']
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/white-list/<int:seq>', methods=['DELETE'])
#@login_required
def deletewhitelist(seq):
    _pattern = db_session.query(Rules_WhiteList).filter_by(seq=seq).first()
    if _pattern is not None :
        db_session.delete(_pattern)
        db_session.commit()
    return ""