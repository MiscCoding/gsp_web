#-*- coding: utf-8 -*-
import datetime
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class GlobalSetting(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'GlobalSetting'
    key = db.Column(db.String(20), primary_key=True)
    value = db.Column(db.String(20))
    name = db.Column(db.String(200))
    description = db.Column(db.String(2000))


    def __init__(self, ip):
        self.ip = ip

    def __init__(self):
        return

    def __repr__(self):
        return '<ip %r>' % self.ip

    def serialize(self):
        d = Serializer.serialize(self)
        return d

