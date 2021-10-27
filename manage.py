import os

from flask_cors import CORS
from flask_migrate import MigrateCommand
from flask_script import Manager

from axf_api import create_app
# 从环境变量获取值，决定代码运行于何种机制
env = os.environ.get("AXF_API") or "default"
# 根据环境创建flask对象
app = create_app(env)
# 处理跨域
CORS(app,supports_credentials=True)
# 添加命令行管理者
manager = Manager(app)
# 添加迁移指令
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
