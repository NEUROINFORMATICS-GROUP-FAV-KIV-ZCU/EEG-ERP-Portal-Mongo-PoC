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
collection.drop()


def insert_many(data=None):
    if(data == None):
        return None

    return collection.insert(data)