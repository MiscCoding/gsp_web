#-*- coding: utf-8 -*-
import csv
import datetime
from collections import OrderedDict

from flask import request, Response, render_template, Blueprint, json, make_response, g, session
import flask_excel as excel
from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.Rules_White_IP import Rules_White_IP
from GSP_WEB.views.rules import blueprint_page

@blueprint_page.route('/white-ip', methods=['GET'])
@login_required
def whiteip_List():
    logUtil.addLog(request.remote_addr,1,'rules > white-ip ')

    return render_template('rules/whiteip_list.html')

@blueprint_page.route('/white-ip/list',methods=['POST'] )
def whiteip_getlist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    keyword = request.form.get('search_keyword').strip()

    query = Rules_White_IP.query

    if keyword != "":
        query = query.filter(Rules_White_IP.ip.like('%'+keyword+'%'))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_White_IP.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = Rules_White_IP.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')


@blueprint_page.route('/white-ip/uploadlist', methods=['POST'])
def addFileData():
    # jsondata = request.form.get("dna_config");

    # 파일 로드

    file = request.files['file']
    if file.content_type == 'application/vnd.ms-excel':
        try:
            datalist = []
            spamreader = csv.reader(file)

            for index, row in enumerate(spamreader):
                # if index == 0 and isNumberString(row[0]) != True:
                #     continue
                # if isNumberString(row[0]) == True:
                #     datalist.append(row[0])
                # else:
                #     datalist.append(None)

                if int(row[1]) not in [8, 16, 24, 32]:
                    raise InvalidUsage('Mask value is not valid', status_code=501)


                try:
                    _pattern = Rules_White_IP()
                    _pattern.ip = row[0]
                    _pattern.mask = row[1]
                    _pattern.description = row[2]
                    db_session.add(_pattern)
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    raise InvalidUsage('DB 저장 오류', status_code=501)

        except Exception as e:
            raise InvalidUsage('CSV 로딩 실패, ' + e.message, status_code=501)

        # target link와 데이터 크기 비교
        # target_type = request.form.get("target_type")
        # target_seq = request.form.get("target_seq")
        # if ValidateTargetSize(datalist.__len__(), target_type, target_seq) == False:
        #     raise InvalidUsage('입력 데이터 사이즈가 다릅니다. ', status_code=501)

        # try:
        #     _pattern = Rules_White_IP()
        #     _pattern.ip = request.form['pattern'].strip()
        #     _pattern.mask = request.form['mask'].strip()
        #     _pattern.description = request.form['desc']
        #     db_session.add(_pattern)
        #     db_session.commit()
        # except Exception as e:
        #     db_session.rollback()
        #     raise InvalidUsage('DB 저장 오류', status_code=501)
    else:
        raise InvalidUsage('지원하지 않는 파일 포멧 입니다.', status_code=501)

    return ""



@blueprint_page.route('/white-ip', methods=['POST'])
#@login_required
def addwhiteip():
    exists = Rules_White_IP.query.filter_by(ip=request.form['pattern'].strip()).first()
    if exists is not None:
        raise InvalidUsage('중복 IP가 존재합니다.', status_code=501)

    try:
        _pattern = Rules_White_IP()
        _pattern.ip =request.form['pattern'].strip()
        _pattern.mask = request.form['mask'].strip()
        _pattern.description = request.form['desc']
        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/white-ip/<int:seq>', methods=['PUT'])
#@login_required
def editwhiteip(seq):
    _pattern = db_session.query(Rules_White_IP).filter_by(seq=seq).first()
    try:
        _pattern.ip = request.form['pattern'].strip()
        _pattern.mask = request.form['mask'].strip()
        _pattern.description = request.form['desc']

        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return ""

@blueprint_page.route('/white-ip/<int:seq>', methods=['DELETE'])
#@login_required
def deletewhiteip(seq):
    _pattern = db_session.query(Rules_White_IP).filter_by(seq=seq).first()
    if _pattern is not None :
        db_session.delete(_pattern)
        db_session.commit()
    return ""


@blueprint_page.route('/white-ip/excel-list', methods=['GET','POST'])
#@login_required
def getWhiteListExcel():


    per_page = int(request.form.get('perpage'))
    #draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    keyword = request.form.get('search_keyword').strip()

    query = Rules_White_IP.query

    if keyword != "":
        query = query.filter(Rules_White_IP.ip.like('%' + keyword + '%'))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_White_IP.cre_dt.desc()).paginate(curpage, per_page, error_out=False)
    #inchan = cncList.items[0].ip




    result = OrderedDict()

    result['날짜'] = list()
    result['ip'] = list()
    result['mask'] = list()
    result['description'] = list()
    result['type'] = list()

    for _item in cncList.items:
        result['날짜'].append(_item.cre_dt)
        result['ip'].append(_item.ip)
        result['mask'].append(_item.mask)
        result['description'].append(_item.description)
        result['type'].append(_item.type)

    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")