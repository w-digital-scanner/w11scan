
from pymongo import MongoClient
import json

# db connect
class MongDB(object):
    def __init__(self,host = 'localhost',port = 27017,database = 'w11scan',username = '',password = ''):
        self.host = host
        self.port = port
        self.database = database
        self.conn = MongoClient(self.host,self.port)
        self.coll = self.conn[self.database]
        # self.coll.authenticate(username,password)

# with open("cms.json") as f:
#     data = json.load(f)
#
# db = MongDB()
# db.coll["cmsdna"].insert_many(data)
#
# # print(db.coll.collection_names())
#
# collections = db.coll.collection_names()
# for k,v in data.items():
#     # db.coll[k].insert_many(v)
#     for i in v:
#         i["hit"] = 0
#         if i["option"] == "regx":
#             i["option"] = "keyword"
#     db.coll[k].insert_many(v)
    # print(v)

# for i in collections:
#     cursor = db.coll[i].find()
#     for f in cursor:
#         print(f)