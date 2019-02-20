import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode


class malicious_info(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'malicious_info'
    # region parameter input
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    url = db.Column(db.String(3000), nullable=False)
    ip = db.Column(db.String(15))
    country_code= db.Column(db.String(10))
    file_name = db.Column(db.String(1000), nullable=False)
    md5 = db.Column(db.String(100))
    detect_info = db.Column(db.String(100))
    collect_point = db.Column(db.String(100))
    comment = db.Column(db.String(100))
    stix = db.Column(db.Text())
    file_path = db.Column(db.String(1000))
    # description = db.Column(db.String(2000))
    #del_yn = db.Column(db.String(1), default='N')


    def __init__(self ):
        return

    def __repr__(self):
        return '<malicious_info %r>' % (self.id)

    def serialize(self):
        d = Serializer.serialize(self)
        # d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d") if self.cre_dt is not None else ''
        return d