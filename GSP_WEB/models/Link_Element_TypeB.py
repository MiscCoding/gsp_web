#-*- coding: utf-8 -*-
import datetime

from flask import json
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class Link_Element_TypeB(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Link_Element_TypeB'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dst_columns_name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(2000))
    operate_function = db.Column(db.String(2000), nullable=False)
    analysis_cycle = db.Column(db.String(100), nullable=False)
    timespan = db.Column(db.String(100), nullable=False)
    dst_data_type = db.Column(db.String(2000), nullable=True, default="list")
    dst_data_size = db.Column(db.Integer, nullable=True)
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
        return d

    def setOperateFunction(self, cols, op, time_range):

        result = {
            "org_elements" : [

            ]
        }

        for row in cols:
            rowDict = {
                "org_type" : row["type"],
                "org_id" : row["id"],
                "operate" : row["op"]
            }
            result["org_elements"].append(rowDict)

        if cols.__len__() > 1:
            result["operate_between"] = op

        if time_range is not None:
            result["time_range"] = time_range

        self.operate_function = json.dumps(result)