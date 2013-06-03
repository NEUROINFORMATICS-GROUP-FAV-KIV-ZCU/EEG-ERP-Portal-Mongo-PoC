__author__ = 'Jakub Danek'
"""
Functions for operating mongodb instance.
"""

from pymongo import MongoClient
import json
from pprint import pprint

#init db connection
client = MongoClient()
db = client.db_experiment
collection = db.experiments


"""
Converts provided exps list (list of experiments) into a dictionary form and stores
it in the mongo db.
Saves the data in several bulks to avoid maximum message size problem.
"""
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

"""
Insert provided dictionary set into the db.
"""
def insert_many(data=None):
    if(data == None):
        return None

    return collection.insert(data)

"""
Returns list of experiment ids based on search dictionary.
See mongoDB documentation for dictionary structure.
"""
def find_ids(searchDictionary = {}):
     return list(collection.find(searchDictionary, {"experiment_id" : 1, "_id" : 0}))