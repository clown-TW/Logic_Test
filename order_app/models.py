import datetime


from axf_api.extension import db
from common.constants import ORDER_STATUS_ORDERED
from common.models import BaseModel
from goods_app.models import Goods


class Order(BaseModel):

    o_user_id = db.Column(db.Integer, nullable=False)

    o_price = db.Column(db.Float, default=1)

    o_status = db.Column(db.Integer, default=ORDER_STATUS_ORDERED)
    # 通常会对应很多时间， 下单时间，付款时间，收货时间...
    o_order_time = db.Column(db.DateTime, default=datetime.datetime.now())
    @property
    def o_goods(self):
        return OrderGoods.query.filter_by(o_order_id=self.id).all()

class OrderGoods(BaseModel):

    o_order_id = db.Column(db.Integer, nullable=False)

    o_goods_num = db.Column(db.Integer, default=1)

    o_goods_id = db.Column(db.Integer, nullable=False)

    @property
    def o_goods(self):
        return Goods.query.filter_by(id=self.o_goods_id).first()
    # 将商品信息 作为一个字段 存储一份
    # o_goods = db.Column(db.Text)
