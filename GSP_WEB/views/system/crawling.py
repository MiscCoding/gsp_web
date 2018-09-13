#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session
from sqlalchemy import and_

from GSP_WEB import login_required, db_session, app, EncryptEncoder
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.common.util.textUtil import RepresentsInt
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.GlobalSetting import GlobalSetting
from GSP_WEB.models.IP_BlackList import IP_BlackList
from GSP_WEB.models.IP_WhiteList import IP_WhiteList
from GSP_WEB.models.Account import Account
from GSP_WEB.models.SystemCrawler import SystemCrawler

blueprint_page = Blueprint('bp_system_crawling_page', __name__, url_prefix='/system')

@blueprint_page.route('/crawling', methods=['GET'])
@login_required
def crawlingList():
    logUtil.addLog(request.remote_addr,1,'system>crawling')
    crawl = SystemCrawler()
    crawl.getOptions()

    return render_template('system/crawling.html', crawl = crawl)


@blueprint_page.route('/crawling', methods=['POST'])
def save_crawlingList():
    try:
        depth = CommonCode.query.filter(and_(CommonCode.GroupCode == "cl", CommonCode.Code == "001")).first()
        depth.EXT1 = request.form.get('depth')
        extension = CommonCode.query.filter(and_(CommonCode.GroupCode == "cl", CommonCode.Code == "002")).first()
        extension.EXT1 = request.form.get('extionsions')
        max_size = CommonCode.query.filter(and_(CommonCode.GroupCode == "cl", CommonCode.Code == "003")).first()
        max_size.EXT1 = request.form.get('maxsize')
        timeout = CommonCode.query.filter(and_(CommonCode.GroupCode == "cl", CommonCode.Code == "004")).first()
        timeout.EXT1 = request.form.get('timeout')
        db_session.commit()

    except Exception as e:
        db_session.rollback()
        #print e.message
        raise InvalidUsage('DB 저장 오류', status_code=501)

    return ""
