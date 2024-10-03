class Config:
    SECRET_KEY  = 'fuhjfgijtcdryurditfitruidryur'
    DEBUG       = True

class DevelopmentConfig(Config):
    MYSQL_HOST      = 'localhost'
    MYSQL_USER      = 'root'
    MYSQL_PASSWORD  = 'mysql'
    MYSQL_DB        = 'techcafe'


config = {
    'development': DevelopmentConfig 
}       