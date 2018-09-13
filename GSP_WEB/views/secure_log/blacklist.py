#-*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

import flask_excel as excel
from dateutil import parser
from flask import request, Response, render_template, json

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_BlackList import Rules_BlackList
from GSP_WEB.views.secure_log import blueprint_page



@blueprint_page.route('/black-list', methods=['GET'])
@login_required
def blacklist_List():
    nowtime = datetime.datetime.now()
    start_of_day = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)
    logUtil.addLog(request.remote_addr,1,'rules > black-list ')
    pattern_list = CommonCode.query.filter_by(GroupCode='rul_input_source').all()
    type_list = CommonCode.query.filter_by(GroupCode='an_data_from').all()
    timefrom = start_of_day.strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


    return render_template('secure_log/blacklist_list.html', pattern_list = pattern_list, timefrom=timefrom, timeto=timeto, type_list=type_list)

@blueprint_page.route('/black-list/list',methods=['POST'] )
@login_required
def blacklist_getlist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()
    search_type = request.form.get('search_type').strip()
    typeStr = list();
    typeStr = [str(item.EName) for item in CommonCode.query.filter_by(GroupCode='an_data_from').all() if item.Code == search_type]
    str_dt = ""
    end_dt = ""

    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()


    search_keyword_type = str(request.form['search_keyword_type'])

    sortedESresult = list()
    resultList = []

    query = Rules_BlackList.query.filter(Rules_BlackList.cre_dt.between(str_dt, end_dt))

    # if search_source != '':
    #     query = query.filter_by(source = search_source)

    if keyword != "" and search_keyword_type or typeStr:
        if search_keyword_type == 'md5':
            if not typeStr:
                typeStr=[""]

            query = query.filter(Rules_BlackList.md5.like('%'+keyword+'%'),
                                 Rules_BlackList.analysis_device.like('%' + typeStr[0] + '%'),
                                 Rules_BlackList.cre_dt.between(str_dt, end_dt))


        elif search_keyword_type == 'collect_uri':
            if not typeStr:
                typeStr=[""]

            query = query.filter(Rules_BlackList.uri.like('%'+keyword+'%'),
                                 Rules_BlackList.analysis_device.like('%' + typeStr[0] + '%'),
                                 Rules_BlackList.cre_dt.between(str_dt, end_dt))

        else:
            if not typeStr:
                typeStr=[""]

            query = query.filter(Rules_BlackList.analysis_device.like('%' + typeStr[0] + '%'))




    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_BlackList.cre_dt.desc()).paginate(curpage, per_page, error_out=False)



    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = Rules_BlackList.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/black-list', methods=['POST'])
@login_required
def addblacklist():
    # dupCheckResult = db_session.query(Account).filter_by(id=id).first()
    # if dupCheckResult is not None:
    #     raise InvalidUsage('중복된 아이디가 있습니다.', status_code=500)
    try:
        _pattern = Rules_BlackList()
        _pattern.rule_name = request.form['rule_name']
        _pattern.mal_file_name = request.form['mal_file_name']
        _pattern.md5 = request.form['pattern']
        _pattern.uri = request.form['uri']
        _pattern.description = request.form['analysis_device']
        #_pattern.size = int(request.form['size'])
        _pattern.analysis_device = request.form['desc']
        _pattern.detection_source = request.form['detection_source']
        #_pattern.source = request.form['source']
        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/black-list/<int:seq>', methods=['PUT'])
@login_required
def editblacklist(seq):
    _pattern = db_session.query(Rules_BlackList).filter_by(seq=seq).first()
    try:
        _pattern.rule_name = request.form['rule_name']
        _pattern.uri = request.form['uri']
        _pattern.md5 = request.form['pattern']
        _pattern.mal_file_name = request.form['mal_file_name']
        _pattern.analysis_device = request.form['analysis_device']
        _pattern.detection_source = request.form['detection_source']
        #_pattern.size = int(request.form['size'])
        _pattern.description = request.form['desc']
        #_pattern.source = request.form['source']
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/black-list/<int:seq>', methods=['DELETE'])
@login_required
def deleteblacklist(seq):
    _pattern = db_session.query(Rules_BlackList).filter_by(seq=seq).first()
    if _pattern is not None :
        db_session.delete(_pattern)
        db_session.commit()
    return ""


@blueprint_page.route('/black-list/excel-list', methods=['GET', 'POST'])
#@login_required
def getBlackListExcel():
    per_page = int(request.form.get('perpage'))

    start_idx = int(request.form.get('start'))
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()
    search_type = request.form.get('search_type').strip()
    typeStr = list();
    typeStr = [str(item.EName) for item in CommonCode.query.filter_by(GroupCode='an_data_from').all() if
               item.Code == search_type]
    str_dt = ""
    end_dt = ""

    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    search_keyword_type = str(request.form['search_keyword_type'])

    sortedESresult = list()
    resultList = []

    query = Rules_BlackList.query.filter(Rules_BlackList.cre_dt.between(str_dt, end_dt))

    if search_source != '':
        query = query.filter_by(source=search_source)

    if keyword != "" and search_keyword_type or typeStr:
        if search_keyword_type == 'md5':
            if not typeStr:
                typeStr = [""]

            query = query.filter(Rules_BlackList.md5.like('%' + keyword + '%'),
                                 Rules_BlackList.analysis_device.like('%' + typeStr[0] + '%'),
                                 Rules_BlackList.cre_dt.between(str_dt, end_dt))


        elif search_keyword_type == 'collect_uri':
            if not typeStr:
                typeStr = [""]

            query = query.filter(Rules_BlackList.uri.like('%' + keyword + '%'),
                                 Rules_BlackList.analysis_device.like('%' + typeStr[0] + '%'),
                                 Rules_BlackList.cre_dt.between(str_dt, end_dt))

    curpage = int(start_idx / per_page) + 1
    rowCount = query.count();
    cncList = query.order_by(Rules_BlackList.cre_dt.desc()).paginate(curpage, rowCount, error_out=False)#page=None, per_page=None, error_out=False, max_per_page=None

    result = OrderedDict()

    result['rule_name'] = list()
    result['uri']= list()
    result['md5'] = list()
    result['mal_file_name'] = list()
    result['description'] = list()
    result['analysis_result'] = list()
    result['cre_dt'] = list()
    result['detection_source'] = list()
    result['analysis_device'] = list()

    for _item in cncList.items:
        result['rule_name'].append(_item.rule_name)
        result['uri'].append(_item.uri)
        result['md5'].append(_item.md5)
        result['mal_file_name'].append(_item.mal_file_name)
        result['description'].append(_item.description)
        result['analysis_result'].append(_item.analysis_result)
        result['cre_dt'].append(_item.cre_dt)
        result['detection_source'].append(_item.detection_source)
        result['analysis_device'].append(_item.analysis_device)

    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")