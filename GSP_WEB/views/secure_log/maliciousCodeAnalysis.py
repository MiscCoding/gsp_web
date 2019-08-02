# -*- coding: utf-8 -*-
import datetime
import json
import os
from collections import OrderedDict

import flask_excel as excel
from elasticsearch import Elasticsearch
from flask import request, render_template, json, Response, send_file
from six.moves.urllib.parse import urlparse
from werkzeug.utils import secure_filename
from os.path import basename

from GSP_WEB import app, login_required, InvalidUsage, db_session
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.query.secure_log import getMaliciousCodeLogData, getMaliciousCodeLogDetailData, updateCommentQuery, \
    getMaliciousCodeLogDataCount, reanalysisRequestQuery, initializationMaxWindowQuery
from GSP_WEB.views.secure_log import blueprint_page
import zipfile, io

@blueprint_page.route('/maliciousCodeAnalysis', methods=['GET'])
@login_required
def getMaliciousFileLog():
    nowtime = datetime.datetime.now()
    start_of_day = datetime.datetime(nowtime.year, nowtime.month, nowtime.day)
    logUtil.addLog(request.remote_addr, 1, 'secure-log/maliciousCodeAnalysis')
    timefrom = start_of_day.strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    logUtil.addLog(request.remote_addr, 1, 'security log > maliciousCodeAnalysis ')
    type_list = CommonCode.query.filter_by(GroupCode='an_data_from').all()
    max_window_value = CommonCode.query.filter_by(GroupCode='max_window_value').first()

    return render_template('secure_log/maliciousCodeAnalysisNew.html', timefrom=timefrom, timeto=timeto \
                           , type_list=type_list, max_window_value = max_window_value)

@blueprint_page.route('/maliciousCodeAnalysis/max_window_value_set', methods=['PUT'])
def setMaxWindowValueSetNP():
    max_window = CommonCode.query.filter_by(GroupCode='max_window_value').first()
    max_window.EXT1 = request.form.get('max_window_value')
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code=501)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@blueprint_page.route('/maliciousCodeAnalysis/getlist', methods=['POST'])
def getMaliciousFileLogList():
    logList = None

    # region search option
    # per_page = int(request.form['perpage'])
    draw = int(request.form['draw'])
    MaxWindowValue = int(request.form['max_window_value'])

    # start_idx = int(request.form['start'])
    # endregion

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    if app.config["NEW_ES"]:
        query_type = "_doc"
    else:
        query_type = "analysis_info"


    startIndex = int(request.form["start"])

    # bodyQuery = initializationMaxWindowQuery(MaxWindowValue)
    # try:
    #     res = es.indices.put_settings(index="gsp*",
    #                               body= bodyQuery,
    #                               request_timeout=600
    #                               )
    # except Exception as e:
    #     raise "Elasticsearch connection failed while elasticsearch initialization" + e
    #     return None


    if startIndex > MaxWindowValue:
        raise Exception("Request size is larger than the max window size")

    doc = getMaliciousCodeLogData(request,query_type)

    # if res['acknowledged'] is True:
    #     try:
    #         res = es.search(index="gsp*", doc_type="analysis_info", body=doc, request_timeout = 600)
    #     except Exception as e:
    #         raise "Elasticsearch connection failed" + e
    #
    # else:
    #     raise Exception("Elasticsearch initialization failure resulted in data retrieval failure")
    try:
        if app.config["NEW_ES"]:
            idx = "gsp-*-analysis_info"
            res = es.search(index=idx, doc_type=query_type, body=doc, request_timeout=600)
        else:
            res = es.search(index="gsp*", doc_type="analysis_info", body=doc, request_timeout=600)
        # res = es.search(index="gsp*", doc_type="analysis_info", body=doc, request_timeout = 600)
    except Exception as e:
        raise "Elasticsearch connection failed" + e


    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    resultList = []
    # if total >= app.config['ELASTICSEARCH_MAX_WINDOW']:
    #     raise Exception("More Item than max window")



    # C&C타입 목록
    # type_list = CommonCode.query.filter_by(GroupCode='RULE_CNC_TYPE').all()

    for row in esResult:
        resultRow = dict()
        resultRow['_id'] = row['_id']
        resultRow['_index'] = row['_index']
        urlparsed = urlparse(row['_source']['url'])
        url_fore_part = str(urlparsed.scheme) + "://" + str(urlparsed.netloc)
        resultRow['_url_fore_part'] = url_fore_part
        resultRow['_subpath'] = urlparsed.path
        urlparsed = urlparse(row['_source']['url'])
        url_fore_part = str(urlparsed.scheme) + "://" + str(urlparsed.netloc)
        pureUrl = urlparsed.path
        fileName = os.path.basename(pureUrl)
        urlInMiddle = list()
        if fileName != "":
            urlInMiddle = pureUrl.rsplit(fileName, 1)
        else:
            urlInMiddle.append("")

        resultRow['_pureuri'] = (url_fore_part + "/" + urlInMiddle[0])
        resultRow['_source'] = row['_source']
        resultList.append(resultRow)


    result = dict()
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = resultList
    result["draw"] = str(draw)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')


