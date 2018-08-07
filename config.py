class Config(object):
    UserName = "admin"
    PassWord = "w11scan"

redis_host = "localhost"
redis_port = 6379
redis_password = ""

mongodb_host = 'localhost'
mongodb_port = 27017
mongodb_username = ''
mongodb_password = ''

BROKER_URL = "redis://localhost:6379/1"
# redis://password@hostname:port/db_number
if redis_password == "":
    BROKER_URL = "redis://{}:{}/1".format(redis_host,redis_port)
else:
    BROKER_URL = "redis://{}@{}:{}/1".format(redis_password,redis_host,redis_port)

CELERY_RESULT_BACKEND = "mongodb://localhost:27017/w11scan_celery"
# mongodb://user:password@localhost:27017/w11scan_celery

if mongodb_username == "" and mongodb_password == "":
    CELERY_RESULT_BACKEND = "mongodb://{}:{}/w11scan_celery".format(mongodb_host,mongodb_port)
else:
    CELERY_RESULT_BACKEND = "mongodb://{}:{}@{}:{}/w11scan_celery".format(mongodb_username,mongodb_password,mongodb_host,mongodb_port)
