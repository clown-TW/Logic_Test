from flask_restful import Api

from goods_app.views import GoodsTypeResource, GoodsTypeCateResource, GoodsResource

goods_api = Api()

goods_api.add_resource(GoodsTypeResource,"/goodstypes/")

goods_api.add_resource(GoodsTypeCateResource,"/goodstypecates/")

goods_api.add_resource(GoodsResource,"/goods/")

