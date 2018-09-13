#-*- coding: utf-8 -*-
import csv
import datetime
from collections import OrderedDict

import openpyxl
from flask import request, Response, render_template, Blueprint, json, make_response, g, session
import flask_excel as excel
from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.Rules_IP_Collection import Rules_IP_Collection
from GSP_WEB.views.rules import blueprint_page

@blueprint_page.route('/ip-collection', methods=['GET'])
@login_required
def ipcollection_List():
    logUtil.addLog(request.remote_addr,1,'rules > ip-collection')

    return render_template('rules/ip_collection.html')

@blueprint_page.route('/ip-collection/list',methods=['POST'] )
def ipcollection_getlist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    keyword = request.form.get('search_keyword').strip()

    query = Rules_IP_Collection.query

    if keyword != "":
        query = query.filter(Rules_IP_Collection.ip.like('%'+keyword+'%'))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_IP_Collection.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = Rules_IP_Collection.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')


@blueprint_page.route('/ip-collection/uploadlist', methods=['POST'])
def addIpCollectionFileData():
    # jsondata = request.form.get("dna_config");

    # 파일 로드

    file = request.files['file']
    if file.filename.split(".")[1] == 'csv':
        try:
            datalist = []
            spamreader = csv.reader(file)

            for index, row in enumerate(spamreader):


                # if int(row[1]) not in [8, 16, 24, 32]:
                #     raise InvalidUsage('Mask value is not valid', status_code=501)


                try:
                    _pattern = Rules_IP_Collection()
                    _pattern.ip = row[0]
                    _pattern.mask = row[1]
                    _pattern.detection_point = row[2]
                    _pattern.description = row[3]
                    #_pattern.description = row[3]
                    db_session.add(_pattern)
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    raise InvalidUsage('DB 저장 오류 ' + index + " line ", status_code=501)

        except Exception as e:
            raise InvalidUsage('CSV 로딩 실패, ' + e.message, status_code=501)

    elif file.filename.split(".")[1] == 'xlsx':
        try:
            wb = openpyxl.load_workbook(file)
            ws = wb.active
            for row in ws.rows:


                # if int(row[1].value) not in [8, 16, 24, 32]:
                #     raise InvalidUsage('Mask value is not valid', status_code=501)

                try:
                    _pattern = Rules_IP_Collection()
                    _pattern.ip = row[0].value
                    _pattern.mask = row[1].value
                    _pattern.detection_point = row[2].value
                    _pattern.description = row[3].value

                    db_session.add(_pattern)
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    raise InvalidUsage('DB 저장 오류 ' + row[0].row + " line ", status_code=501)

        except Exception as e:
            raise InvalidUsage('xlsx 로딩 실패, ' + e.message, status_code=501)

    else:
        raise InvalidUsage('지원하지 않는 파일 포멧 입니다.', status_code=501)

    return ""



@blueprint_page.route('/ip-collection', methods=['POST'])
#@login_required
def addipcollection():
    exists = Rules_IP_Collection.query.filter_by(ip=request.form['pattern'].strip()).first()
    if exists is not None:
        raise InvalidUsage('중복 IP가 존재합니다.', status_code=501)

    try:
        _pattern = Rules_IP_Collection()
        _pattern.ip = request.form['pattern'].strip()
        _pattern.mask = request.form['mask'].strip()
        _pattern.detection_point = request.form['detection_point'].strip()
        _pattern.description = request.form['description'].strip()
        #_pattern.description = request.form['desc']
        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/ip-collection/<int:seq>', methods=['PUT'])
#@login_required
def editipcollection(seq):
    _pattern = db_session.query(Rules_IP_Collection).filter_by(seq=seq).first()
    try:
        _pattern.ip = request.form['pattern'].strip()
        _pattern.mask = request.form['mask'].strip()
        _pattern.detection_point = request.form['detection_point'].strip()
        _pattern.description = request.form['description'].strip()
        #_pattern.description = request.form['desc']

        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/ip-collection/<int:seq>', methods=['DELETE'])
#@login_required
def deleteipcollection(seq):
    _pattern = db_session.query(Rules_IP_Collection).filter_by(seq=seq).first()
    if _pattern is not None :
        db_session.delete(_pattern)
        db_session.commit()
    return ""


@blueprint_page.route('/ip-collection/excel-list', methods=['GET','POST'])
#@login_required
def getIpCollectionExcel():


    per_page = int(request.form.get('perpage'))
    #draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    keyword = request.form.get('search_keyword').strip()

    query = Rules_IP_Collection.query

    if keyword != "":
        query = query.filter(Rules_IP_Collection.ip.like('%' + keyword + '%'))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_IP_Collection.cre_dt.desc()).paginate(curpage, per_page, error_out=False)
    #inchan = cncList.items[0].ip




    result = OrderedDict()

    result['날짜'] = list()
    result['ip'] = list()
    result['mask'] = list()
    result['detection_point'] = list()
    result['etc'] = list()
    result['description'] = list()
    # result['description'] = list()
    # result['type'] = list()

    for _item in cncList.items:
        result['날짜'].append(_item.cre_dt)
        result['ip'].append(_item.ip)
        result['mask'].append(_item.mask)
        result['detection_point'].append(_item.detection_point)
        result['etc'].append(_item.etc)
        result['description'].append(_item.description)
        # result['description'].append(_item.description)
        # result['type'].append(_item.type)

    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")