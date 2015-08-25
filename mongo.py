__author__ = 'vincentnewpro'

import pymongo
import datetime
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('107.170.115.138', 27017)

db = client['Shuzhai']
collection = db['BookListings']

def writeToMongo(post):
    if collection.find_one({"docid":post["docid"]}) is None:
        return collection.insert_one(post).inserted_id

def checkDocExsists(docid):
    if collection.find_one({"docid":docid}) is None:
        return False
    else:
        return True

#print(collection.find_one())
print(checkDocExsists('912201'))