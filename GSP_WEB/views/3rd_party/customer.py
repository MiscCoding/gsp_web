#-*- coding: utf-8 -*-
import datetime

from flask import request, Response, render_template, Blueprint, json, make_response, g, session

from GSP_WEB import login_required, db_session, app
from GSP_WEB.common.util.invalidUsage import InvalidUsage
from GSP_WEB.common.util.logUtil import logUtil
from GSP_WEB.common.util.textUtil import RepresentsInt
from GSP_WEB.models.IP_WhiteList import IP_WhiteList
from GSP_WEB.models.Account import Account

blueprint_page = Blueprint('bp_customer_page', __name__, url_prefix='/3rdparty')

@blueprint_page.route('/customer', methods=['GET'])
@login_required
def customer():
    return render_template('3rdparty/customer.html')

@blueprint_page.route('/customer/<string:id>', methods=['POST'])
def addCustomer(id):

    return 'true'

@blueprint_page.route('/customer/<string:id>', methods=['DELETE'])
def deleteCustomer(id):
    return 'true'