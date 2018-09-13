import datetime

from GSP_WEB import db
from GSP_WEB.common.encoder.alchemyEncoder import Serializer
from GSP_WEB.models.CommonCode import CommonCode
from GSP_WEB.models.Rules_Profile_Group import Rules_Profile_Group


class Rules_Profile(db.Model, Serializer):
    __table_args__ = {"schema": "GSP_WEB"}
    __tablename__ = 'Rules_Profile'
    # region parameter input
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500) )
    description = db.Column(db.String(2000))
    pattern_ui = db.Column(db.String(2000))
    pattern_query = db.Column(db.String(2000))
    pattern_operation = db.Column(db.String(2000))
    cre_dt = db.Column(db.DateTime, default=datetime.datetime.now())
    del_yn = db.Column(db.String(1), default='N')
    group_code = db.Column(db.Integer )

    def __init__(self ):
        return

    def __repr__(self):
        return '<Rules_Profile %r>' % (self.seq)

    def serialize(self):
        d = Serializer.serialize(self)
        d['cre_dt'] = self.cre_dt.strftime("%Y-%m-%d")

        if self.group_code is not None:
            group = Rules_Profile_Group.query.filter_by(seq = self.group_code).first()
            d['group_name'] =group.name
        else:
            d['group_name'] = ''

        #del d['pattern_ui']
        return d

    @property
    def search_tag_list(self):
        if (self.search_tag is not None):
            return self.search_tag.split(',')
        else:
            return ''
