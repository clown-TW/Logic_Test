from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# 创建orm对象
db = SQLAlchemy()
# 创建迁移对象
migrate = Migrate()
# 创建缓存对象
cache = Cache(config={
    "CACHE_TYPE":"redis",
    "CACHE_REDIS_URL":"redis://:123456@localhost:6379/1"
})

def init_extension(app):
    db.init_app(app)
    migrate.init_app(app,db)
    cache.init_app(app)