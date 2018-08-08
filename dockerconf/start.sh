#!/bin/bash

XUNFENG_BASE=/opt/w11scan
cd $XUNFENG_BASE
XUNFENG_LOG=/var/log/xunfeng
MONGODB_PATH=/data/db

[ ! -d $XUNFENG_LOG ] && mkdir -p ${XUNFENG_LOG}
[ ! -d $MONGODB_PATH ] && mkdir -p ${MONGODB_PATH}

nohup redis-server > ${XUNFENG_LOG}/redis.log &
nohup mongod --bind_ip 127.0.0.1 --port 65521 --dbpath=${MONGODB_PATH}> ${XUNFENG_LOG}/db.log &
sleep 3s
mongorestore -h 127.0.0.1 --port 65521 -d w11scan ${XUNFENG_BASE}/backup/w11scan
mongo 127.0.0.1:65521 < ${XUNFENG_BASE}/dockerconf/mongoauth
python3 ${XUNFENG_BASE}/manage.py migrate
nohup python3 ${XUNFENG_BASE}/manage.py runserver 0.0.0.0:8000 > ${XUNFENG_LOG}/web.log &
nohup celery -A whatcms worker -l info > ${XUNFENG_LOG}/celery.log &
nohup celery -A whatcms worker -l info > ${XUNFENG_LOG}/celery2.log &
/usr/bin/tail -f /dev/null
