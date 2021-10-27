from flask_restful import Api

from user_app.views import UsersResource

user_api = Api()

user_api.add_resource(UsersResource, "/users/")