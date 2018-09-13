from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class CycleConfig(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'CycleConfig'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Section = db.Column(db.String(255))
    Type = db.Column(db.String(255))
    Value = db.Column(db.String(255))

