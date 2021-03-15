class Config(object):
    DEBUG = False
    TESTING = False
    SLASH_COMMAND = "/choose"
    DATABASE_URI = "mongodb://localhost:27017/ichooseyoudb"
    WAIT_FOR_THREAD_BEFORE_RETURN = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SLASH_COMMAND = "/choose_dev"


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SLASH_COMMAND = "/slash_command"
    DATABASE_URI = "mongodb://localhost:27017/ichooseyoudb_test"
    WAIT_FOR_THREAD_BEFORE_RETURN = True


CONFIG = {"prod": ProductionConfig, "dev": DevelopmentConfig, "test": TestingConfig}
