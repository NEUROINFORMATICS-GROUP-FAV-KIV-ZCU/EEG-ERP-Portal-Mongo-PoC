__author__ = 'Jakub Danek'

from pymongo import MongoClient
import json
from pprint import pprint

json_data = open('data/schema.json')
data = json.load(json_data)
json_data.close()


client = MongoClient()
db = client.db_experiment
collection = db.experiments


def init_mongo(exps=[]):
    collection.drop()
    list = []
    k = 0
    print "Transforming to MONGO..."
    for e in exps:
        list.append(e.to_dict())
        k += 1
        if(k % 1000 == 0) :
            insert_many(list)
            list = []
    print "MONGO data finished."

def insert_many(data=None):
    if(data == None):
        return None

    return collection.insert(data)

def find_ids(searchDictionary = {}):
     return list(collection.find(searchDictionary, {"experiment_id" : 1, "_id" : 0}))