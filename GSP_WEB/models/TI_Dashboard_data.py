from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer


class TI_Dashboard_data(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'TI_Dashboard_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    div_id = db.Column(db.String(45))
    title = db.Column(db.String(200))
    url = db.Column(db.String(2000))
    # EName = db.Column(db.String(255))
    # UseYn = db.Column(db.String(2))
    # SortOrder = db.Column(db.Integer )
    # EXT1 = db.Column(db.String(2048))
    # EXT2 = db.Column(db.String(2048))
    # EXT3 = db.Column(db.String(2048))
    # EXT4 = db.Column(db.String(2048))
    # EXT5 = db.Column(db.String(2048))
    # MoDatetime = db.Column(db.DateTime)

    # relation
    #rules_CNC = db.relationship("Rules_CNC", uselist=False, back_populates='commonCode')

    def __init__(self, code):
        self.Code = code

    def __repr__(self):
        return '<TI_Dashboard_data %r>' % (self.id)

    def serialize(self):
        d = Serializer.serialize(self)

        return d