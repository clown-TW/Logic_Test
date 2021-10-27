import random
import secrets
import uuid

from flask import request
from flask_restful import Resource, marshal, fields

from axf_api.extension import cache
from common import status, msg
from user_app.models import User

user_fields = {
    "username":fields.String,
    "phone":fields.String,
    "icon":fields.String,
    # "birth":fields.DateTime,
    "age":fields.Integer,
    "is_vip":fields.Boolean,
    "level":fields.Integer,
    # "register_time":fields.DateTime,
}

class UsersResource(Resource):

    def get(self):
        token = request.args.get("token")
        user = cache.get(token)

        if not user:
            data = {
                "msg":"用户身份失效",
                "status":status.HTTP_400_BAD_REQUEST
            }
            return data
        data = {
            "msg":msg.MSG_OK,
            "status":status.HTTP_200_OK,
            "data":marshal(user,user_fields)
        }
        return data

    def post(self):

        action = request.args.get("action")

        if action == "register":
            return self.do_register()
        elif action == "get_code":
            return self.do_get_code()
        elif action == "login":
            return self.do_login()
        elif action == "logout":
            return self.do_logout()

        data = {
           "msg":msg.MSG_OK,
            "status":status.HTTP_200_OK
        }
        return data

    def do_register(self):

        username = request.form.get("username")

        phone = request.form.get("phone")

        password = request.form.get("password")

        code = request.form.get("code")

        verify_code = cache.get(phone)

        print(code,verify_code)

        if code is None or str(code) != str(verify_code):

            data = {
                "msg":msg.MSG_VERIFY_CODE_ERROR,
                "status":status.HTTP_400_BAD_REQUEST
            }
            return data

        user = User(username=username,password=password,phone=phone)

        if user.save():

            data = {
                "msg":msg.MSG_OK,
                "status":status.HTTP_201_CREATED
            }
            return data
        else:
            data = {
                "msg": msg.MSG_REGISTER_FAILED,
                "status": status.HTTP_400_BAD_REQUEST
            }
            return data


    def do_get_code(self):

        phone = request.form.get("phone")
        # 判断手机号的有效性

        # send_code
        source_code = "qwertyuiopasdfghjklzxcvbnm7894561230QWERTYUIOPASDFGHJKLZXCVBNM"

        code = "".join(random.choices(source_code,k=4))

        print(phone,code)

        # 记录发送的验证码
        cache.set(phone,code,timeout=60*60*24*7)

        data = {
            "msg": msg.MSG_OK,
            "status": status.HTTP_200_OK,
            "data":{
                "code":code
            }
        }
        return data

    def do_login(self):

        username = request.form.get("username")

        password = request.form.get("password")

        users = User.query.filter_by(username=username).all()

        if not users:
            data = {
                "msg":"用户不存在",
                "status":status.HTTP_404_NOT_FOUND
            }
            return data

        user = users[0]

        if not user.verify_password(password):
            data = {
                "msg": "密码错误",
                "status": status.HTTP_401_UNAUTHORIZED
            }
            return data
        # 生成token
        # token = uuid.uuid4().hex
        token = secrets.token_hex()
        # 存储token
        cache.set(token,user,timeout=60*60*24*7)

        data = {
            "msg": "登录成功",
            "status": status.HTTP_200_OK,
            "data":{
                "token":token
            }
        }
        return data

    def do_logout(self):
        token = request.form.get("token")

        cache.delete(token)

        data = {
            "msg":msg.MSG_OK,
            "status":status.HTTP_204_NO_CONTENT
        }
        return data
