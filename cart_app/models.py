from axf_api.extension import db
from common.models import BaseModel
from goods_app.models import Goods


class Cart(BaseModel):

    c_goods_id = db.Column(db.Integer, nullable=False)
    c_user_id= db.Column(db.Integer, nullable=False)
    c_goods_num = db.Column(db.Integer, default=1)
    is_select = db.Column(db.Boolean, default=True)

    @property
    def c_goods(self):
        return Goods.query.filter_by(id=self.c_goods_id).first()
