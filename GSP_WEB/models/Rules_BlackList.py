import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode


class Rules_BlackList(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Rules_BlackList'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mal_file_name = db.Column(db.String(2000))
    md5 = db.Column(db.String(1000), nullable=False)
    size = db.Column(db.BigInteger)
    description = db.Column(db.String(2000))
    analysis_device = db.Column(db.String(200))
    analysis_result = db.Column(db.String(200))
    detection_source = db.Column(db.String(200))
    source = db.Column(db.BigInteger, db.ForeignKey(CommonCode.idx))
    uri = db.Column(db.String(2000))
    rule_name = db.Column(db.String(255))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
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
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d %H:%M:%S") #New requirement hour, min, second format added
        return d