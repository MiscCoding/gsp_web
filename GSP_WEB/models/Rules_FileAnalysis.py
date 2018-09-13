import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer

class Rules_FileAnalysis(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Rules_FileAnalysis'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orgfilename = db.Column(db.String(1000), nullable=False)
    realfilename = db.Column(db.String(1000), nullable=False)
    subpath = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(2000))
    cre_id = db.Column(db.String(100))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    mod_dt =db.Column(db.DateTime, default=datetime.datetime.now())
    del_yn = db.Column(db.String(1), default='N')

    def __init__(self ):
        return

    def __repr__(self):
        return '<Rules_FileAnalysis %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d")
        return d