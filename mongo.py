__author__ = 'vincentnewpro'

import pymongo
import datetime
from pymongo import MongoClient
import json


client = MongoClient()
client = MongoClient('107.170.115.138', 27017)

db = client['Shuzhai']
collection = db['BookListings']

def writeToMongo(post):
    if collection.find_one({"docid":post["docid"]}) is None:
        post_id = collection.insert_one(post).inserted_id


print(collection.find_one())