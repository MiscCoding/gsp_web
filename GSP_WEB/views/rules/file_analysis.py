#-*- coding: utf-8 -*-
import sys
#python 2.7 버전 사용시 주석 해제
# reload(sys)
# sys.setdefaultencoding('utf-8')
import datetime

import os

from elasticsearch import Elasticsearch
from flask import request, Response, render_template, Blueprint, json, make_response, g, session, send_from_directory
from sqlalchemy import or_

from GSP_WEB import db_session, login_required, app
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.Rules_FileAnalysis import Rules_FileAnalysis
from GSP_WEB.views.rules import blueprint_page
from flask_uploads import (UploadSet, UploadConfiguration, ALL)

@blueprint_page.route('/file-analysis', methods=['GET'])
@login_required
def filesnalysis_List():
    logUtil.addLog(request.remote_addr,1,'rules > file-analysis ')

    return render_template('rules/file_analysis_list.html')

@blueprint_page.route('/file-analysis/<int:seq>', methods=['GET'])
@login_required
def filesnalysis_download(seq):

    fileanalysis = Rules_FileAnalysis.query.filter_by(seq=seq).first()
    if fileanalysis is not None:
        uploadpath = app.config['UPLOAD_FOLDER']
        fullpath = os.path.join(uploadpath,app.config['UPLOAD_CRAWLING_FOLDER'] , fileanalysis.subpath)
        return send_from_directory(directory=fullpath, filename=fileanalysis.realfilename, as_attachment=True
                                   ,attachment_filename = fileanalysis.orgfilename)
    else:
        return ""

@blueprint_page.route('/file-analysis/list',methods=['POST'] )
def filesnalysis_getlist():
    per_page = int(request.form.get('perpage'))
    draw = int(request.form.get('draw'))
    start_idx = int(request.form.get('start'))
    keyword = request.form.get('search_keyword').strip()

    query = Rules_FileAnalysis.query

    if keyword != "":
        query = query.filter(or_(Rules_FileAnalysis.orgfilename.like('%'+keyword+'%'), Rules_FileAnalysis.description.like('%'+keyword+'%')))

    curpage = int(start_idx / per_page) + 1
    cncList = query.order_by(Rules_FileAnalysis.cre_dt.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(cncList.total)
    result["recordsFiltered"] = str(cncList.total)
    result["data"] = Rules_FileAnalysis.serialize_list(cncList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/file-analysis', methods=['POST'])
#@login_required
def addfilesnalysislist():
    # dupCheckResult = db_session.query(Account).filter_by(id=id).first()
    # if dupCheckResult is not None:
    #     raise InvalidUsage('중복된 아이디가 있습니다.', status_code=500)
    try:
        if request.files['files'] is not None:
            Config = UploadConfiguration
            uset = UploadSet('files', ALL)
            #uset._config = Config('/usr/gsp/web_uploads')
            uploadpath = app.config['UPLOAD_FOLDER']
            subpath = datetime.datetime.now().strftime('%Y%m%d')
            combinepath = os.path.join(uploadpath,app.config['UPLOAD_CRAWLING_FOLDER'], subpath)
            uset._config = Config(combinepath)

            #DB 데이터 입력
            fileAnalysis = Rules_FileAnalysis()
            fileAnalysis.realfilename = uset.save(request.files['files'])
            fileAnalysis.orgfilename = request.files['files'].filename
            fileAnalysis.subpath = subpath
            fileAnalysis.description = request.form.get('desc')
            fileAnalysis.cre_id = session['id']
            db_session.add(fileAnalysis)
            db_session.commit()

            #elastic search 데이터 입력
            es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
            doc = {
                '@timestamp': datetime.datetime.utcnow().isoformat()
                , 'fileExt': os.path.splitext(fileAnalysis.orgfilename)[1]
                , 'nfs_path': ".\\{0}\\{1}\\{2}".format(app.config['UPLOAD_CRAWLING_FOLDER'], subpath
                                                        , fileAnalysis.realfilename, fileAnalysis.realfilename)
                , 'data_type': "crawlings"
                , 'filePath':  os.path.join(combinepath, fileAnalysis.realfilename)
                , 'fileName' : fileAnalysis.realfilename
                , 'origianl_fileName' : fileAnalysis.orgfilename
                , 'register_path': "001"
                , 'status' : 0
            }
            _index = 'gsp-{0}'.format(datetime.datetime.now().strftime("%Y.%m.%d"))
            es.index(index=_index, doc_type="url_crawleds", body=doc)

            return ""
    except Exception as e:
        db_session.rollback()
        raise InvalidUsage('DB 저장 오류', status_code = 501)

    return ""
