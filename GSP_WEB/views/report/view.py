import datetime
from flask import request, Response, render_template, Blueprint, json, make_response, g

from GSP_WEB import login_required, db_session
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.StandardLog import StandardLog

blueprint_page = Blueprint('bp_report_page', __name__, url_prefix='/report')

@blueprint_page.route('', methods=['GET'])
@login_required
def getView():
    return render_template('report/list.html')

