#-*- coding: utf-8 -*-
import datetime
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer

class LinkDnaLog(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'LinkDnaLog'
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(100))
    ip = db.Column(db.String(100))
    importance = db.Column(db.Integer)
    description = db.Column(db.String(3000))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())

    def serialize(self):
        d = Serializer.serialize(self)
        d['cre_dt'] = d['cre_dt'].strftime("%Y-%m-%d %H-%M-%S")
        return d