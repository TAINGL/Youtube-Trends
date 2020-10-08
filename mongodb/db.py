
from pymongo import MongoClient
from pymongo import ReturnDocument
from bson.objectid import ObjectId
from secret.config import MongodbConfig


import pymongo

# If you work on local mongo compass write "local", 
# and if you work on mongo atlas write "altas" in MongodbConfig
URI = MongodbConfig("atlas")
client = pymongo.MongoClient(URI)

for database_name in client.list_database_names():  
    print("Database - "+database_name)  
    for collection_name in client.get_database(database_name).list_collection_names():  
        print(collection_name)  

collection = client.youtube_trends.channel_info
collection = client.youtube_trends.channel_info


collection.insert_many(booksData)  