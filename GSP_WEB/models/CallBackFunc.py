from GSP_WEB.models.Account import Account
from GSP_WEB import db_session

class accountRestore(object):

    def __init__(self, id, role_id):
        self.id = id
        self.role_id = role_id

    def restoreAccount(self):
        ret_count = Account.query.filter_by(id=self.id).first()
        ret_count.login_fail_cnt = 0
        ret_count.role_id = "001"
        print ret_count.login_fail_cnt
        print ret_count.role_id
        print "executed!"
        try:
            db_session.commit()
        except Exception as e:
            db_session.rollback()

