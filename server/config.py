class Config(object):
    DEBUG = False
    TESTING = False
    SLASH_COMMAND = "/ichu"
    DATABASE_URI = "mongodb://localhost:27017/ichooseyoudb"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SLASH_COMMAND = "/slash_command"
    DATABASE_URI = "mongodb://localhost:27017/ichooseyoudb_test"


CONFIG = {"prod": ProductionConfig, "dev": DevelopmentConfig, "test": TestingConfig}
