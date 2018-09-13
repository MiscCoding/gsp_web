#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session

from GSP_WEB import login_required, db_session, app
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.common.util.textUtil import RepresentsInt
from GSP_WEB.models.IP_WhiteList import IP_WhiteList
from GSP_WEB.models.Account import Account

blueprint_page = Blueprint('bp_alert_page', __name__, url_prefix='/system')

@blueprint_page.route('/alert', methods=['GET'])
@login_required
def alert():
    return render_template('system/alert.html')