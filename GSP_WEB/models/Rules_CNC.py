import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode


class Rules_CNC(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Rules_CNC'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pattern_uri = db.Column(db.String(2000))
    category = db.Column(db.String(200))
    rule_type = db.Column(db.BigInteger, db.ForeignKey(CommonCode.idx))
    analysis_device = db.Column(db.String(2000))
    analysis_result = db.Column(db.String(200))
    detection_source = db.Column(db.String(200))
    description = db.Column(db.String(2000))
    source = db.Column(db.BigInteger, db.ForeignKey(CommonCode.idx))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    del_yn = db.Column(db.String(1), default='N')
    country_code = db.Column(db.String(200))
    mod_dt = db.Column(db.DateTime, default=datetime.datetime.now())


    rule_type_commonCode = db.relationship("CommonCode",order_by="CommonCode.SortOrder",foreign_keys=[rule_type])
    source_commonCode = db.relationship("CommonCode", order_by="CommonCode.SortOrder", foreign_keys=[source])

    def __init__(self ):
        return

    def __repr__(self):
        return '<Rules_CNC %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['rule_type_commonCode']
        d['type_name'] = self.rule_type_commonCode.EXT1 if self.rule_type_commonCode is not None else ""
        del d['source_commonCode']
        d['source_name'] = self.source_commonCode.EXT1 if self.rule_type_commonCode is not None else ""
        d['source_code'] = self.source_commonCode.Code if self.rule_type_commonCode is not None else ""
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d")
        return d

    @property
    def search_tag_list(self):
        if (self.search_tag is not None):
            return self.search_tag.split(',')
        else:
            return ''
