from flask import request
from flask_restful import Resource, fields, marshal
from rest_framework import status
from sqlalchemy import text

from axf_api.extension import cache
from cart_app.models import Cart
from common.constants import TYPE_DEFAULT, CATE_DEFAULT, ORDER_RULE_DEFAULT, ORDER_RULE_PRICE_UP, ORDER_RULE_PRICE_DOWN, \
    ORDER_RULE_SALE_UP, ORDER_RULE_SALE_DOWN
from goods_app.models import GoodsType, GoodsTypeCate, Goods

goods_types_cate_fields = {
    "id": fields.Integer,
    "type_name": fields.String,
    "type_order": fields.Integer,
}

goodstype_fields = {
    "id": fields.Integer,
    "type_name": fields.String,
    "type_order": fields.Integer,
    "goods_types_cates":fields.Nested(goods_types_cate_fields)
}


class GoodsTypeResource(Resource):

    def get(self):

        goodsType = GoodsType.query.all()

        data = {
            "msg": "create ok",
            "status":status.HTTP_200_OK,
            "data": marshal(goodsType,goodstype_fields)
        }
        return data

    def post(self):

        type_name = request.form.get("type_name")

        type_order = request.form.get("type_order")

        goodsType = GoodsType(type_name=type_name,type_order=type_order)

        if goodsType.save():

            data = {
                "msg":"create ok",
                "status":status.HTTP_201_CREATED
            }
            return data

        data = {
            "msg":"create fail",
            "status":status.HTTP_400_BAD_REQUEST
        }
        return data

class GoodsTypeCateResource(Resource):

    def post(self):
        type_name = request.form.get("type_name")

        type_order = request.form.get("type_order")

        goods_type_id = request.form.get("goods_type_id")

        goodsTypeCate = GoodsTypeCate(type_name=type_name,type_order=type_order,goods_type_id=goods_type_id)

        if goodsTypeCate.save():
            data = {
                "msg": "create ok",
                "status": status.HTTP_201_CREATED
            }
            return data

        data = {
            "msg": "create fail",
            "status": status.HTTP_400_BAD_REQUEST
        }
        return data


goods_fields = {
    "id": fields.Integer,
    "goods_image": fields.String,
    "goods_name": fields.String,
    "goods_price": fields.Float,
    "goods_market_price": fields.Float,
    "goods_unit": fields.String,
    "goods_is_rec": fields.Boolean,
    "goods_bar_code": fields.String,
    "goods_sold_num": fields.Integer,
    "goods_num":fields.Integer,
}


class GoodsResource(Resource):

    def get(self):
        # ??????????????????
        type_id = request.args.get("type_id", TYPE_DEFAULT, type=int)
        # ??????????????????
        cate_id = request.args.get("cate_id", CATE_DEFAULT, type=int)
        # ????????????
        order_rule = request.args.get("order_rule", ORDER_RULE_DEFAULT, type=int)
        # ????????????????????????
        goods_list = Goods.query.filter_by(goods_type_id=type_id)
        # ????????????????????????
        if cate_id != CATE_DEFAULT:
            goods_list = goods_list.filter_by(goods_type_cate_id=cate_id)
        # ????????????????????????
        if order_rule == ORDER_RULE_DEFAULT:
           pass
        elif order_rule == ORDER_RULE_PRICE_UP:
            goods_list = goods_list.order_by("goods_price")
        elif order_rule == ORDER_RULE_PRICE_DOWN:
            goods_list = goods_list.order_by(text("-goods_price"))
        elif order_rule == ORDER_RULE_SALE_UP:
            goods_list = goods_list.order_by(text("goods_sold_num"))
        elif order_rule == ORDER_RULE_SALE_DOWN:
            goods_list = goods_list.order_by(text("-goods_sold_num"))

        #     ???????????????????????????????????????????????????????????????????????????????????????
        token = request.args.get("token")
        print(token)
        # ????????????
        goods_list = goods_list.all()
        goods_list_new = []

        if token:
            # ????????????
            user = cache.get(token)
            if user:
                user_id = user.id
                # ???????????????????????????
                carts = Cart.query.filter_by(c_user_id=user_id).all()
                # ??????????????????
                for goods in goods_list:
                    # ?????????????????????
                    for cart in carts:
                        # ????????????????????????????????????????????????
                        if goods.id == cart.c_goods_id:
                            # ????????????????????????
                            goods.goods_num = cart.c_goods_num
                    # ??????????????????????????????????????????
                    goods_list_new.append(goods)
        else:
            goods_list_new = goods_list

        data = {
            "msg": "ok",
            "status": 200,
            "data": marshal(goods_list_new, goods_fields)
        }

        return data

