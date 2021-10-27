from flask import jsonify

from common import status

def load_middleware(app):
    @app.errorhandler
    def error_handle(e):
        print(e)
        data = {
            "msg": "网络异常",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
        }

        return jsonify(data)