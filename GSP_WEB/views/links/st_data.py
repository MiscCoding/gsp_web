#-*- coding: utf-8 -*-
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session
from sqlalchemy import or_, and_

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.DNA_StandardData import DNA_StandardData
import csv

from GSP_WEB.models.Link_Element_TypeA import Link_Element_TypeA
from GSP_WEB.models.Link_Element_TypeB import Link_Element_TypeB
from GSP_WEB.views.links import blueprint_page
import re

@blueprint_page.route('/st_data', methods=['GET'])
@login_required
def stData():
    #logUtil.addLog(request.remote_addr,1,'links > list ')

    return render_template('links/st_data.html')

@blueprint_page.route('/st_data/list', methods=['POST'])
@login_required
def getStData():
    # logUtil.addLog(request.remote_addr,1,'links > list ')

    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    search_type = request.form.get('search_type')
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()

    query = DNA_StandardData.query.filter(DNA_StandardData.del_yn == 'N')

    if keyword != "":
        query = query.filter(DNA_StandardData.name.like('%' + keyword + '%'))

    curpage = int(start_idx / per_page) + 1
    dndList = query.order_by(DNA_StandardData.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(dndList.total)
    result["recordsFiltered"] = str(dndList.total)
    result["data"] = DNA_StandardData.serialize_list(dndList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/st_data', methods=['POST'] )
def addStData():
    jsondata = request.form.get("dna_config");

    #파일 로드

    file = request.files['file']
    if file.content_type == 'application/vnd.ms-excel':
        try:
            datalist = []
            spamreader = csv.reader(file)

            for index, row in enumerate(spamreader):
                if index == 0 and isNumberString(row[0]) != True:
                    continue
                if isNumberString(row[0]) == True:
                    datalist.append(row[0])
                else:
                    datalist.append(None)

        except Exception as e:
            raise InvalidUsage('CSV 로딩 실패', status_code=501)

        # target link와 데이터 크기 비교
        target_type = request.form.get("target_type")
        target_seq = request.form.get("target_seq")
        if ValidateTargetSize(datalist.__len__(), target_type, target_seq) == False:
            raise InvalidUsage('입력 데이터 사이즈가 다릅니다. ', status_code=501)
        
        try:
            dna = DNA_StandardData()
            dna.name = request.form.get("name")
            dna.list_data = json.dumps(datalist)
            dna.list_size = datalist.__len__()
            dna.mod_dt = datetime.datetime.now()
            dna.target_link_type = request.form.get("target_type")
            dna.target_link_seq = request.form.get("target_seq")
            dna.del_yn = 'N'
            db_session.add(dna)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise InvalidUsage('DB 저장 오류', status_code=501)
    else:
        raise InvalidUsage('지원하지 않는 파일 포멧 입니다.', status_code=501)

    return ""


@blueprint_page.route('/st_data/<int:id>', methods=['PUT'])
def editStData(id):

    # 파일 로드
    file = request.files.get('file')
    if file is not None and file.content_type == 'application/vnd.ms-excel':
        try:
            datalist = []
            spamreader = csv.reader(file)
            for index, row in enumerate(spamreader):
                if index == 0 and isNumberString(row[0]) != True:
                    continue
                datalist.append(row[0])

        except Exception as e:
            raise InvalidUsage('CSV 로딩 실패', status_code=501)

        # target link와 데이터 크기 비교
        target_type = request.form.get("target_type")
        target_seq = request.form.get("target_seq")
        if ValidateTargetSize(datalist.__len__(), target_type, target_seq) == False:
            raise InvalidUsage('입력 데이터 사이즈가 다릅니다. ', status_code=501)

        try:
            dna = DNA_StandardData.query.filter_by(id=id).first()
            dna.name = request.form.get("name")
            dna.list_data = json.dumps(datalist)
            dna.list_size = datalist.__len__()
            dna.target_link_type = request.form.get("target_type")
            dna.target_link_seq = request.form.get("target_seq")
            dna.mod_dt = datetime.datetime.now()
            dna.del_yn = 'N'
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise InvalidUsage('DB 저장 오류', status_code=501)
    elif file is None :
        dna = DNA_StandardData.query.filter_by(id=id).first()
        dna.name = request.form.get("name")
        dna.target_link_type = request.form.get("target_type")
        dna.target_link_seq = request.form.get("target_seq")
        dna.mod_dt = datetime.datetime.now()
        dna.del_yn = 'N'
        db_session.commit()
    else:
        raise InvalidUsage('지원하지 않는 파일 포멧 입니다.', status_code=501)

    return ""

@blueprint_page.route('/st_data/download/<int:id>', methods=['GET'])
def downStData(id):

    json_listData = DNA_StandardData.query.filter_by(id = id).first().list_data
    listData = json.loads(json_listData)
    si = None
    try:
        si = StringIO()
    except Exception:
        si = StringIO.StringIO()
    cw = csv.writer(si)

    for _row in listData:
        cw.writerow([_row])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@blueprint_page.route('/st_data/<int:id>', methods=['DELETE'])
def delStData(id):
    try:
        dna = DNA_StandardData.query.filter_by(id=id).first()
        dna.del_yn = 'Y'
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code=501)

    return ""

@blueprint_page.route('/st_data/full-list', methods=['GET'])
#@login_required
def getFullStData():
    # logUtil.addLog(request.remote_addr,1,'links > list ')

    query = DNA_StandardData.query.filter(DNA_StandardData.del_yn == 'N')

    result = DNA_StandardData.serialize_list(query.all())
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

def isNumberString(str):
    try:
        m = re.search(r'\d+', str)
        number = m.group()
        float(number)
        return True
    except Exception:
        return False

def ValidateTargetSize(size, target_type, target_id):
    link = None
    if target_type == "a":
        link = Link_Element_TypeA.query.filter_by(id = target_id).first()

        #size가 비어있으면 시계열 형태
        if link.dst_data_size is None:
            if size == 7 or size == 24 or size == 144:
                return True
            else:
                return False
        else:
            if link.dst_data_size == size:
                return True
            else:
                return False

    else:
        link = Link_Element_TypeB.query.filter_by(id = target_id).first()
        if link.dst_data_size == size:
            return True
        else:
            return False


