class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'tping'
"""
PARA QUE ANDE DESDE INTERNET:
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'bp0nuaifmebpf0bnmpef-mysql.services.clever-cloud.com'
    MYSQL_USER = 'uw3yygxhdjg6nxut'
    MYSQL_PASSWORD = 'g4ZwTLtgMw94BnBURaPW'
    MYSQL_DB = 'bp0nuaifmebpf0bnmpef'
    MYSQL_PORT = 3306
"""
config = {
    'development': DevelopmentConfig
}
