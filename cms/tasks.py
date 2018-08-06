
import redis
import re
import math
import hashlib
from pymongo import MongoClient
import queue
import threading
import time
import requests
from bson.objectid import ObjectId
from whatcms import celery_app
from cms.otherscan import WebEye
import builtwith
from config import redis_host,redis_port,mongodb_host,mongodb_password,mongodb_port,mongodb_username

redisConn = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

class MongDB(object):
    def __init__(self,database = 'w11scan'):

        self.host = mongodb_host
        self.port = mongodb_port
        self.database = database
        self.conn = MongoClient(self.host,self.port)
        self.coll = self.conn[self.database]
        if mongodb_username and mongodb_password:
            self.coll.authenticate(mongodb_username,mongodb_password)

def AverageSplit(L,index):
    """
    Average split list
    """
    count = len(L)
    return [L[(i - 1) * index:i * index] for i in list(range(1, math.ceil(count / index) + 1))]

def getMD5(c):
    m = hashlib.md5()
    m.update(c)
    psw = m.hexdigest()
    return psw

def success(tmp,taskid):
    # 成功后先将结果更新到w11scan_config result表中，更新信息，然后更新w11scan表中指纹命中率

    # tmp {'_id': ObjectId('5b5f48158598842b975e03a8'), 'path': '/robots.txt', 'option': 'regx', 'content': 'wordpress','hit': 0, 'name': 'wordpress'}

    # 1.插入成功信息到w11scan_config resutl表中
    mongodb = MongDB(database="w11scan_config")
    data = {
        "status":"success",
        "webdna":{
            "cmsname":tmp["name"],
            "path":tmp["path"],
            "option": tmp["option"],
            "content": tmp["content"],
            "dnaid": tmp["_id"],
            "time": time.time()
        }
    }
    mongodb.coll["result"].update({"url":tmp["url"],"taskid":ObjectId(taskid)},{"$set":data})

    # 2. 更新指纹命中率
    dnaid = ObjectId(tmp["_id"])
    mongodb = MongDB(database="w11scan")
    mongodb.coll[tmp["name"]].update(
        {"_id": dnaid},
        {"$inc": {
            "hit": 1
        }}
    )



# 这只是预处理模块，不涉及扫描和判断部分
class whatweb(object):

    def __init__(self,urls):
        self.mongodb = MongDB()
        self.urls = urls
        self.cms_hash_list = {}

    def buildPayload(self):
        collections = self.mongodb.coll.collection_names()

        path_cache_hit = []
        for i in collections:
            cursor = self.mongodb.coll[i].find()
            for f in cursor:
                f["name"] = i
                path = f["path"]
                f["_id"] = str(f["_id"])
                if path not in self.cms_hash_list:
                    self.cms_hash_list[path] = []
                self.cms_hash_list[path].append(f)
                if str(f["hit"]).isdigit() and int(f["hit"]) > 0:
                    path_cache_hit.append((path, int(f["hit"])))

        # 组合指纹

        cms_key_cache = {}
        for k, v in self.cms_hash_list.items():
            cms_key_cache[k] = len(v)

        # 路径排名前十 [('/favicon.ico', 68), ('/robots.txt', 31), ('', 21), ('/license.txt', 6)
        pathList = sorted(cms_key_cache.items(), key=lambda d: d[1], reverse=True)

        # 按照路径进行排序，然后取出命中率前十的路径的指纹排序在前面。
        # [('/images/buttonImg/add.png', 1)]
        pathL = sorted(path_cache_hit, key=lambda x: x[1],reverse=True)[:10]

        # build OrderDict
        combine = []
        for item in pathL + pathList:
            if item[0] not in combine:
                combine.append(item[0])

        return AverageSplit(combine,10)

    def run(self):
        items = self.buildPayload()
        webList = []
        for item in items:
            # webDict = c1.OrderedDict()
            webDict = []
            for i in item:
                # webDict[i] = self.cms_hash_list[i]
                webDict.append(self.cms_hash_list[i])
            webList.append(webDict)
        return webList

# 分布式扫描程序,接收url和payload,一次接受多个payload,启动线程池消费
class WhatScan(object):

    def __init__(self,url,payload,taskid,threadnum = 10):
        self.queue = queue.Queue()
        self.threadNum = threadnum
        self.threadContinue = True
        self.domain = url
        self.taskid = taskid
        for i in payload:
            self.queue.put(i)
        self.result = []

    def exceptionHandledFunction(self):
        while not self.queue.empty() and self.threadContinue:

            payload = self.queue.get()
            # payload like [{'_id': ObjectId('5b5f48158598842b975e03a8'), 'path': '/robots.txt', 'option': 'regx','content': 'wordpress', 'hit': 0, 'name': 'wordpress'}
            if isinstance(payload,list) and len(payload):
                path = payload[0]["path"]
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
                }
                new_url = self.domain + path
                try:
                    r = requests.get(new_url, headers=headers)
                except:
                    print("error:" + new_url)
                    continue

                if r.status_code == 200:
                    bytes = r.content
                    html = r.text


                    for tmp in payload:
                        _id = tmp["_id"]
                        option = tmp["option"]
                        content = tmp["content"]
                        cmsname = tmp["name"]
                        tmp["url"] = self.domain
                        fingter = False

                        if option == "md5":
                            if content == getMD5(bytes):
                                fingter = True

                        elif option == "regx":
                            r = re.search(content, html)
                            if r:
                                fingter = True

                        elif option == "keyword":
                            if content in html:
                                fingter = True

                        if fingter:
                            self.result.append(tmp)
                            redisConn.delete(self.domain)
                            success(tmp,self.taskid)
                            print(tmp)


    def run(self):

        threads = []
        for numThread in list(range(self.threadNum)):
            thread = threading.Thread(target=self.exceptionHandledFunction, name=str(numThread), args=[])
            thread.daemon = True
            thread.start()
            threads.append(thread)

        # And wait for them to all finish
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.isAlive():
                    alive = True
                    time.sleep(0.1)

        if len(self.result) == 0:
            return False
        return self.result

@celery_app.task
def otherscan(url,taskid):
    res = WebEye(url)
    res.run()
    cms = list(res.cms_list)
    title = res.title()
    try:
        build = builtwith.builtwith(url)
    except:
        build = {}
    if cms:
        build["other"] = cms

    mongodb = MongDB(database="w11scan_config")
    data = {
        "status": "finish",
        "other":build,
        "title":title
    }
    mongodb.coll["result"].update({"url": url, "taskid": ObjectId(taskid)}, {"$set": data})


@celery_app.task
def buildPayload(url,taskid):
    what = whatweb(url)
    redisConn.set(url, "1",ex=60*60*24)
    wli = what.run()
    for ordict in wli:
        singscan.delay(url,ordict,taskid)
    otherscan.delay(url,taskid)
    # other

@celery_app.task
def singscan(url,ordict,taskid):
    value = redisConn.get(url)
    if value is None or value != "1":
        return False
    scan = WhatScan(url, ordict,taskid)
    l = scan.run()
    return l

if __name__ == '__main__':
    url = "https://x.hacking8.com"
    # buildPayload(url)