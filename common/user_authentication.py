from flask import request, g

from axf_api.extension import cache
from common import status


def login_required(fun):

    def wrapper(*args, **kwargs):
        try:
            token = request.args.get("token")

            user = cache.get(token)

            if not user:
                raise Exception("用户不存在")
        except Exception as e:
            print(e)

            data = {
                "msg": "authentication failed",
                "status":status.HTTP_401_UNAUTHORIZED
            }
            return data
        g.user = user

        return fun(*args, **kwargs)
    return wrapper
