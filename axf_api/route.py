from cart_app.urls import cart_api
from goods_app.urls import goods_api
from order_app.urls import order_api
from user_app.urls import user_api


def init_route(app):
    goods_api.init_app(app)
    user_api.init_app(app)
    cart_api.init_app(app)
    order_api.init_app(app)

