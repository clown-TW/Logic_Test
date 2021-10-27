import datetime


from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

from axf_api.extension import db
from common.models import BaseModel


class User(BaseModel):
    username = db.Column(db.String(32),unique=True)
    phone = db.Column(db.String(16),unique=True)
    # 存云存储，我们只要地址
    icon = db.Column(db.String(256),nullable=True)
    # 要做密码安全
    _password = db.Column(db.String(256))
    # 密码变成不可访问的字段
    @property
    def password(self):
        raise Exception("can't access")
    # 设置密码安全策略，对密码进行加密
    @password.setter
    def password(self,value):
        self._password = generate_password_hash(value)
    # 提供密码验证策略
    def verify_password(self,value):
        return check_password_hash(self._password,value)

    # 出生日期
    birth = db.Column(db.DateTime,default=datetime.datetime.now())
    # @property
    # def age(self):
    #     delta =  datetime.datetime.now() - self.birth
    #
    #     return delta.year



    is_vip = db.Column(db.Boolean,default=False)
    is_delete = db.Column(db.Boolean,default=False)

    @property
    def level(self):
        return 1

    register_time = db.Column(db.DateTime,default=datetime.datetime.now())


