import datetime
from flask import session

from GSP_WEB import db_session
from GSP_WEB.models.StandardLog import StandardLog


class logUtil():

    @staticmethod
    def addLog(src_ip, important, description):
        log = StandardLog()
        log.id = session['id']
        log.ip = src_ip
        log.importance = important
        log.description = description
        log.cre_dt = datetime.datetime.now()
        db_session.add(log)
        db_session.commit()
        return

