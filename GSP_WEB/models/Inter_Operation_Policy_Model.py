import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode
from sqlalchemy.sql import func


class Integrated_Inter_Operation_Policy(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Inter_Operation_Policy'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Type = db.Column(db.String(255), nullable=False)
    IPS_Policy = db.Column(db.String(255), unique=True, nullable=False)
    IPS_Policy_No = db.Column(db.String(255), nullable=False)
    Mal_IP = db.Column(db.String(500), nullable=False)
    Target_IP = db.Column(db.String(500), nullable=False)
    Mal_IP_Type = db.Column(db.String(255), nullable=False)
    Regular_Exp_Name = db.Column(db.String(255), nullable=False)
    Security_Log_Use = db.Column(db.Boolean, nullable=False)
    TI_Log_Use = db.Column(db.Boolean, nullable=False)
    # IP_Address = db.Column(db.String(15), nullable=True)
    # mask = db.Column(db.SmallInteger, nullable=True)
    # Description = db.Column(db.String(1000))
    # Password = db.Column(db.String(100))
    # description = db.Column(db.String(2000))
    # type = db.Column(db.String(2000))
    # cre_dt = db.Column(db.DateTime, server_default=func.now())
    # mod_dt = db.Column(db.DateTime)
    # del_yn = db.Column(db.String(1), default='N')

    def __init__(self ):
        return

    def __repr__(self):
        return '<Inter_Operation_Policy %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        # d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d") if self.cre_dt is not None else ''
        # d['mod_dt'] = self.mod_dt.strftime("%Y-%m-%d") if self.mod_dt is not None else ''
        return d