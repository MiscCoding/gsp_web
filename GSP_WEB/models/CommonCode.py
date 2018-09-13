from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class CommonCode(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'ca100'
    idx = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    GroupCode = db.Column(db.String(255))
    Code = db.Column(db.String(255))
    Name = db.Column(db.String(255))
    EName = db.Column(db.String(255))
    UseYn = db.Column(db.String(2))
    SortOrder = db.Column(db.Integer )
    EXT1 = db.Column(db.String(2048))
    EXT2 = db.Column(db.String(2048))
    EXT3 = db.Column(db.String(2048))
    EXT4 = db.Column(db.String(2048))
    EXT5 = db.Column(db.String(2048))
    MoDatetime = db.Column(db.DateTime)

    # relation
    #rules_CNC = db.relationship("Rules_CNC", uselist=False, back_populates='commonCode')

    def __init__(self, code ):
        self.Code = code

    def __repr__(self):
        return '<CommonCode %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)

        return d