import os


class BaseConfig(object):
    DEBUG = None
    # jwt的密钥
    SECRET_KEY = os.urandom(24)
    JWT_EXPIRE_TIME = 24
    # 数据库的连接信息
    # 数据库配置
    DB_HOST = 'localhost'
    DB_PORT = 13306
    DB_USERNAME = 'root'
    DB_PASSWORD = '123456'
    DB_NAME = 'SunCMS'

    DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 七牛配置
    QINIU_AK = "_k1OYVrwNoF0ALCVhmlVv89pDSbIJD5GzPlXXzej"
    QINIU_SK = "UysGleEpeyUrIdgYAifuxKyZj9qhlzqNOgWGAdeY"
    QINIU_BUCKETNAME = "literature-czl"
    QINIU_URLPREFIX = "http://qqvpxfcfz.hn-bkt.clouddn.com/"


class DevConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_ECHO = True  # 打印sql


class ProdConfig(BaseConfig):
    pass


config_dict = {
    'dev_config': DevConfig,
    'prod_config': ProdConfig
}
