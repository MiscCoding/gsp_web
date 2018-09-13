#-*- coding: utf-8 -*-
import datetime
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class Account(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Account'
    id = db.Column(db.String(100), primary_key=True, unique=True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(500))
    mobile = db.Column(db.String(500))
    role_id = db.Column(db.String(255)) #Common Code
    culture = db.Column(db.String(500))
    comment = db.Column(db.String(2000))
    last_pass_change_date = db.Column(db.DateTime)
    last__login_date = db.Column(db.DateTime)
    login_fail_date = db.Column(db.DateTime)
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    cre_id = db.Column(db.String(500))
    login_fail_cnt = db.Column(db.Integer, default=0)
    blockCode = db.Column(db.String(255)) #Common Code
    login_fail_dt = db.Column(db.DateTime)


    def __init__(self, id):
        self.id = id

    def __init__(self):
        return

    def __repr__(self):
        return '<id %r>' % self.id

    def serialize(self):
        d = Serializer.serialize(self)
        return d


