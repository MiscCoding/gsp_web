#-*- coding: utf-8 -*-
import datetime
import io
import zipfile
from collections import OrderedDict

import flask_excel as excel
from dateutil import parser
from flask import request, Response, render_template, json, Flask, send_file

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.malicious_info import malicious_info
# blueprint_page = Blueprint('bp_rules_page', __name__, url_prefix='/rules')
from GSP_WEB.views.secure_log import blueprint_page


@blueprint_page.route('/malCodeCollectionNew', methods=['GET'])
@login_required
def malList():
    nowtime = datetime.datetime.now()
    start_of_day = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)
    logUtil.addLog(request.remote_addr,1,'rules > c&c ')
    #type_list = CommonCode.query.filter_by(GroupCode = 'RULE_CNC_TYPE').all()
    # type_list = CommonCode.query.filter_by(GroupCode='an_data_from').all()
    pattern_list = CommonCode.query.filter_by(GroupCode = 'rul_input_source').all()

    timefrom = start_of_day.strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return render_template('secure_log/malCodeCollectionNew.html', timefrom=timefrom, timeto=timeto, pattern_list = pattern_list)


@blueprint_page.route('/malCodeCollectionNew/list', methods=['POST'])
@login_required
def getMalList():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))

    #search_source = request.form.get('search_source')


    keyword = request.form.get('search_keyword').strip()
    #search_type = request.form.get('search_keyword_type').strip()
    # typeStr = list()
    # typeStr = [str(item.EName) for item in CommonCode.query.filter_by(GroupCode='an_data_from').all() if
    #            item.Code == search_type]
    str_dt = ""
    end_dt = ""

    search_keyword_type = str(request.form['search_keyword_type'])

    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()


    query = malicious_info.query.filter(malicious_info.cre_dt.between(str_dt, end_dt))

    # if search_type != '':
    #     query = query.filter_by(rule_type = search_type)
    # if search_source != '':
    #     query = query.filter_by(source = search_source)
    # if keyword != "" and not search_keyword_type or typeStr:
    #     if not typeStr:
    #         typeStr = [""]

    # query = Rules_White_IP_URL.query
    #
    if keyword != "" and search_keyword_type == "ip":
        query = query.filter(malicious_info.ip.like('%' + str(keyword) + '%'))
    #
    if keyword != "" and search_keyword_type == "url":
        query = query.filter(malicious_info.url.like('%' + keyword + '%'))
    #
    if keyword != "" and search_keyword_type == "country_code":
        query = query.filter(malicious_info.country_code.like('%' + keyword + '%'))
    #
    if keyword != "" and search_keyword_type == "file_name":
        query = query.filter(malicious_info.file_name.like('%' + keyword + '%'))

    if keyword != "" and search_keyword_type == "md5":
        query = query.filter(malicious_info.md5.like('%' + keyword + '%'))

    if keyword != "" and search_keyword_type == "detect_info":
        query = query.filter(malicious_info.detect_info.like('%' + keyword + '%'))

    if keyword != "" and search_keyword_type == "collect_point":
        query = query.filter(malicious_info.collect_point.like('%' + keyword + '%'))

    # query = query.filter(malicious_info.url.like('%'+keyword+'%'))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(malicious_info.cre_dt.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = malicious_info.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')


@blueprint_page.route('/malCodeCollectionNew', methods=['POST'])
@login_required
def addMalCnc():
    # dupCheckResult = db_session.query(Account).filter_by(id=id).first()
    # if dupCheckResult is not None:
    #     raise InvalidUsage('중복된 아이디가 있습니다.', status_code=500)
    try:
        _cnc = malicious_info()
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

@blueprint_page.route('/malCodeCollectionNew/<int:seq>', methods=['PUT'])
@login_required
def editMalAccount(seq):
    _cnc = db_session.query(malicious_info).filter_by(id=seq).first()
    try:
        #_cnc.rule_type = request.form['type']
        # _cnc.pattern_uri = request.form['pattern_uri']
        # _cnc.description = request.form['desc']
        _cnc.comment = request.form['comment']
        #_cnc.source = request.form['source']
        # _cnc.mod_dt = datetime.datetime.now()
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/malCodeCollectionNew/<int:seq>', methods=['DELETE'])
@login_required
def deleteMalAccount(seq):
    _cnc = db_session.query(malicious_info).filter_by(id=seq).first()
    if _cnc is not None :
        db_session.delete(_cnc)
        db_session.commit()
    return ""

