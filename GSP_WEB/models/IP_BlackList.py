#-*- coding: utf-8 -*-
import datetime
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class IP_BlackList(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'IP_BlackList'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20))
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

