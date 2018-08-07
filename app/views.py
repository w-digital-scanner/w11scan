from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import config as config1
import json
from . import Conn
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
import time
from cms.tasks import buildPayload
from urllib.parse import urlparse
from app.Common import CreateTable
import re

# Create your views here.
def mgo_text_split(query_text):
    ''' split text to support mongodb $text match on a phrase '''
    sep = r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]'
    word_lst = re.split(sep, query_text)
    text_query = ' '.join('\"{}\"'.format(w) for w in word_lst)
    return text_query

def search(request):
    if not request.session.get('is_login',None):
        return redirect(login)

    keyword = request.GET.get("q", None)
    if keyword is None or keyword == "":
        return render(request, "search.html")
    words = keyword.split(";")
    query = {}
    for word in words:
        if ":" not in word:
            word = "all:" + word
        pro, suff = word.split(":")
        if pro == "cms":
            query["webdna.cmsname"] = suff
        elif pro == "url":
            query["url"] = {"$regex":suff,"$options":"i"}
        elif pro == "other":
            text_query = mgo_text_split(suff)
            query['$text'] = {'$search': text_query, '$caseSensitive': True}
        elif pro == "all":
            text_query = mgo_text_split(suff)
            query['$text'] = {'$search': text_query, '$caseSensitive': True}
    db = Conn.MongDB(database="w11scan_config")
    cursor = db.coll['result'].find(query)
    data = list(cursor)

    return render(request, "task_detail.html", {"cursor":data,"tasks":{"name":"{}的搜索结果".format(keyword)},"len":len(data)})

