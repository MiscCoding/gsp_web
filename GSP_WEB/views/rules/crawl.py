#-*- coding: utf-8 -*-
import csv
import datetime
from collections import OrderedDict

from dateutil import parser

from flask import request, Response, render_template, Blueprint, json, make_response, g, session
import flask_excel as excel

from GSP_WEB import db_session, login_required
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_Crawl import Rules_Crawl
from GSP_WEB.models.SystemCrawler import SystemCrawler
from GSP_WEB.views.rules import blueprint_page
from GSP_WEB.models.Manual_Crawling_Info import Manual_Crawling_Info

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
    per_page = int(request.form.get('perpage'))
    start_idx = int(request.form.get('start'))
    draw = int(request.form.get('draw'))
    startDate = request.form.get('timeFrom')
    endDate = request.form.get('timeTo')
    searchKeyword = request.form.get('search_keyword')
    startDatestr = ""
    endDatestr = ""
    if startDate:
        # startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d %H:%M").strftime("%Y.%m.%d")
        startDate = parser.parse(request.form['timeFrom']).isoformat()
        #startDatestr = startDate

    if endDate:
       endDate = parser.parse(request.form['timeTo']).isoformat()
       # endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d %H:%M").strftime("%Y.%m.%d")

       # endDatestr = endDate.strftime("%Y.%m.%d")

    if not startDate and not endDate:
        startDate = datetime.datetime.now().strftime("%Y.%m.%d")
        endDate = startDate

    query = Manual_Crawling_Info.query.filter(Manual_Crawling_Info.register_date.between(startDate, endDate))

    if searchKeyword != '':
        query = query.filter(Manual_Crawling_Info.url.like('%' + searchKeyword + '%'))

    curpage = int(start_idx / per_page) + 1

    cncList = query.order_by(Manual_Crawling_Info.register_date.desc()).paginate(curpage, per_page, error_out=True)
    # cncList = query.order_by(Manual_Crawling_Info.register_date.desc())


    # elsaticQuery = 'gsp-{},gsp-{}'.format(startDate, endDate)
    # elsaticQuery = 'gsp-*'
    # query_type = "uri"
    # cncList = Rules_Crawl.getList(elsaticQuery, request)
    #
    # total = int(cncList['hits']['total'])
    # if total > 10000:
    #     total = 10000
    #
    # input_type = CommonCode.serialize_list(CommonCode.query.filter_by(GroupCode='crawling input type').all())
    # for _row in cncList['hits']['hits']:
    #     val = [x for i, x in enumerate(input_type) if x['Code'] == _row['_source']['register_path']]
    #     if val.__len__() > 0:
    #         _row['_source']['register_path_text'] = val[0].get('EXT1')


    result = dict()
    result["draw"] = str(draw)
    # result["recordsTotal"] = total
    # result["recordsFiltered"] = total
    # result["data"] = cncList['hits']['hits']
    result["recordsTotal"] = cncList.total
    result["recordsFiltered"] = cncList.total
    result["data"] = Manual_Crawling_Info.serialize_list(cncList.items)

    # result["input_type"] = input_type
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

    # try:
    #     _pattern = Rules_Crawl()
    #     _pattern.uri =request.form['pattern']
    #     _pattern.depth = int(request.form['depth'])
    #     _pattern.desc = request.form['desc']
    #     _pattern.register_path = request.form['source']
    #     Rules_Crawl.insertData(_pattern)
    #
    # except Exception as e:
    #     raise InvalidUsage('DB 저장 오류', status_code = 501)
    try:
        _pattern = Manual_Crawling_Info()
        # _pattern.type = request.form['type']

        _pattern.depth = request.form['depth'].strip()
        _pattern.url = request.form['url'].strip()
        # _pattern.mask = request.form['mask'].strip()
        _pattern.comment = request.form['comment']
        db_session.add(_pattern)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

    # return json.dumps({'success':True}), 200, {'ContentType':'application/json'} ## Initially "" empty string handled statement. I put 200 OK to look clean in the UI

@blueprint_page.route('/crawl/batchUpload', methods=['POST'])
@login_required
def addcrawllistBatch():

    # try:
    #     _pattern = Rules_Crawl()
    #     _pattern.uri =request.form['pattern']
    #     _pattern.depth = int(request.form['depth'])
    #     _pattern.desc = request.form['desc']
    #     _pattern.register_path = request.form['source']
    #     Rules_Crawl.insertData(_pattern)
    #
    # except Exception as e:
    #     raise InvalidUsage('DB 저장 오류', status_code = 501)
    file = request.files['file']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if file.filename.split(".")[1] == 'csv':
        try:
            datalist = []
            spamreader = csv.reader(file)
            next(spamreader)
            for index, row in enumerate(spamreader):

                # if str(row[0]) not in ["Portal", "Video", "AntiVirus", "SNS", "Network", "Server", "Etc"]:
                #     raise InvalidUsage('Type value is not valid', status_code=501)
                #
                # if int(row[2]) not in [8, 16, 24, 32]:
                #     raise InvalidUsage('Mask value is not valid', status_code=501)

                try:
                    _pattern = Manual_Crawling_Info()
                    _pattern.url = str(row[0])
                    _pattern.depth = int(row[1])
                    _pattern.comment = str(row[2])
                    _pattern.register_from = str(row[3])
                    _pattern.register_date = timestamp
                    # _pattern.description = row[4]

                    db_session.add(_pattern)
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    raise InvalidUsage('DB 저장 오류' + index + " line ", status_code=501)

        except Exception as e:
            raise InvalidUsage('CSV 로딩 실패, ' + e.message, status_code=501)
    else:
        raise InvalidUsage('지원하지 않는 파일 포멧 입니다.', status_code=501)
    # try:
    #     _pattern = Manual_Crawling_Info()
    #     # _pattern.type = request.form['type']
    #
    #     _pattern.depth = request.form['depth'].strip()
    #     _pattern.url = request.form['url'].strip()
    #     # _pattern.mask = request.form['mask'].strip()
    #     _pattern.comment = request.form['comment']
    #     db_session.add(_pattern)
    #     db_session.commit()
    # except Exception as e:
    #     db_session.rollback()
    #     raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""

@blueprint_page.route('/crawl/sample-excel-list', methods=['GET','POST'])
#@login_required
def getCrawlingBatchExcel_sample():
    # -*- coding: utf-8 -*-
    sample = request.form.get('sample').strip()

    result = OrderedDict()


    result['URL'] = list()
    result['Depth'] = list()
    result['Comment'] = list()
    result['Register_from'] = list()
    # result['description'] = list()

    result['URL'].append("http://www.daum.net")
    result['Depth'].append("1")
    result['Comment'].append(u"User Input")
    result['Register_from'] .append(u"International")
    # result['type'].append("Network")
    # result['ip'].append("111.112.33.54")
    # result['mask'].append("32")
    # result['url'].append("http://www.daum.net")
    # result['description'].append("자동 등록")


    return excel.make_response_from_dict(result, "csv",
                                          file_name="export_data")

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
    # query = Rules_Crawl()


    # elsaticQuery = 'gsp-*'
    # query_type = "url_jobs"
    # cncList = Rules_Crawl.deleteData(elsaticQuery, dataDate, deleteID)
    _pattern = db_session.query(Manual_Crawling_Info).filter_by(idx=deleteID).first()
    if _pattern is not None :
        db_session.delete(_pattern)
        db_session.commit()
    # return json.dumps({'success':True}), 200, {'ContentType':'application/json'} ## Initially "" empty string handled statement. I put 200 OK to look clean in the UI
    return ''