#-*- coding: utf-8 -*-
import datetime
from flask import render_template, Blueprint, json, request, session, redirect, url_for

from GSP_WEB import EncryptEncoder, db_session
from GSP_WEB.models.Account import Account
from GSP_WEB.models.GlobalSetting import GlobalSetting
from GSP_WEB.models.IP_BlackList import IP_BlackList
from GSP_WEB.models.IP_WhiteList import IP_WhiteList
from GSP_WEB.models.CallBackFunc import accountRestore
import threading

blueprint_page = Blueprint('bp_root', __name__)
max_nodes_size = 1000

@blueprint_page.route('/login', methods=['GET'])
def getLogin():
    session.clear()
    err_code = request.args.get('err_code')
    login_account = request.args.get('login_account')

    return render_template('login.html', err_code=err_code, login_account=login_account)

@blueprint_page.route('/login', methods=['POST'])
def postLogin():
    ip_allow = db_session.query(GlobalSetting).filter_by(key="ALLOW_IP").first()
    requestIP = request.remote_addr
    if ip_allow.value == "white":
        whiteList = db_session.query(IP_WhiteList).filter(IP_WhiteList.ip.like(requestIP)).first()
        if whiteList is None:
            return redirect(url_for('bp_root.getLogin', err_code=2, login_account=Account))
    else:
        requestIP = request.remote_addr
        blackList = db_session.query(IP_BlackList).filter(IP_BlackList.ip.like(requestIP)).first()
        if blackList is not None:
            return redirect(url_for('bp_root.getLogin', err_code=2, login_account=Account))

    id = request.form.get("id")
    pw = request.form.get("pw")
    if pw is None and pw == "":
        return redirect(url_for('login'))

    if pw is None and pw == "":
        return redirect(url_for('login'))

    pw = EncryptEncoder.sha256Encrypt(pw)
    ret_count = Account.query.filter_by(id=id).filter_by(password=pw).first()

    if ret_count is not None:
        if ret_count.role_id == '004' or ret_count.role_id == '005':
            return redirect(url_for('bp_root.getLogin', err_code=3, login_account=Account)) #차단 된 계정
        session['id'] = id
        session['role_id'] =ret_count.role_id
        return redirect(url_for('index'))
    else :
        ret_count = Account.query.filter_by(id=id).first()
        if ret_count is not None:
            if ret_count.login_fail_cnt is None:
                ret_count.login_fail_cnt = 1
            else:
                ret_count.login_fail_cnt += 1
                print ret_count.login_fail_cnt
                ret_count.login_fail_dt = datetime.datetime.now()
                if ret_count.login_fail_cnt > 4:
                    initialRole_id = ret_count.role_id
                    accountToRestore = accountRestore(id, initialRole_id)
                    ret_count.role_id = '004'
                    print "timer started"
                    threading.Timer(3600, accountToRestore.restoreAccount, ()).start()


            db_session.commit()

            return redirect(url_for('bp_root.getLogin', err_code=1, login_account=Account))
        else:
            return redirect(url_for('bp_root.getLogin', err_code=1, login_account=Account))

@blueprint_page.route('/dashboard-asis', methods=['GET'])
def getIndex_asis():
    timenow = datetime.datetime.now().strftime("%Y-%m-%d")
    return render_template('index/dashboard.html', timenow = timenow)

@blueprint_page.route('/modif-dashboard-asis', methods=['GET'])
def getIndex_asis_modif():
    timenow = datetime.datetime.now().strftime("%Y-%m-%d")
    return render_template('index/dashboardmodif.html', timenow = timenow)