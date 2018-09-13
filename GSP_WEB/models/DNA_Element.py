#-*- coding: utf-8 -*-
import datetime

from flask import json
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer

class DNA_Element(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'DNA_Element'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dna_name = db.Column(db.String(500), nullable=False)
    operate_function = db.Column(db.String(10000), nullable=False)
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    mod_dt = db.Column(db.DateTime)
    use_yn = db.Column(db.String(1), default='Y')
    del_yn = db.Column(db.String(1), default='N')
    sector_list = []

    def __init__(self, id):
        self.id = id

    def __init__(self):
        return

    def __repr__(self):
        return '<id %r>' % self.id

    def serialize(self):
        self.getSectorList()
        d = Serializer.serialize(self)
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d %H:%M:%S")
        d['mod_dt'] = self.mod_dt.strftime("%Y-%m-%d %H:%M:%S") if self.mod_dt is not None else self.cre_dt.strftime("%Y-%m-%d %H:%M:%S")
        d['sector_list'] = self.sector_list
        return d

    def getSectorList(self):
        op = json.loads(self.operate_function)
        self.sector_list = []
        for _sec in op['dna_name_list']:
            self.sector_list.append({"name": _sec['dna_name'],
                                     "desc": _sec['desc'],
                                     "comment" : _sec['comment']
                                     })



