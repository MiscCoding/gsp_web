#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_Snort import Rules_Snort
from GSP_WEB.views.rules import blueprint_page

@blueprint_page.route('/snort', methods=['GET'])
@login_required
def snort_List():
    logUtil.addLog(request.remote_addr,1,'rules > snort-list ')
    pattern_list = CommonCode.query.filter_by(GroupCode = 'rul_input_source').all()
    myorder = [2,1,0]
    pattern_list = [pattern_list[i] for i in myorder]

    return render_template('rules/snort_list.html', pattern_list = pattern_list)

@blueprint_page.route('/snort/list',methods=['POST'] )
def snort_getlist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()
    columnIndex = request.form.get('columnIndex').strip()

    query = Rules_Snort.query

    if search_source != '':
        query = query.filter_by(source = search_source)
    if keyword != "":
        query = query.filter(Rules_Snort.pattern.like('%'+keyword+'%'))

    curpage = int(start_idx / per_page) + 1

    cncList = query.order_by(Rules_Snort.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    if columnIndex == "name":
        cncList = query.order_by(Rules_Snort.name.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = Rules_Snort.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/snort', methods=['POST'])
#@login_required
def addsnortlist():
    # dupCheckResult = db_session.query(Account).filter_by(id=id).first()
    # if dupCheckResult is not None:
    #     raise InvalidUsage('중복된 아이디가 있습니다.', status_code=500)
    try:
        _pattern = Rules_Snort()
        _pattern.name = request.form['name']
        _pattern.pattern =request.form['pattern']
        _pattern.level = int(request.form['level'])
        _pattern.description = request.form['desc']
        _pattern.source = request.form['source']
        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/snort/<int:seq>', methods=['PUT'])
#@login_required
def editsnortlist(seq):
    _pattern = db_session.query(Rules_Snort).filter_by(seq=seq).first()
    try:
        _pattern.name = request.form['name']
        _pattern.pattern = request.form['pattern']
        _pattern.level = int(request.form['level'])
        _pattern.description = request.form['desc']
        _pattern.mod_dt = datetime.datetime.now()
        _pattern.source = request.form['source']
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/snort/<int:seq>', methods=['DELETE'])
#@login_required
def deletesnortlist(seq):
    _pattern = db_session.query(Rules_Snort).filter_by(seq=seq).first()
    if _pattern is not None :
        db_session.delete(_pattern)
        db_session.commit()
    return ""