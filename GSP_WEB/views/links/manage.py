#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session
from sqlalchemy import or_, and_

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Data_Element import Data_Element
from GSP_WEB.models.Link_Element_List import Link_Element_List
from GSP_WEB.models.Link_Element_TypeA import Link_Element_TypeA
from GSP_WEB.models.Link_Element_TypeB import Link_Element_TypeB

from GSP_WEB.views.links import blueprint_page

@blueprint_page.route('/list', methods=['GET'])
@login_required
def linkList():
    #logUtil.addLog(request.remote_addr,1,'links > list ')
    type_list = CommonCode.query.filter_by(GroupCode = 'raw_data_type').all()

    return render_template('links/list.html', type_list = type_list)

@blueprint_page.route('/getlist',methods=['POST'] )
@login_required
def getList():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    keyword = request.form.get('search_keyword').strip()

    list = Link_Element_List()
    list.getList(start_idx, per_page, keyword)

    curpage = int(start_idx / per_page) + 1

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = list.total
    result["recordsFiltered"] = list.total
    result["data"] = list.data
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/type-a',methods=['POST'] )
#@login_required
def addTypeA():
    existResult = db_session.query(Link_Element_TypeA).filter_by(src_type = request.form['type'])\
        .filter_by(dst_columns_name=request.form['dst_column']).first()
    if (existResult != None):
        raise InvalidUsage('중복된 요소가 존재합니다.', status_code=501)

    src_dataElement = Data_Element.query.filter_by(data_source=request.form['type']). \
        filter_by(column_name=request.form['src_column']).first()

    try:
        _pattern = Link_Element_TypeA()
        _pattern.src_type = request.form['type']
        _pattern.src_columns_name = request.form['src_column']
        _pattern.dst_columns_name = request.form['dst_column']
        _pattern.description = request.form['desc']
        _pattern.dst_data_type = src_dataElement.getLinkDataType()[0]
        _pattern.dst_data_size = src_dataElement.getLinkDataType()[1]
        _pattern.use_yn = request.form['use_yn']
        _pattern.del_yn = 'N'

        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code=501)

    return ""

@blueprint_page.route('/type-a/<int:seq>',methods=['PUT'] )
#@login_required
def editTypeA(seq):

    try:
        existResult = db_session.query(Link_Element_TypeA).filter(
                and_(Link_Element_TypeA.id != seq , Link_Element_TypeA.dst_columns_name == request.form['dst_column'],
                     Link_Element_TypeA == request.form['type'])
            ).all()
        if (existResult != None and existResult.__len__() > 0):
            raise InvalidUsage('중복된 요소가 존재합니다.', status_code=501)

        src_dataElement = Data_Element.query.filter_by(data_source = request.form['type']).\
            filter_by(column_name = request.form['src_column']).first()

        _pattern = Link_Element_TypeA.query.filter_by(id = seq).first()
        _pattern.src_type = request.form['type']
        _pattern.src_columns_name = request.form['src_column']
        _pattern.dst_columns_name = request.form['dst_column']
        _pattern.description = request.form['desc']
        _pattern.dst_data_type = src_dataElement.getLinkDataType()[0]
        _pattern.dst_data_size = src_dataElement.getLinkDataType()[1]
        _pattern.use_yn = request.form['use_yn']
        _pattern.del_yn = 'N'

        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code=501)

    return ""

@blueprint_page.route('/element-list',methods=['GET'] )
#@login_required
def getElementList():
    elementList = dict()
    list_a = Link_Element_TypeA.query.filter(
        and_(Link_Element_TypeA.use_yn == 'Y', Link_Element_TypeA.del_yn == 'N')).all()
    list_b = Link_Element_TypeB.query.filter(
        and_(Link_Element_TypeB.use_yn == 'Y', Link_Element_TypeB.del_yn == 'N')).all()
    elementList['TypeA'] = Link_Element_TypeA.serialize_list(list_a)
    elementList['TypeB'] = Link_Element_TypeB.serialize_list(list_b)

    return json.dumps(elementList)

