#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_Crawl import Rules_Crawl
from GSP_WEB.models.SystemCrawler import SystemCrawler
from GSP_WEB.views.rules import blueprint_page

@blueprint_page.route('/crawl', methods=['GET'])
@login_required
def crawl_List():
    nowtime = datetime.datetime.now()
    start_of_day = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)
    #logUtil.addLog(request.remote_addr,1,'rules > crawl-list ')
    pattern_list = CommonCode.query.filter_by(GroupCode = 'crawling input type').all()
    crawl = SystemCrawler()
    crawl.getOptions()
    timefrom = start_of_day.strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('rules/crawl_list.html', pattern_list=pattern_list, crawl=crawl, timefrom = timefrom, timeto=timeto)

@blueprint_page.route('/crawl/list',methods=['POST'] )
@login_required
def crawl_getlist():

    draw = int(request.form.get('draw'))
    startDate = request.form.get('timeFrom')
    endDate = request.form.get('timeTo')
    startDatestr = ""
    endDatestr = ""
    if startDate:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d %H:%M").strftime("%Y.%m.%d")
        #startDatestr = startDate

    if endDate:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d %H:%M").strftime("%Y.%m.%d")
       # endDatestr = endDate.strftime("%Y.%m.%d")

    if not startDate and not endDate:
        startDate = datetime.datetime.now().strftime("%Y.%m.%d")
        endDate = startDate

    # elsaticQuery = 'gsp-{},gsp-{}'.format(startDate, endDate)
    elsaticQuery = 'gsp-*'
    query_type = "uri"
    cncList = Rules_Crawl.getList(elsaticQuery, request)

    total = int(cncList['hits']['total'])
    if total > 10000:
        total = 10000

    input_type = CommonCode.serialize_list(CommonCode.query.filter_by(GroupCode='crawling input type').all())
    for _row in cncList['hits']['hits']:
        val = [x for i, x in enumerate(input_type) if x['Code'] == _row['_source']['register_path']]
        if val.__len__() > 0:
            _row['_source']['register_path_text'] = val[0].get('EXT1')


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = cncList['hits']['hits']

    result["input_type"] = input_type
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/crawl/list_sql',methods=['POST'] )
@login_required
def crawl_getlistSql():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    search_source = request.form.get('search_source')
    keyword = request.form.get('search_keyword').strip()

    query = Rules_Crawl.query

    if search_source != '':
        query = query.filter_by(source = search_source)
    if keyword != "":
        query = query.filter(Rules_Crawl.pattern.like('%'+keyword+'%'))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_Crawl.cre_dt.desc()).paginate(curpage, per_page, error_out=False)

    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = int(cncList.total)
    result["recordsFiltered"] = int(cncList.total)
    result["data"] = Rules_Crawl.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/crawl', methods=['POST'])
@login_required
def addcrawllist():

    try:
        _pattern = Rules_Crawl()
        _pattern.uri =request.form['pattern']
        _pattern.depth = int(request.form['depth'])
        _pattern.desc = request.form['desc']
        _pattern.register_path = request.form['source']
        Rules_Crawl.insertData(_pattern)

    except Exception as e:
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} ## Initially "" empty string handled statement. I put 200 OK to look clean in the UI

@blueprint_page.route('/crawl', methods=['PUT'])
@login_required
def editcrawllist():
    try:
        _pattern = Rules_Crawl()
        _pattern._id = request.form['seq']
        _pattern.uri = request.form['pattern']
        _pattern.depth = int(request.form['depth'])
        _pattern.desc = request.form['desc']
        _pattern.register_path = request.form['source']
        _pattern._index = request.form['index']
        Rules_Crawl.insertData(_pattern)
    except Exception as e:
        raise InvalidUsage('DB 저장 오류', status_code = 501)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} ## Initially "" empty string handled statement. I put 200 OK to look clean in the UI

@blueprint_page.route('/crawldelete', methods=['POST'])
@login_required
def deletecrawllist():
    deleteID = request.form.get('u_id')
    dataDate = request.form.get('u_datadate')
    query = Rules_Crawl()

    elsaticQuery = 'gsp-*'
    query_type = "url_jobs"
    cncList = Rules_Crawl.deleteData(elsaticQuery, dataDate, deleteID)
    # _pattern = db_session.query(Rules_Crawl).filter_by(seq=seq).first()
    # if _pattern is not None :
    #     db_session.delete(_pattern)
    #     db_session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} ## Initially "" empty string handled statement. I put 200 OK to look clean in the UI