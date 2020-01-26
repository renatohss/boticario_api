from pymongo import MongoClient

client = MongoClient('172.17.0.2:27017')

print(client.list_database_names())