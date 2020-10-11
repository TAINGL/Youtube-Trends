from pymongo import MongoClient
from pymongo import ReturnDocument
from bson.objectid import ObjectId

import sys
sys.path.insert(0, '../secret/')
from secret.config import MongodbConfig


from os import listdir
from os.path import isfile, join

import pymongo
import pandas as pd

# If you work on local mongo compass write "local", 
# and if you work on mongo atlas write "altas" in MongodbConfig
URI = MongodbConfig("atlas")
client = pymongo.MongoClient(URI)

# Create Database if it's not already created
for database_name in client.list_database_names():  
    print("Database - "+database_name)
    
    if "youtube_trends" in database_name:
        print("The database exists.")
    else:
        db = client.youtube_trends
        print('The database is created.')
        
# Create collection in your database if it's not already created
for collection_name in client.get_database(database_name).list_collection_names():  
    print(collection_name)

    collection_list = ['channel_info', 'featured_channels', 'featured_channels_info',
                        'video_comment', 'video_data', 'youtuber_list']
    
    for collection in collection_list:

        if collection in database_name:
            print("The collection exists.")
        else:
            collection = client.collection
            print('The collection is created.')


def csv_to_json(filename, header=None):
    """
    Convert CSV to Json 
    """
    data = pd.read_csv(filename, header=None)
    return data.to_dict('records')


def get_csv_file(mypath):
    """
    mypath is path where you have your folder data projet with all csv file
    """
    csv_file = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.DS_Store' != f]
    print(csv_file)


def insert_csv(csv_file):
    """
    Insert Many CSV to divers collections on your database
    """
    collection_db = [db.channel_info, db.featured_channels, db.featured_channels_info,
                        db.video_comment, db.video_data, db.youtuber_list]

    for csv in csv_file:
        data = pd.read_csv(csv, header=None)
        data_dict = data.to_dict('records')

        for collection in collection_db: 
            collection.insert_many(data_dict)
        
        return "CSV inserted!"  
