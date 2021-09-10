class Config(object):
    DEBUG = False
    TESTING = False
    APP_NAME = "I choose you"
    SLASH_COMMAND = "/ichu"
    DATABASE_URI = "mongodb://localhost:27017/ichooseyoudb"
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
    API_URL = "https://bfa847856e78.ngrok.io"


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    APP_NAME = "I choose you test"
    SLASH_COMMAND = "/slash_command"
    DATABASE_URI = "mongodb://localhost:27017/ichooseyoudb_test"
    WAIT_FOR_THREAD_BEFORE_RETURN = True


CONFIG = {"prod": ProductionConfig, "dev": DevelopmentConfig, "test": TestingConfig}
