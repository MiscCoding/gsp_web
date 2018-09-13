#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session
from sqlalchemy import or_, and_

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.DNA_Element import DNA_Element
from GSP_WEB.models.DNA_Schedule import DNA_Schedule

from GSP_WEB.views.dna import blueprint_page

@blueprint_page.route('/schedule', methods=['GET'])
@login_required
def scheduleList():
    #logUtil.addLog(request.remote_addr,1,'links > list ')
    timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    type_list = CommonCode.query.filter_by(GroupCode='raw_data_type').all()
    dna_list = DNA_Element.query.filter_by( del_yn = "N", use_yn="Y" )
    return render_template('dna/schedule.html', timenow = timenow, type_list = type_list, dna_list = dna_list)

@blueprint_page.route('/schedule/list', methods=['POST'])
@login_required
def get_schedulelist():
    #logUtil.addLog(request.remote_addr,1,'links > list ')

    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    search_type = request.form.get('search_type')
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()

    query = DNA_Schedule.query.filter(DNA_Schedule.del_yn == 'N')

    if keyword != "":
        query = query.filter(DNA_Schedule.dna_name.like('%' + keyword + '%'))

    curpage = int(start_idx / per_page) + 1
    dndList = query.order_by(DNA_Schedule.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(dndList.total)
    result["recordsFiltered"] = str(dndList.total)
    result["data"] = DNA_Schedule.serialize_list(dndList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/schedule', methods=['POST'])
#@login_required
def addSchedule():
    try:
        schedule = DNA_Schedule()
        schedule.dna_id = request.form['dna_id']
        schedule.description = request.form['desc']
        schedule.cycle =request.form['cycle_value']+request.form['cycle_opt']
        schedule.start_time = request.form['start_time']
        schedule.cre_id = session.get('id')
        schedule.filter_ip = request.form['filter_ip']
        schedule.filter_data_type = request.form['filter_data_type']
        db_session.add(schedule)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/schedule/<int:seq>', methods=['PUT'])
@login_required
def editSchedule(seq):
    try:
        schedule = db_session.query(DNA_Schedule).filter_by(id=seq).first()
        schedule.dna_id = request.form['dna_id']
        schedule.description = request.form['desc']
        schedule.cycle =request.form['cycle_value']+request.form['cycle_opt']
        schedule.start_time = request.form['start_time']
        schedule.cre_id = session.get('id')
        schedule.filter_ip = request.form['filter_ip']
        schedule.filter_data_type = request.form['filter_data_type']
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/scheduleRestart/<int:seq>', methods=['PUT'])
@login_required
def editRestartSchedule(seq):
    try:
        schedule = db_session.query(DNA_Schedule).filter_by(id=seq).first()
        schedule.restart_request = 1

        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""



@blueprint_page.route('/schedule/<int:seq>', methods=['DELETE'])
@login_required
def deleteSchedule(seq):
    schedule = db_session.query(DNA_Schedule).filter_by(id=seq).first()
    if schedule is not None :
        schedule.del_yn = 'Y'
        db_session.commit()
    return ""