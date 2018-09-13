#-*- coding: utf-8 -*-
from functools import wraps

from flask import url_for, request, session
from werkzeug.utils import redirect


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #session값 추가
        # session['id'] = 'ktwo2'
        # return f(*args, **kwargs)
        if session.get('id') is None:
            return redirect(url_for('bp_root.getLogin'))

        if session.get('role_id') is None:
            return redirect(url_for('bp_root.getLogin'))
        elif session.get('role_id') != "001" and request.method != "GET":
            return redirect(url_for('bp_root.getLogin'))
        elif session.get('role_id') == "004":
            return redirect(url_for('bp_root.getLogin'))
        elif session.get('role_id') == "003" and request.url.find('index') < 0 :
            return redirect(url_for('bp_index_page.getIndex'))
        return f(*args, **kwargs)

    return decorated_function

def login_required_ajax(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get('id') is None:
            return redirect(url_for('bp_root.getLogin'))

        if session.get('role_id') is None:
            return redirect(url_for('bp_root.getLogin'))
        elif session.get('role_id') != "001" and request.method != "GET":
            return redirect(url_for('bp_root.getLogin'))
        elif session.get('role_id') == "004":
            return redirect(url_for('bp_root.getLogin'))
        elif session.get('role_id') == "003" and request.url.find('index') < 0 :
            return redirect(url_for('bp_index_page.getIndex'))
        return f(*args, **kwargs)

    return decorated_function