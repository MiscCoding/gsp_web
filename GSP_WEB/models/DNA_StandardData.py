#-*- coding: utf-8 -*-
import datetime

from flask import json
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class DNA_StandardData(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'DNA_StandardData'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2000), nullable=False)
    list_data = db.Column(db.String(5000), nullable=False)
    list_size = db.Column(db.Integer, nullable=False, default=0)
    target_link_type = db.Column(db.String(10))
    target_link_seq = db.Column(db.Integer)
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    mod_dt = db.Column(db.DateTime)
    use_yn = db.Column(db.String(1), default='Y')
    del_yn = db.Column(db.String(1), default='N')


    def __init__(self, id):
        self.id = id

    def __init__(self):
        return

    def __repr__(self):
        return '<id %r>' % self.id

    def serialize(self):
        d = Serializer.serialize(self)
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d %H:%M:%S")
        d['mod_dt'] = self.mod_dt.strftime("%Y-%m-%d %H:%M:%S") if self.mod_dt is not None else ''
        return d
