
from pymongo import MongoClient
from config import mongodb_host,mongodb_password,mongodb_port,mongodb_username
import json

# db connect
class MongDB(object):
    def __init__(self,database = 'w11scan'):
        self.host = mongodb_host
        self.port = mongodb_port
        self.database = database
        self.conn = MongoClient(self.host,self.port)
        self.coll = self.conn[self.database]
        if mongodb_username != "" and mongodb_password != "":
            self.coll.authenticate(mongodb_username,mongodb_password)