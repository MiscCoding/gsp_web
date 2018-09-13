import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode


class Rules_WhiteList(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Rules_WhiteList'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    md5 = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(2000))
    source = db.Column(db.BigInteger, db.ForeignKey(CommonCode.idx))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    del_yn = db.Column(db.String(1), default='N')

    source_commonCode = db.relationship("CommonCode", order_by="CommonCode.SortOrder", foreign_keys=[source])

    def __init__(self ):
        return

    def __repr__(self):
        return '<Rules_WhiteList %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['source_commonCode']
        d['source_name'] = self.source_commonCode.EXT1
        d['source_code'] = self.source_commonCode.Code
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d")
        return d