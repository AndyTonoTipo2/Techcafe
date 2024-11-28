class Config:
    SECRET_KEY  = 'fuhjfgijtcdryurditfitruidryur'
    DEBUG       = True

class DevelopmentConfig(Config):
    MYSQL_HOST      = 'localhost'
    MYSQL_USER      = 'root'
    MYSQL_PASSWORD  = 'mysql'
    MYSQL_DB        = 'techcafe'

#PythonAnywhere

'''MYSQL_HOST      = 'techcafe.mysql.pythonanywhere-services.com'
    MYSQL_USER      = 'techcafe'
    MYSQL_PASSWORD  = 'Andy6Jp1'
    MYSQL_DB        = 'techcafe$techcafe'''

class MailConfig(Config):
    MAIL_SERVER         ='smtp.gmail.com'
    MAIL_PORT           = 587
    MAIL_USE_TLS        = True
    MAIL_USE_SSL        = False
    MAIL_USERNAME       = 'andres.rojas1816@alumnos.udg.mx'       
    MAIL_PASSWORD       = 'ayas gvgs clbz vhol'
    MAIL_DEFAULT_SENDER  = 'andres.rojas1816@alumnos.udg.mx'
    MAIL_ASCII_ATTACHMENTS  = True
config = {
    'development': DevelopmentConfig,
    'mail'       : MailConfig              
}       