from flask_restful import Api

from order_app.views import OrdersResource

order_api = Api()

order_api.add_resource(OrdersResource, "/orders/")