from flask import g, request
from flask_restful import Resource, marshal, fields

from cart_app.models import Cart
from common import msg, status
from common.constants import ORDER_STATUS_ORDERED, ORDER_STATUS_PAYED
from common.user_authentication import login_required
from order_app.models import Order, OrderGoods

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
    "goods_num": fields.Integer,
}

order_goods_fields = {
    "id": fields.Integer,
    "o_goods_num": fields.Integer,
    "o_goods": fields.Nested(goods_fields)

}

order_fields = {
    "o_user_id": fields.Integer,
    "id": fields.Integer,
    "o_price": fields.Float,

    "o_status": fields.Integer,
    # 通常会对应很多时间， 下单时间，付款时间，收货时间...
    "o_order_time": fields.DateTime,
    "o_goods": fields.Nested(order_goods_fields)
}


class OrdersResource(Resource):

    @login_required
    def get(self):

        action = request.args.get("action")

        if action == "get_order_list":
            return self.get_order_list()
        elif action == "get_order_detail":
            return self.get_order_detail()
        else:
            return self.get_order_status_count()

    def get_order_list(self):
        order_type = request.args.get("order_type", type=int)

        if order_type == ORDER_STATUS_ORDERED:
            orders = Order.query.filter_by(o_user_id=g.user.id).filter_by(o_status=ORDER_STATUS_ORDERED).all()
            data = {
                "msg": msg.MSG_OK,
                "status": status.HTTP_200_OK,
                "data": marshal(orders, order_fields)
            }
            return data

    def get_order_detail(self):

        order_id = request.args.get("order_id")

        order = Order.query.filter_by(id=order_id).first()

        if order:

            data = {
                "msg": msg.MSG_OK,
                "status": status.HTTP_200_OK,
                "data": marshal(order, order_fields)
            }
            return data

        else:
            data = {
                "msg": "order not fount",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return data

    def get_order_status_count(self):

        not_pay = Order.query.filter_by(o_user_id=g.user.id).filter_by(o_status=ORDER_STATUS_ORDERED).count()
        not_send = Order.query.filter_by(o_user_id=g.user.id).filter_by(o_status=ORDER_STATUS_PAYED).count()

        data = {
            "status": status.HTTP_200_OK,
            "msg": msg.MSG_OK,
            "data": {
                "not_pay": not_pay,
                "not_send": not_send
            }
        }

        return data

    @login_required
    def post(self):
        """
            生成一个订单
                Order中的一条数据
            生成订单商品数据
                OrderGoods中产生数据
                数据来源
                    Cart表中的数据
        """

        carts = Cart.query.filter_by(c_user_id=g.user.id).filter_by(is_select=True).all()

        if not carts:
            data = {
                "msg": "please select goods",
                "status": status.HTTP_404_NOT_FOUND
            }

            return data

        total = 0

        for cart in carts:
            total += cart.c_goods_num * cart.c_goods.goods_price
        # 创建订单
        order = Order(o_user_id=g.user.id, o_price=total)

        order.save()

        for cart in carts:
            orderGoods = OrderGoods(o_order_id=order.id, o_goods_id=cart.c_goods_id, o_goods_num=cart.c_goods_num)
            orderGoods.save()
            cart.delete()

        data = {
            "msg": msg.MSG_OK,
            "status": status.HTTP_201_CREATED,
            "data": marshal(order, order_fields)
        }

        return data
