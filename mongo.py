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
id = collection.insert(data)

for experiment in collection.find({"configuration.temperature" : 101}):
    pprint(experiment)