def task(request):
    if not request.session.get('is_login',None):
        return redirect(login)
    db = Conn.MongDB(database="w11scan_config")
    data = list(db.coll["tasks"].find().sort("time",-1))

    for item in data:
        item["time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item["time"]))


    return render(request,"task.html",{"data":data,"len":len(data)})

# 指纹界面
def plugin(request,slug = None):
    if not request.session.get('is_login',None):
        return redirect(login)

    page = int(request.GET.get("page",1))

    limit = 50

    db = Conn.MongDB()
    collections = db.coll.collection_names()
    delist = []
    if slug:
        for i in collections:
            # m = re.match(slug,i,re.IGNORECASE)
            # if not m:
            #     collections.remove(i)
            if slug not in i:
                delist.append(i)
        for i in delist:
            collections.remove(i)

    count = len(collections)
    if page < 1 or page > ceil(count/limit):
        page = 1

    start = (page - 1) * limit
    end = limit * page

    collections = collections[start:end]

    webdata = dict()
    for i in collections:
        cursor = db.coll[i].find()
        webdata[i] = {}
        webdata[i]["len"] = cursor.count()
        webdata[i]["data"] = cursor


    pagination = []

    if page >= 5:
        pagination.append('<li><a href="?page={}"><i class="fa fa-angle-left"></i>前一页</a></li>'.format(page - 1))
        for i in list(range(page-2,page+3)):
            if i == page:
                pagination.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
            else:
                pagination.append('<li><a href="?page={}">{}</a></li>'.format(i,i))
        pagination.append('<li><a href="?page={}"><i class="fa fa-angle-right"></i>后一页</a></li>'.format(page + 1))
    else:
        for i in list(range(1,ceil(count/limit))):
            if i == page:
                pagination.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
            else:
                pagination.append('<li><a href="?page={}">{}</a></li>'.format(i,i))


    return render(request,"plugin.html",{"cmsdata":webdata,"cmslen":count,"pagination":pagination})

def makeurl(url):
    if not url.startswith("http"):
        url =  "http://" + url
    p = urlparse(url)
    path = p.netloc
    if p.path:
        path = p.netloc + p.path.rstrip('/')

    new = "{}://{}".format(p.scheme,path)
    return new

@csrf_exempt
def plugin_add(request):
    cmsname = request.POST.get("cmsname")
    content = request.POST.get("content")
    result = {}
    try:
        jp = json.loads(content)
    except:
        result["status"] = "fail"
        return JsonResponse(result)

    if len(cmsname) == 0 and len(content) == 0:
        result["status"] = "fail"
        return JsonResponse(result)

    db = Conn.MongDB()
    db.coll[cmsname].insert_many(jp)

    result = {}
    result["status"] = "ok"
    return JsonResponse(result)

@csrf_exempt
def plugin_del(request):
    cmsname = request.POST.get("oid")
    db = Conn.MongDB()
    db.coll[cmsname].drop()
    return HttpResponse("success")

@csrf_exempt
def task_add(request):
    taskname = request.POST.get("taskname")
    taskdesc = request.POST.get("taskdesc")
    taskcontent = request.POST.get("taskcontent")

    result = {}

    if len(taskname) == 0 or len(taskcontent) == 0:
        result["status"] = "fail"
        return JsonResponse(result)

    jp = {}
    db = Conn.MongDB(database="w11scan_config")

    if not taskdesc:
        taskdesc = "这个人很懒，这都不想写。"
    jp["name"] = taskname
    jp["desc"] = taskdesc
    # jp["content"] = taskcontent.strip().splitlines()
    jp["time"] = time.time()
    insertid = db.coll["tasks"].insert_one(jp).inserted_id

    resultTB = []
    urls = set()
    for url in taskcontent.strip().splitlines():
        urls.add(makeurl(url))

    for item in urls:
        _result = {}
        _result["url"] = item
        _result["status"] = "pending"
        _result["taskid"] = insertid
        buildPayload.delay(item, str(insertid))
        resultTB.append(_result)

    if len(resultTB):
        db.coll["result"].insert_many(resultTB)

    result = {}
    result["status"] = "ok"
    return JsonResponse(result)

@csrf_exempt
def task_del(request):
    _id = request.POST.get("oid")
    db = Conn.MongDB(database="w11scan_config")
    db.coll["tasks"].delete_one({"_id":ObjectId(_id)})
    db.coll["result"].delete_many({"taskid":ObjectId(_id)})

    return HttpResponse("success")

def analysis(request):
    if not request.session.get('is_login',None):
        return redirect(login)

    db = Conn.MongDB(database="w11scan")
    collections = db.coll.collection_names()
    total_zw = len(collections)
    total_cms = 0
    for i in collections:
        total_cms += db.coll[i].count()

    db2 = Conn.MongDB(database="w11scan_config")
    total_scan = db2.coll["result"].count()
    total_finish = db2.coll["result"].find({"status":"finish"}).count()
    # 指纹总数 CMS种类 扫描总数 已完成

    group = {"$group":{"_id":"$webdna.cmsname","count":{"$sum":1}}}
    sort = {"$sort": {"count": -1}}

    groups = db2.coll["result"].aggregate([group,sort])
    stackBar = []
    for item in list(groups):
        if item.get("_id") is not None:
            stackBar.append(item)

    return render(request,"analysis.html",{"total_zw":total_zw,"total_cms":total_cms,"total_scan":total_scan,"total_finish":total_finish,"stackBar":json.dumps(stackBar)})

def config(request):
    if not request.session.get('is_login',None):
        return redirect(login)

    return render(request,"config.html",{})

def login(request):
    if request.session.get('is_login',None):
        return redirect(search)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        C = config1.Config()
        if username == C.UserName and password == C.PassWord:
            request.session['is_login'] = True
            request.session['username'] = username

            return redirect(search)


    return render(request,"login.html",{})

def logout(request):
    request.session.flush()
    return redirect(login)

@csrf_exempt
def edit(request):
    if not request.session.get('is_login',None):
        return redirect(login)

    slug = request.GET.get("slug",None)
    db = Conn.MongDB()

    if request.method == "POST":
        path = request.POST.get("path")
        option = request.POST.get("option")
        content = request.POST.get("content")
        hit = request.POST.get("hit")
        _id = request.POST.get("_id")
        delete = request.POST.get("delete",None)

        if delete:
            if delete == "add":
                return HttpResponse("success")

            db.coll[slug].remove({"_id": ObjectId(delete)})
            return HttpResponse("success")

        # add update
        if _id == "add":
            # 添加指纹
            insertid = {
                "path":path,
                "option":option,
                "content":content,
                "hit":hit
            }
            db.coll[slug].insert(insertid)
            return HttpResponse("success")

        else:
            # 更新指纹
            db.coll[slug].update({"_id":ObjectId(_id)},{
                "path": path,
                "option": option,
                "content": content,
                "hit": int(hit)
            })
            return HttpResponse("success")

    if slug is None:
        return redirect(login)

    x = db.coll[slug].find()


    return render(request,"edit.html",{"cursor":x,"cmsname":slug})

def detail(request,slug = ""):

    if not request.session.get('is_login',None):
        return redirect(login)

    db = Conn.MongDB(database="w11scan_config")

    tasks = db.coll["tasks"].find_one({"_id":ObjectId(slug)})

    data = db.coll["result"].find({"taskid":ObjectId(slug)})

    return render(request, "task_detail.html", {"cursor":data,"tasks":tasks,"len":data.count()})

def download(request,slug = ""):

    if not request.session.get('is_login',None):
        return redirect(login)

    db = Conn.MongDB(database="w11scan_config")

    tasks = db.coll["tasks"].find_one({"_id":ObjectId(slug)})
    colname = tasks.get("name",None)
    taskdate = tasks.get("time",None)
    if taskdate is None:
        return HttpResponse("faild,taskid invalid")
    taskdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(taskdate))
    data = db.coll["result"].find({"taskid":ObjectId(slug)})
    # { "_id" : ObjectId("5b6696d78598849b135dd44e"), "url" : "http://okoko.cn", "status" : "finish", "taskid" : ObjectId("5b6696d78598849b135dd448"), "other" : { "web-servers" : [ "Tengine" ], "other" : [ "Langeuage:php", "Server:Tengine/1.4.2", "X-Powered-By:PHP/5.3.10" ] }, "title" : "okoko.cn-您正在访问的网站可以合作！" }
    # ['任务状态', '域名', '网站标题', 'CMS识别结果', '其他信息']
    show = []
    for i in data:
        cms = i.get("webdna","")
        if cms != "":
            cms = cms.get("cmsname","")
        _ = [i.get("status",""),i.get("url",""),i.get("title",""),cms,repr(i.get("other",""))]
        show.append(_)
    siov = CreateTable(show,colname)

    response = HttpResponse(siov, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename={}.xls'.format(taskdate)
    response.write(siov)

    return response


