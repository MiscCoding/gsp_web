import datetime
from flask import Blueprint, render_template, request

from GSP_WEB import login_required
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_Profile import Rules_Profile

blueprint_page = Blueprint('bp_analysis', __name__, url_prefix='/analysis')

@blueprint_page.route('', methods=['GET'])
@login_required
def getAnalysis():
    logUtil.addLog(request.remote_addr, 1, 'link-dna/log')
    timefrom = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    profileList = Rules_Profile.query.all()
    typeList = CommonCode.query.filter_by(GroupCode = "DATA_TYPE").all()

    return render_template('analysis/list.html', timefrom=timefrom, timeto=timeto, profileList=profileList, typeList = typeList)