class Config:
    SECRET_KEY  = 'fuhjfgijtcdryurditfitruidryur'
    DEBUG       = True

class DevelopmentConfig(Config):
    '''MYSQL_HOST      = 'localhost'
    MYSQL_USER      = 'root'
    MYSQL_PASSWORD  = 'mysql'
    MYSQL_DB        = 'techcafe' '''

#PythonAnywhere

    MYSQL_HOST      = 'techcafe.mysql.pythonanywhere-services.com'
    MYSQL_USER      = 'techcafe'
    MYSQL_PASSWORD  = 'Andy6Jp1'
    MYSQL_DB        = 'techcafe$techcafe'

config = {
    'development': DevelopmentConfig 
}       