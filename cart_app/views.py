from flask import request, g
from flask_restful import Resource, marshal, fields

from cart_app.models import Cart
from common import msg, status
from common.user_authentication import login_required

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
}


cart_fields = {
    "id": fields.Integer,
    "is_select": fields.Boolean,
    "c_goods_id": fields.Integer,
    "c_user_id": fields.Integer,
    "c_goods_num": fields.Integer,
    "c_goods": fields.Nested(goods_fields)
}


class CartsResource(Resource):

    @login_required
    def get(self):

        carts = Cart.query.filter_by(c_user_id=g.user.id).all()

        is_all_select = True

        if Cart.query.filter_by(c_user_id=g.user.id).filter_by(is_select=False).all():
            is_all_select = False

        data = {
            "msg": msg.MSG_OK,
            "status": status.HTTP_200_OK,
            "is_all_select": is_all_select,
            "total_price": self.calc_total_price(),
            "data": marshal(carts, cart_fields)
        }

        return data

    @login_required
    def post(self):

        action = request.args.get("action")

        if action == "add_cart":
            return self.do_add_cart()
        elif action == "change_select":
            return self.change_select()
        elif action == "change_all_select":
            return self.change_all_select()
        elif action == "sub_goods_num":
            return self.sub_goods_num()

    def do_add_cart(self):

        goods_id = request.form.get("goods_id")

        user = g.user

        carts = Cart.query.filter_by(c_goods_id=goods_id).filter_by(c_user_id=user.id).all()

        if carts:
            cart = carts[0]
            cart.c_goods_num = cart.c_goods_num+1
        else:
            cart = Cart(c_goods_id=goods_id, c_user_id=user.id)

        if cart.save():

            data = {
                "msg": "add success",
                "status": 201,
                "data": marshal(cart, cart_fields),
            }

            return data
        else:

            data = {
                "msg": "add fail",
                "status": status.HTTP_400_BAD_REQUEST
            }

            return data

    def change_select(self):
        cart_id = request.form.get("cart_id")

        cart = Cart.query.filter_by(id=cart_id).first()

        cart.is_select = not cart.is_select

        if cart.save():

            data = {
                "msg": msg.MSG_OK,
                "status": status.HTTP_201_CREATED,
                "total_price": self.calc_total_price()
            }

            return data
        else:
            data = {
                "msg": "change fail",
                "status": status.HTTP_400_BAD_REQUEST
            }

            return data

    def change_all_select(self):
        # 根据我们的数据进行处理
        carts = Cart.query.filter_by(c_user_id=g.user.id).filter_by(is_select=False).all()

        if carts:
            for cart in carts:
                cart.is_select = True
                cart.save()
        else:
            carts = Cart.query.filter_by(c_user_id=g.user.id).all()

            if not carts:
                data = {
                    "msg": "change fail, no data",
                    "status": status.HTTP_205_RESET_CONTENT
                }
                return data

            for cart in carts:
                cart.is_select = False
                cart.save()

        data = {
            "msg": msg.MSG_OK,
            "status": status.HTTP_200_OK,
            "total_price": self.calc_total_price()
        }

        return data

    def calc_total_price(self):

        carts = Cart.query.filter_by(c_user_id=g.user.id).filter_by(is_select=True).all()
        total = 0

        for cart in carts:
            total += cart.c_goods_num*cart.c_goods.goods_price

        return total

    def sub_goods_num(self):

        cart_id = request.form.get("cart_id")

        cart = Cart.query.filter_by(id=cart_id).first()

        data = {
            "msg": msg.MSG_OK,
        }

        if cart.c_goods_num == 1:
            cart.delete()
            data["status"] = status.HTTP_204_NO_CONTENT
        else:
            cart.c_goods_num = cart.c_goods_num - 1
            cart.save()
            data["status"] = status.HTTP_200_OK
        data["total_price"] = self.calc_total_price()
        return data
