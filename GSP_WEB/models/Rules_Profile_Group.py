import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer

class Rules_Profile_Group(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Rules_Profile_Group'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500) )
    time_gubun = db.Column(db.String(100))
    time_value = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    del_yn = db.Column(db.String(1), default='N')

    def __init__(self ):
        return

    def __repr__(self):
        return '<Rules_Profile_Group %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d")
        return d
