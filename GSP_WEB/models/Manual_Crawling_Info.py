import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode
from sqlalchemy.sql import func


class Manual_Crawling_Info(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Manual_Crawling_Info'
    # region parameter input
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    url = db.Column(db.String(5000), nullable=False)
    depth = db.Column(db.SmallInteger, nullable=True, default=1)
    comment = db.Column(db.String(100), nullable=True)
    register_from = db.Column(db.String(100), nullable=True)
    register_date = db.Column(db.DateTime, server_default=func.now())
    del_yn = db.Column(db.String(1), nullable=False, default='n')
    result_yn = db.Column(db.String(1), nullable=False, default="n")



    def __init__(self ):
        return

    def __repr__(self):
        return '<Manual_Crawling_Info %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        # d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d") if self.cre_dt is not None else ''
        # d['mod_dt'] = self.mod_dt.strftime("%Y-%m-%d") if self.mod_dt is not None else ''
        return d