@blueprint_page.route('/maliciousCodeAnalysis/getDetailedResult', methods=['POST'])
def getMaliciousFileLogDetailedList():

    doc_type_obtained = "analysis_url_detail_info"
    detailInfoType = request.form.get('detailType')
    indexFromView = request.form.get('index')
    if app.config["NEW_ES"]:
        idx = indexFromView[:-len('-analysis_info')]
        if detailInfoType == 'url':
            idx = idx + '-analysis_url_detail_info'
            docT = "_doc"
            doc_type_obtained = "analysis_url_detail_info"
        elif detailInfoType == 'file':
            idx = idx + '-analysis_file_detail_info'
            docT = "_doc"
            doc_type_obtained = "analysis_file_detail_info"
    else:
        if detailInfoType == 'url':
            doc_type_obtained = "analysis_url_detail_info"
        elif detailInfoType == 'file':
            doc_type_obtained = "analysis_file_detail_info"

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    query_type = "phrase"
    doc = getMaliciousCodeLogDetailData(request, query_type)
    if app.config["NEW_ES"]:
        res = es.search(index=idx, doc_type=docT, body=doc, request_timeout=360)
    else:
        res = es.search(index=indexFromView, doc_type=doc_type_obtained, body=doc, request_timeout=360)



    esResult = res['hits']['hits']
    total = int(res['hits']['total'])
    resultList = []



    # C&C타입 목록
    #type_list = CommonCode.query.filter_by(GroupCode='RULE_CNC_TYPE').all()

    for row in esResult:
        resultRow = dict()


        if(row['_source']['engine_name'] == 'imas'):
            resultRow['imas'] = row['_source']
        elif(row['_source']['engine_name'] == 'zombiezero'):
            resultRow['zombie'] = row['_source']

        resultList.append(resultRow)


    result = dict()
    result["recordsTotal"] = total
    result["recordsFiltered"] = total
    result["data"] = resultList
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/maliciousCodeAnalysis/updateComment', methods=['POST'])
def updateComment():
    logList = None

    _index = request.form.get('_index')
    _id = request.form.get('_id')

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    query_type = "analysis_info"
    docupdate = updateCommentQuery(request, query_type)
    try:
        res = es.update(index=_index, doc_type="analysis_info", id=_id, body=docupdate, request_timeout = 360)
    except Exception as e:
        raise InvalidUsage("error " + e.message, status_code=501)



    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@blueprint_page.route('/maliciousCodeAnalysis/malfileUpload', methods=['POST'])
@login_required
def addreanalysisfiledata():


    # 파일 로드
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = secure_filename(file.filename)

            try:
                file.save(os.path.join("/usr/gsp/nfs/user/file", file_name))
            except IOError as e:
                raise InvalidUsage("File write failure " + e.message)
            except Exception as e:
                raise InvalidUsage("Unknown failure " + e.message)
    else:
        raise InvalidUsage("No file name found ")

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@blueprint_page.route('/maliciousCodeAnalysis/manualurlanalysisrequest', methods=['POST'])
@login_required
def manualurlanalysisrequest():
    # jsondata = request.form.get("dna_config");

    # 파일 로드
    if request.method == 'POST':
        urldata = request.form.get('_manualurlRequest')
        if urldata:
            datenowstr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = "request_" + datenowstr + ".txt"
            pathandFilename = "/usr/gsp/nfs/user/url/" + file_name
            try:
                text_file = open(pathandFilename, "w")
                text_file.write(urldata)
                text_file.close()
            except IOError as e:
                raise InvalidUsage("File write error " + e.message)
        else:
            raise InvalidUsage("No url received! ");



    else:
        raise InvalidUsage("No Post method received")

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@blueprint_page.route('/maliciousCodeAnalysis/download', methods=['POST'])
@login_required
def maliciouscodedownload():
    # jsondata = request.form.get("dna_config");

    filePathsList = []
    zipfileNameStr = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S");


    # 파일 로드
    if request.method == 'POST':
        filepathnfs = request.form.get('_filepath')
        if filepathnfs:
            filePathsList = filepathnfs.split(",");
            zip_filename = "%s.zip" % zipfileNameStr

            data = io.BytesIO()

            with zipfile.ZipFile(data, mode="w") as z:
                for f_name in filePathsList:
                    z.write(f_name, basename(f_name))


            data.seek(0)

            return send_file(
                data,
                mimetype='application/zip',
                as_attachment = True,
                attachment_filename = zip_filename
            )

            # s = StringIO.StringIO()
            #
            # zf = zipfile.ZipFile(s, "w")
            #
            #
            # for fpath in filePathsList:
            #     fdir, fname = os.path.split(fpath)
            #     zip_path = os.path.join(zipfileNameStr, fname)
            #
            #     zf.write(fpath, zip_path)
            #
            # zf.close()
            #
            # try:
            #     headers = Headers()
            #     headers.add('Content-Disposition', 'attachment', filename=zip_filename)
            #     download_obj = open(s.getvalue(), "rb")
            #     headers['Content-Length'] = os.path.getsize(s.getvalue())
            # except IOError as e:
            #     raise InvalidUsage("File not found" + e.message)
            #
            # def generate():
            #     for block in iter(lambda: download_obj.read(4096), b""):
            #         yield block
            #
            #     download_obj.close()
            #
            # return Response(generate(), mimetype="application/octet-stream", headers=headers)

    else:
        raise InvalidUsage("No Post method received")

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@blueprint_page.route('/maliciousCodeAnalysis/reanalysisRequest', methods=['POST'])
def reanalysisRequest():
    logList = None

    _index = request.form.get('_index')
    _id = request.form.get('_id')

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    query_type = "analysis_info"
    docupdate = reanalysisRequestQuery(request, query_type)
    try:
        res = es.update(index=_index, doc_type="analysis_info", id=_id, body=docupdate, request_timeout = 360)
    except Exception as e:
        raise InvalidUsage("error " + e.message, status_code=501)



    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@blueprint_page.route('/maliciousCodeAnalysis/deleteSigleElement', methods=['POST'])
