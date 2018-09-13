import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode


class Rules_Snort(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Rules_Snort'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(200))
    pattern = db.Column(db.String(2000), nullable=False)
    level = db.Column(db.SmallInteger)
    description = db.Column(db.String(2000))
    source = db.Column(db.BigInteger, db.ForeignKey(CommonCode.idx))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    mod_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    del_yn = db.Column(db.String(1), default='N')

    source_commonCode = db.relationship("CommonCode", order_by="CommonCode.SortOrder", foreign_keys=[source])

    def __init__(self ):
        return

    def __repr__(self):
        return '<Rules_BlackList %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['source_commonCode']
        d['source_name'] = self.source_commonCode.EXT1
        d['source_code'] = self.source_commonCode.Code
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d")
        try:
            d['mod_dt'] = self.mod_dt.strftime("%Y-%m-%d")
        except:
            d['mod_dt'] = ''
        return d