@blueprint_page.route('/type-b',methods=['POST'] )
#@login_required
def addTypeB():
    existResult = db_session.query(Link_Element_TypeB).filter_by(dst_columns_name=request.form['name']).first()
    if (existResult != None):
        raise InvalidUsage('중복된 요소가 존재합니다.', status_code=501)

    try:
        _pattern = Link_Element_TypeB()
        _pattern.dst_columns_name = request.form['name']
        _pattern.description = request.form['desc']

        #operationFuntion 파라메터 생성
        opFunction = list()
        col0 = {
            "type" : request.form.get("src_type0"),
            "id" : request.form.get("src_column0"),
            "op": request.form.get("src_column_op0")
        }
        opFunction.append(col0)
        #요소 Source가 복수개인 경우
        if request.form.get("colCnt") == "2":
            col1 = {
                "type": request.form.get("src_type1"),
                "id": request.form.get("src_column1"),
                "op": request.form.get("src_column_op1")
            }
            opFunction.append(col1)

        time_range = None

        if request.form.get("tr_op") is not None:
            time_range = {
                "unit" : request.form.get("tr_unit"),
                "value" : [ request.form.get("tr_value0") ],
                "op" : request.form.get("tr_op")
            }
            if request.form.get("tr_value1") is not None:
                time_range["value"].append(request.form.get("tr_value1"))

        _pattern.setOperateFunction( opFunction, request.form.get("op"), time_range)

        _pattern.description = request.form['desc']
        _pattern.analysis_cycle = request.form['cycle_value'] + request.form['cycle_opt']
        _pattern.timespan = request.form['timespan_opt'] if request.form['timespan_opt'] != '' else ''
        _pattern.dst_data_type = 'single' if request.form['timespan_opt'] == '' else 'list'
        _pattern.use_yn = request.form['use_yn']
        _pattern.del_yn = 'N'

        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code=501)

    return ""

@blueprint_page.route('/type-b/<int:seq>',methods=['PUT'] )
#@login_required
def editTypeB(seq):

    try:
        _pattern = Link_Element_TypeB.query.filter_by(id=seq).first()
        _pattern.dst_columns_name = request.form['name']
        _pattern.description = request.form['desc']

        #operationFuntion 파라메터 생성
        opFunction = list()
        col0 = {
            "type" : request.form.get("src_type0"),
            "id" : request.form.get("src_column0"),
            "op": request.form.get("src_column_op0")
        }
        opFunction.append(col0)
        #요소 Source가 복수개인 경우
        if request.form.get("colCnt") == "2":
            col1 = {
                "type": request.form.get("src_type1"),
                "id": request.form.get("src_column1"),
                "op": request.form.get("src_column_op1")
            }
            opFunction.append(col1)

        time_range = None

        if request.form.get("tr_op") is not None:
            time_range = {
                "unit" : request.form.get("tr_unit"),
                "value" : [ request.form.get("tr_value0") ],
                "op" : request.form.get("tr_op")
            }
            if request.form.get("tr_value1") is not None:
                time_range["value"].append(request.form.get("tr_value1"))

        _pattern.setOperateFunction( opFunction, request.form.get("op"), time_range)
        _pattern.description = request.form['desc']
        _pattern.analysis_cycle = request.form['cycle_value'] + request.form['cycle_opt']
        _pattern.timespan = request.form['timespan_opt'] if request.form['timespan_opt'] != '' else ''
        _pattern.dst_data_type = 'single' if request.form['timespan_opt'] == '' else 'list'
        _pattern.use_yn = request.form['use_yn']
        _pattern.del_yn = 'N'
        _pattern.mod_dt = datetime.datetime.now()

        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code=501)

    return ""

@blueprint_page.route('/type-b/<int:seq>',methods=['DELETE'] )
#@login_required
def delTypeB(seq):
    link = db_session.query(Link_Element_TypeB).filter_by(id=seq).first()
    if link is not None:
        link.del_yn = 'Y'
        db_session.commit()
    return ""

@blueprint_page.route('/type-a/<int:seq>',methods=['DELETE'] )
#@login_required
def delTypeA(seq):
    link = db_session.query(Link_Element_TypeA).filter_by(id=seq).first()
    if link is not None:
        link.del_yn = 'Y'
        db_session.commit()
    return ""

@blueprint_page.route('/data-list/<string:datasource>',methods=['GET','POST'])
def getDataElementList(datasource):
    data_list = Data_Element.query.filter(and_(Data_Element.del_yn == 'N', Data_Element.use_yn == 'Y'))\
        .filter_by(data_source = datasource).all()
    result = dict()
    result["data"] = Data_Element.serialize_list(data_list)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