@blueprint_page.route('/malCodeCollectionNew/download', methods=['POST'])
@login_required
def maliciouscodedownloadInCollectionPage():
    # jsondata = request.form.get("dna_config");

    filePathsList = []
    zipfileNameStr = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    if request.method == 'POST':
        filepathnfs = request.form.get('_filepath')
        if filepathnfs:
            filePathsList = filepathnfs.split(",");
            zip_filename = "%s.zip" % zipfileNameStr

            data = io.BytesIO()

            with zipfile.ZipFile(data, mode="w") as z:
                for f_name in filePathsList:
                    z.write(f_name)


            data.seek(0)

            return send_file(
                data,
                mimetype='application/zip',
                as_attachment = True,
                attachment_filename = zip_filename
            )
    else:
        raise InvalidUsage("No Post method received")

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@blueprint_page.route('/malCodeCollectionNew/excel-list', methods=['GET', 'POST'])
#@login_required
def getMalListExcel():
    per_page = int(request.form.get('perpage'))
    # draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))

    # search_source = request.form.get('search_source')

    keyword = request.form.get('search_keyword').strip()
    # search_type = request.form.get('search_keyword_type').strip()
    # typeStr = list()
    # typeStr = [str(item.EName) for item in CommonCode.query.filter_by(GroupCode='an_data_from').all() if
    #            item.Code == search_type]
    str_dt = ""
    end_dt = ""

    search_keyword_type = str(request.form['search_keyword_type'])

    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    query = malicious_info.query.filter(malicious_info.cre_dt.between(str_dt, end_dt))

    # if search_type != '':
    #     query = query.filter_by(rule_type = search_type)
    # if search_source != '':
    #     query = query.filter_by(source = search_source)
    # if keyword != "" and not search_keyword_type or typeStr:
    #     if not typeStr:
    #         typeStr = [""]

    # query = Rules_White_IP_URL.query
    #
    if keyword != "" and search_keyword_type == "ip":
        query = query.filter(malicious_info.ip.like('%' + str(keyword) + '%'))
    #
    if keyword != "" and search_keyword_type == "url":
        query = query.filter(malicious_info.url.like('%' + keyword + '%'))
    #
    if keyword != "" and search_keyword_type == "country_code":
        query = query.filter(malicious_info.country_code.like('%' + keyword + '%'))
    #
    if keyword != "" and search_keyword_type == "file_name":
        query = query.filter(malicious_info.file_name.like('%' + keyword + '%'))

    if keyword != "" and search_keyword_type == "md5":
        query = query.filter(malicious_info.md5.like('%' + keyword + '%'))

    if keyword != "" and search_keyword_type == "detect_info":
        query = query.filter(malicious_info.detect_info.like('%' + keyword + '%'))

    if keyword != "" and search_keyword_type == "collect_point":
        query = query.filter(malicious_info.collect_point.like('%' + keyword + '%'))

    curpage = int(start_idx / per_page) + 1
    rowCount = query.count()
    cncList = query.order_by(malicious_info.cre_dt.desc()).paginate(curpage, rowCount, error_out=False)


    result = OrderedDict()

    result['creation_date'] = list()
    result['url'] = list()
    result['ip'] = list()
    result['country_code'] = list()
    result['file_name'] = list()
    result['md5'] = list()
    result['detection_info'] = list()
    result['collection_point'] = list()
    result['comment'] = list()
    result['stix'] = list()

    for _item in cncList.items:
        result['creation_date'].append(_item.cre_dt)
        result['url'].append(_item.url)
        result['ip'].append(_item.ip)
        result['country_code'].append(_item.country_code)
        result['file_name'].append(_item.file_name)
        result['md5'].append(_item.md5)
        result['detection_info'].append(_item.detect_info)
        result['collection_point'].append(_item.collect_point)
        result['comment'].append(_item.comment)
        result['stix'].append(_item.stix)
        # result['category'].append(_item.category)
        # result['pattern_uri'].append(_item.pattern_uri)
        # result['analysis_device'].append(_item.analysis_device)
        # result['analysis_result'].append(_item.analysis_result)
        # result['cre_dt'].append(_item.cre_dt)
        # result['source_name'].append(_item.source)
        # result['description'].append(_item.description)

    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")