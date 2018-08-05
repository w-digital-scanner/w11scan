from celery import Celery

celery_app = Celery('app',include=['cms.tasks'])
celery_app.config_from_object('celery_config')

# useage:
# celery -A whatcms worker -l info/warning