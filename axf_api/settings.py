def get_db_uri(dbinfo):
    database = dbinfo.get("DATABASE")
    driver = dbinfo.get("DRIVER")
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")
    return "{}+{}://{}:{}@{}:{}/{}".format(database,driver,user,password,host,port,name)


class Config:

    DEBUG = False

    TESTING = False

    SECRET_KEY = "TYUIOPFGHJKYUI"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    DEBUG = True

    dbinfo = {
        "DATABASE":"mysql",
        "DRIVER":"pymysql",
        "USER":"root",
        "PASSWORD":"123456",
        "HOST":"localhost",
        "PORT":"3306",
        "NAME":"axf",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestingConfig(Config):
    TESTING = True

    dbinfo = {
        "DATABASE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "axf",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

class StagingConfig(Config):
    dbinfo = {
        "DATABASE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "axf",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

class ProductConfig(Config):
    dbinfo = {
        "DATABASE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "axf",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

envs = {
    "develop":DevelopConfig,
    "default":DevelopConfig,
    "testing":TestingConfig,
    "staging":StagingConfig,
    "product":ProductConfig,
}