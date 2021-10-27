from axf_api.extension import db
from common.models import BaseModel


class GoodsType(BaseModel):
    type_name = db.Column(db.String(16),nullable=False,unique=True)
    type_order = db.Column(db.Integer,default=50)

    @property
    def goods_types_cates(self):
        return [{id:0,"type_name":"全部分类","type_order":50}] + GoodsTypeCate.query.filter_by(goods_type_id = self.id).all()

class GoodsTypeCate(BaseModel):
    type_name = db.Column(db.String(16),nullable=False,unique=True)
    type_order = db.Column(db.Integer,default=50)
    goods_type_id = db.Column(db.Integer,nullable=False)

class Goods(BaseModel):
    # 一级数据类别的唯一标识
    goods_type_id = db.Column(db.Integer,nullable=False)
    # 二级数据类别唯一标识
    goods_type_cate_id = db.Column(db.Integer,nullable=False)
    # 商品详细信息
    goods_image = db.Column(db.String(256))
    goods_name = db.Column(db.String(128))
    goods_price = db.Column(db.Float, default=1)
    goods_market_price = db.Column(db.Float, default=1)
    goods_unit = db.Column(db.String(64))
    goods_is_rec = db.Column(db.Boolean, default=False)
    goods_bar_code = db.Column(db.String(64), nullable=False, unique=True)
    goods_sold_num = db.Column(db.Integer, default=0)
