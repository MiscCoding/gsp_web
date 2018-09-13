#-*- coding: utf-8 -*-
import datetime

from flask import json
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import backref

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.DNA_Element import DNA_Element


class DNA_Schedule(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'DNA_Schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dna_id = db.Column(db.Integer, db.ForeignKey(DNA_Element.id), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    filter_ip = db.Column(db.String(500), nullable = True)
    filter_data_type = db.Column(db.String(500), nullable = True)
    cycle = db.Column(db.String(500), nullable = True)
    start_time = db.Column(db.DateTime, default=datetime.datetime.now())
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    cre_id = db.Column(db.String(500), nullable = True)
    restart_request = db.Column(db.Integer, default=0)
    proceed_state = db.Column(db.String(500), nullable = True, default='대기중')
    del_yn = db.Column(db.String(1), default='N')

    dna = db.relationship("DNA_Element")

    def __init__(self, id):
        self.id = id

    def __init__(self):
        return

    def __repr__(self):
        return '<id %r>' % self.id

    def serialize(self):
        d = Serializer.serialize(self)
        del d['dna']
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d %H:%M:%S")
        d['start_time'] = self.start_time.strftime("%Y-%m-%d %H:%M:%S")
        return d
