class Config(object):
    UserName = "admin"
    PassWord = "admin"

BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "mongodb://localhost:27017/w11scan_celery"

redis_host = "localhost"
redis_port = 6379

mongodb_host = 'localhost'
mongodb_port = 27017
mongodb_username = ''
mongodb_password = ''