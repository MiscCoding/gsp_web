import datetime
from flask import request, Response, render_template, Blueprint, json, make_response, g

from GSP_WEB import login_required, db_session
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.StandardLog import StandardLog

blueprint_page = Blueprint('bp_standard_log_page', __name__, url_prefix='/standard-log')

@blueprint_page.route('/', methods=['GET'])
@login_required
def standardLog():
    logUtil.addLog(request.remote_addr, 1, 'index')
    strdate = datetime.datetime.now().strftime("%Y-%m-%d")
    return render_template('standard_log/standard_log.html', now=strdate)


@blueprint_page.route('/getlist', methods=['POST'])
def getStandardLogList():
    logList = None
    per_page = int(request.form['perpage'])
    cur_page = int(request.form['curpage'])

    logList = db_session.query(StandardLog)

    _codes = None
    _logs = db_session.query(StandardLog)

    logList = _logs.order_by(StandardLog.seq.desc()).paginate(cur_page, per_page, error_out=False)

    result = dict()
    result["recordsTotal"] = str(logList.total)
    result["recordsFiltered"] = str(logList.total)
    result["data"] = StandardLog.serialize_list(logList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')