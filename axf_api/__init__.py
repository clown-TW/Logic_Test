from flask import Flask

from axf_api.extension import init_extension
from axf_api.middleware import load_middleware

from axf_api.settings import envs
from axf_api.route import init_route


def create_app(env):

    app = Flask(__name__,template_folder="../templates",static_folder ="../static")
    # 初始化配置
    app.config.from_object(envs.get(env))
    # 加载第三方库
    init_extension(app)
    # 加载中间件
    load_middleware(app)
    # 加载路由
    init_route(app)

    return app