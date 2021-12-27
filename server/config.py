class Config(object):
    DEBUG = False
    TESTING = False
    APP_NAME = "I choose you"
    SLASH_COMMAND = "/ichu"
    API_URL = "https://ichooseyou.etienne-t.fr"
    WAIT_FOR_THREAD_BEFORE_RETURN = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    APP_NAME = "I choose you dev"
    SLASH_COMMAND = "/ichu_dev"
    API_URL = "https://7852-62-23-96-26.ngrok.io"


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    APP_NAME = "I choose you test"
    SLASH_COMMAND = "/slash_command"
    DATABASE_URI = "mongodb://localhost:27017/ichooseyoudb_test"
    WAIT_FOR_THREAD_BEFORE_RETURN = True


CONFIG = {"prod": ProductionConfig, "dev": DevelopmentConfig, "test": TestingConfig}
