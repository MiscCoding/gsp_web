#-*- coding: utf-8 -*-
import datetime
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class Link_Element_TypeA(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Link_Element_TypeA'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    src_type = db.Column(db.String(2000), nullable=False)
    src_columns_name = db.Column(db.String(500), nullable=False)
    dst_columns_name = db.Column(db.String(500), nullable=False)
    operate_function = db.Column(db.String(2000), nullable=True)
    dst_data_type = db.Column(db.String(2000), nullable=True, default="single")
    dst_data_size = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(2000))
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

