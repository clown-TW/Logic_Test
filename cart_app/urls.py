from flask_restful import Api

from cart_app.views import CartsResource

cart_api = Api()

cart_api.add_resource(CartsResource, "/carts/")