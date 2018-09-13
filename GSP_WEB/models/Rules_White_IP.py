import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode


class Rules_White_IP(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Rules_White_IP'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(15), nullable=False)
    mask = db.Column(db.SmallInteger, nullable=False)
    description = db.Column(db.String(2000))
    type = db.Column(db.String(2000))
    url = db.Column(db.String(2000))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    del_yn = db.Column(db.String(1), default='N')


    def __init__(self ):
        return

    def __repr__(self):
        return '<Rules_White_IP %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d") if self.cre_dt is not None else ''
        return d