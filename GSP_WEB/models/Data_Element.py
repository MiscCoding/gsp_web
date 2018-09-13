#-*- coding: utf-8 -*-
import datetime

from flask import json
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer

class Data_Element(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Data_Element'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    column_name = db.Column(db.String(100), nullable=False, unique=True)
    data_source = db.Column(db.String(100), nullable=False)
    format = db.Column(db.String(100), nullable=False)
    form = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=True)
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
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d %H:%M:%S") if self.cre_dt is not None else ''
        d['mod_dt'] = self.mod_dt.strftime("%Y-%m-%d %H:%M:%S") if self.mod_dt is not None else ''
        return d

    def getLinkDataType(self):
        if self.format == "number" and self.form == "time_seriese":
            return ["list", None]
        elif self.format == "string" and self.form == "single":
            return ["single", None]
        elif self.format == "string" and self.form == "list":
            return ["map", None]
        elif self.format == "number" and self.form == "array":
            return ["single_list", self.size]
        elif self.format == "number" and self.form == "single":
            return ["single", self.size]