def deleteSingleElement():
    logList = None

    _index = request.form.get('_index')
    _id = request.form.get('_id')

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])

    deleteDoc = {
                  "query": {
                    "bool": {
                      "must": [{"match": {"analysis_info_id": { "query" : _id, "type": "phrase"}}}]
                    }
                  }
                }

    try:
        res = es.delete(index=_index, doc_type="analysis_info", id=_id)
    except Exception as e:
        raise InvalidUsage('Elastic error ' + e.message, status_code=501)

    try:
        res = es.delete_by_query(index=_index, body= deleteDoc, doc_type = "analysis_file_detail_info", request_timeout = 360)
        #res = es.delete(index=_index, doc_type="analysis_file_detail_info", id=_id)
    except Exception as e:
        pass

    try:
        res = es.delete_by_query(index=_index, body=deleteDoc, doc_type = "analysis_url_detail_info", request_timeout = 360)
    except Exception as e:
        pass



    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@blueprint_page.route('/maliciousCodeAnalysis/excel-list', methods=['GET','POST'])
#@login_required
def getMaliciousFileLogListExcel():
    logList = None

    # start_idx = int(request.form['start'])
    MaxWindowValue = int(request.form['max_window_value'])



    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    query_type = "analysis_info"
    documentCount = getMaliciousCodeLogDataCount(request, query_type, per_pageP=None)
    resCountDoc = es.count(index="gsp*" + "", doc_type="analysis_info", body=documentCount, request_timeout = 600)
    doc = getMaliciousCodeLogData(request, query_type, resCountDoc['count'])
    res = es.search(index="gsp*" + "", doc_type="analysis_info", body=doc)

    esResult = res['hits']['hits']
    resultList = []



    # C&C타입 목록
    # type_list = CommonCode.query.filter_by(GroupCode='RULE_CNC_TYPE').all()

    for row in esResult:
        resultRow = dict()
        resultRow['_id'] = row['_id']
        resultRow['_index'] = row['_index']
        resultRow['_source'] = row['_source']
        resultList.append(resultRow)


    result = OrderedDict()

    result['Date'] = list()
    result['fullurl'] = list()
    result['url'] = list()
    result['subpath'] = list()
    result['uri'] = list()
    result['IP'] = list()
    result['Country'] = list()
    result['File'] = list()
    result['MD5'] = list()
    result['Detection_source'] = list()
    result['Detection_name'] = list()
    result['URI_analysis_result'] = list()
    result['File_analysis_result'] = list()
    result['Comments'] = list()

    for _item in resultList:
        result['Date'].append(_item['_source']['kor_timestamp'])
        result['fullurl'].append(_item['_source']['url'])
        urlparsed = urlparse(_item['_source']['url'])
        url_fore_part = str(urlparsed.scheme) + "://" + str(urlparsed.netloc)
        pureUrl = urlparsed.path
        fileName = os.path.basename(pureUrl)
        urlInMiddle = list()
        if fileName != "":
            urlInMiddle = pureUrl.rsplit(fileName, 1)
        else:
            urlInMiddle.append("")
        result['url'].append(url_fore_part)
        result['subpath'].append(urlparsed.path)
        result['uri'].append(url_fore_part + "/" + urlInMiddle[0])
        result['IP'].append(_item['_source']['dst_ip'])
        result['Country'].append(_item['_source']['dst_country_code1'])
        result['File'].append(_item['_source']['file_name'])
        result['MD5'].append(_item['_source']['md5'])
        result['Detection_source'].append(_item['_source']['data_type'])
        result['Detection_name'].append(_item['_source']['malware_comment'])
        URI_Analysis_Result = str(_item['_source']['detect_cnt_url'])+ "/"+ str(_item['_source']['total_cnt_url'])
        File_Analysis_Result = str(_item['_source']['detect_cnt_file'])+"/" + str(_item['_source']['total_cnt_file'])
        result['URI_analysis_result'].append(URI_Analysis_Result)
        result['File_analysis_result'].append(File_Analysis_Result)
        result['Comments'].append(_item['_source']['comment'] if _item['_source']['comment'] is not None else "")

    return excel.make_response_from_dict(result, "xlsx",
                                          file_name="export_data")


