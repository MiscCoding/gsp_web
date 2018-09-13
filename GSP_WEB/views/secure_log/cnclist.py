#-*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

import flask_excel as excel
from dateutil import parser
from flask import request, Response, render_template, json, Flask

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_CNC import Rules_CNC
# blueprint_page = Blueprint('bp_rules_page', __name__, url_prefix='/rules')
from GSP_WEB.views.secure_log import blueprint_page


@blueprint_page.route('/cnc-manage', methods=['GET'])
@login_required
def cncList():
    nowtime = datetime.datetime.now()
    start_of_day = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)
    logUtil.addLog(request.remote_addr,1,'rules > c&c ')
    #type_list = CommonCode.query.filter_by(GroupCode = 'RULE_CNC_TYPE').all()
    type_list = CommonCode.query.filter_by(GroupCode='an_data_from').all()
    pattern_list = CommonCode.query.filter_by(GroupCode = 'rul_input_source').all()

    timefrom = start_of_day.strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return render_template('secure_log/cnc_manage.html', type_list = type_list, timefrom=timefrom, timeto=timeto, pattern_list = pattern_list)


@blueprint_page.route('/cnc-manage/list', methods=['POST'])
@login_required
def getList():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))

    search_source = request.form.get('search_source')


    keyword = request.form.get('search_keyword').strip()
    search_type = request.form.get('search_type').strip()
    typeStr = list()
    typeStr = [str(item.EName) for item in CommonCode.query.filter_by(GroupCode='an_data_from').all() if
               item.Code == search_type]
    str_dt = ""
    end_dt = ""

    search_keyword_type = str(request.form['search_keyword_type'])

    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()


    query = Rules_CNC.query.filter(Rules_CNC.cre_dt.between(str_dt, end_dt))

    # if search_type != '':
    #     query = query.filter_by(rule_type = search_type)
    if search_source != '':
        query = query.filter_by(source = search_source)
    if keyword != "" and not search_keyword_type or typeStr:
        if not typeStr:
            typeStr = [""]

        query = query.filter(Rules_CNC.pattern_uri.like('%'+keyword+'%'),
                             Rules_CNC.analysis_device.like('%'+typeStr[0]+'%'),
                             Rules_CNC.cre_dt.between(str_dt, end_dt))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_CNC.cre_dt.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = Rules_CNC.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')


@blueprint_page.route('/cnc-manage', methods=['POST'])
@login_required
def addCnc():
    # dupCheckResult = db_session.query(Account).filter_by(id=id).first()
    # if dupCheckResult is not None:
    #     raise InvalidUsage('중복된 아이디가 있습니다.', status_code=500)
    try:
        _cnc = Rules_CNC()
        #_cnc.rule_type = request.form['type']
        _cnc.pattern_uri =request.form['uri']
        _cnc.description = request.form['desc']
        _cnc.detection_source = request.form['detection_source']
       #_cnc.source = request.form['source']
        db_session.add(_cnc)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/cnc-manage/<int:seq>', methods=['PUT'])
@login_required
def editAccount(seq):
    _cnc = db_session.query(Rules_CNC).filter_by(seq=seq).first()
    try:
        #_cnc.rule_type = request.form['type']
        _cnc.pattern_uri = request.form['pattern_uri']
        _cnc.description = request.form['desc']
        _cnc.detection_source = request.form['detection_source']
        #_cnc.source = request.form['source']
        _cnc.mod_dt = datetime.datetime.now()
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/cnc-manage/<int:seq>', methods=['DELETE'])
@login_required
def deleteAccount(seq):
    _cnc = db_session.query(Rules_CNC).filter_by(seq=seq).first()
    if _cnc is not None :
        db_session.delete(_cnc)
        db_session.commit()
    return ""


@blueprint_page.route('/cnc-manage/excel-list', methods=['GET', 'POST'])
#@login_required
def getListExcel():
    per_page = int(request.form.get('perpage'))

    start_idx = int(request.form.get('start'))

    search_source = request.form.get('search_source')

    keyword = request.form.get('search_keyword').strip()
    search_type = request.form.get('search_type').strip()
    typeStr = list()
    typeStr = [str(item.EName) for item in CommonCode.query.filter_by(GroupCode='an_data_from').all() if
               item.Code == search_type]
    str_dt = ""
    end_dt = ""

    search_keyword_type = str(request.form['search_keyword_type'])

    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    query = Rules_CNC.query.filter(Rules_CNC.cre_dt.between(str_dt, end_dt))

    # if search_type != '':
    #     query = query.filter_by(rule_type = search_type)
    if search_source != '':
        query = query.filter_by(source=search_source)
    if keyword != "" and not search_keyword_type or typeStr:
        if not typeStr:
            typeStr = [""]

        query = query.filter(Rules_CNC.pattern_uri.like('%' + keyword + '%'),
                             Rules_CNC.analysis_device.like('%' + typeStr[0] + '%'),
                             Rules_CNC.cre_dt.between(str_dt, end_dt))

    curpage = int(start_idx / per_page) + 1
    rowCount = query.count()
    cncList = query.order_by(Rules_CNC.cre_dt.desc()).paginate(curpage, rowCount, error_out=False)


    result = OrderedDict()

    result['category'] = list()
    result['pattern_uri'] = list()
    result['analysis_device'] = list()
    result['analysis_result'] = list()
    result['cre_dt'] = list()
    result['source_name'] = list()
    result['description'] = list()

    for _item in cncList.items:
        result['category'].append(_item.category)
        result['pattern_uri'].append(_item.pattern_uri)
        result['analysis_device'].append(_item.analysis_device)
        result['analysis_result'].append(_item.analysis_result)
        result['cre_dt'].append(_item.cre_dt)
        result['source_name'].append(_item.source)
        result['description'].append(_item.description)

    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")