#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session

from GSP_WEB import login_required, db_session, app, EncryptEncoder
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.common.util.textUtil import RepresentsInt
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.GlobalSetting import GlobalSetting
from GSP_WEB.models.IP_BlackList import IP_BlackList
from GSP_WEB.models.IP_WhiteList import IP_WhiteList
from GSP_WEB.models.Account import Account

blueprint_page = Blueprint('bp_account_page', __name__, url_prefix='/system')

@blueprint_page.route('/account', methods=['GET'])
@login_required
def accountList():
    logUtil.addLog(request.remote_addr,1,'system>account')
    ip_allow = db_session.query(GlobalSetting).filter_by(key="ALLOW_IP").first()
    ip_allow_value = ip_allow.value

    role_list = CommonCode.query.filter(CommonCode.GroupCode=="role_type").all()
    return render_template('system/account.html',ip_allow = ip_allow_value, role_list = role_list)

@blueprint_page.route('/account/accountlist', methods=['GET'])
def getAccountList():
    accountList = None
    per_page = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    start_idx = int(request.args.get('start'))
    search_param = request.args.get('search[value]').strip()

    _codes = None
    if session.get("role_id") != "001":
        _codes = Account.query.filter(Account.id == session.get('id') )
    elif search_param is not u"":
        _codes = Account.query.filter(Account.id.like('%'+search_param+'%'))
    else:
        _codes = db_session.query(Account)

    curpage = int(start_idx / per_page) + 1
    accountList = _codes.order_by(Account.cre_dt.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(accountList.total)
    result["recordsFiltered"] = str(accountList.total)
    result["data"] = Account.serialize_list(accountList.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')


@blueprint_page.route('/account/<string:id>', methods=['POST'])
#@login_required
def addAccount(id):
    dupCheckResult = db_session.query(Account).filter_by(id=id).first()
    if dupCheckResult is not None:
        raise InvalidUsage('중복된 아이디가 있습니다.', status_code=500)
    _account = Account()
    _account.id =id
    _account.password = pw = EncryptEncoder.sha256Encrypt(request.form["password"])
    _account.cre_dt = datetime.datetime.now()
    _account.email = request.form["email"]
    _account.mobile = request.form["mobile"]
    _account.role_id = request.form["role"]
    _account.culture = request.form["culture"]
    _account.comment = request.form["comment"]
    db_session.add(_account)
    db_session.commit()
    return ""

@blueprint_page.route('/account/<string:id>', methods=['PUT'])
@login_required
def editAccount(id):
    _account = db_session.query(Account).filter_by(id=id).first()
    if request.form['password'] != "":
        _account.password = pw = EncryptEncoder.sha256Encrypt(request.form["password"])
    _account.cre_dt = datetime.datetime.now()
    _account.email = request.form["email"]
    _account.mobile = request.form["mobile"]
    _account.role_id = request.form["role"]
    _account.culture = request.form["culture"]
    _account.comment = request.form["comment"]
    if request.form["role"] == "001":
        _account.login_fail_cnt = 0

    db_session.commit()
    return ""

@blueprint_page.route('/account/<string:usrid>', methods=['DELETE'])
@login_required
def deleteAccount(usrid):
    account = db_session.query(Account).filter_by(id=usrid ).first()
    if account is not None :
        db_session.delete(account)
        db_session.commit()
    return ""

@blueprint_page.route('/ip-white', methods=['POST'])
@login_required
#@login_required
def addIP_White():
    ip = request.form["ip"]
    desc = request.form["desc"]
    dupCheckResult = db_session.query(IP_WhiteList).filter_by(ip=ip).first()
    if dupCheckResult is not None:
        raise InvalidUsage('중복된 IP가 존재 합니다.', status_code=501)
    whiteip = IP_WhiteList()
    whiteip.ip = ip
    whiteip.description = desc
    db_session.add(whiteip)
    db_session.commit()
    return ""

@blueprint_page.route('/ip-white/<string:ip>', methods=['PUT'])
@login_required
def editIP_White(ip):
    whitelist = db_session.query(IP_WhiteList).filter_by(ip=ip).first()
    whitelist.ip = request.form["ip"]
    whitelist.description = request.form["desc"]
    db_session.commit()
    return ""

@blueprint_page.route('/ip-white/<string:ip>', methods=['DELETE'])
@login_required
def deleteIP_White(ip):
    whitelist = db_session.query(IP_WhiteList).filter_by(ip=ip ).first()
    if whitelist is not None :
        db_session.delete(whitelist)
        db_session.commit()
    return ""

@blueprint_page.route('/ip-white/whitelist', methods=['GET'])
def getWhiteList():
    blacklist = None
    per_page = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    start_idx = int(request.args.get('start'))
    search_param = request.args.get('search[value]').strip()

    _codes = None
    if search_param is not u"":
        _codes = IP_BlackList.query.filter(IP_WhiteList.id.like('%'+search_param+'%'))
    else:
        _codes = db_session.query(IP_WhiteList)

    curpage = int(start_idx / per_page) + 1
    whitelist = _codes.order_by(IP_WhiteList.id.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(whitelist.total)
    result["recordsFiltered"] = str(whitelist.total)
    result["data"] = IP_WhiteList.serialize_list(whitelist.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/ip-black', methods=['POST'])
@login_required
def addIP_Black():
    ip = request.form["ip"]
    desc = request.form["desc"]
    dupCheckResult = db_session.query(IP_BlackList).filter_by(ip=ip).first()
    if dupCheckResult is not None:
        raise InvalidUsage('중복된 IP가 존재 합니다.', status_code=501)
    blackip = IP_BlackList()
    blackip.ip = ip
    blackip.description = desc
    db_session.add(blackip)
    db_session.commit()
    return ""

@blueprint_page.route('/ip-black/<string:ip>', methods=['PUT'])
@login_required
def editIP_Black(ip):
    blacklist = db_session.query(IP_BlackList).filter_by(ip=ip).first()
    blacklist.ip = request.form["ip"]
    blacklist.description = request.form["desc"]
    db_session.commit()
    return ""

@blueprint_page.route('/ip-black/<string:ip>', methods=['DELETE'])
@login_required
def deleteIP_Black(ip):
    blacklist = db_session.query(IP_BlackList).filter_by(ip=ip ).first()
    if blacklist is not None :
        db_session.delete(blacklist)
        db_session.commit()
    return ""

@blueprint_page.route('/ip-black/blacklist', methods=['GET'])
def getBlackList():
    blacklist = None
    per_page = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    start_idx = int(request.args.get('start'))
    search_param = request.args.get('search[value]').strip()

    _codes = None
    if search_param is not u"":
        _codes = IP_BlackList.query.filter(IP_BlackList.id.like('%'+search_param+'%'))
    else:
        _codes = db_session.query(IP_BlackList)

    curpage = int(start_idx / per_page) + 1
    blacklist = _codes.order_by(IP_BlackList.id.desc()).paginate(curpage, per_page, error_out=False)


    result = dict()
    result["draw"] = str(draw)
    result["recordsTotal"] = str(blacklist.total)
    result["recordsFiltered"] = str(blacklist.total)
    result["data"] = IP_WhiteList.serialize_list(blacklist.items)
    str_json = json.dumps(result)
    return Response(str_json, mimetype='application/json')

@blueprint_page.route('/ip-allow', methods=['POST'])
@login_required
def ChangeAllowIpSetting():
    key = "ALLOW_IP"
    value = request.form.get("value")
    desc = request.form.get("description")
    ip_allow = db_session.query(GlobalSetting).filter_by(key=key).first()
    if ip_allow is not None:
        ip_allow.value = value
        ip_allow.description = desc
        db_session.commit()
    else:
        newSetting = GlobalSetting()
        newSetting.key = key
        newSetting.value = value
        newSetting.description = desc
        db_session.add(newSetting)
        db_session.commit()
    return ""