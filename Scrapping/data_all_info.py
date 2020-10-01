# Python program to convert 
# JSON file to CSV 
  
import json 
import csv
import pandas as pd 
import datetime
  
# Opening JSON file and loading the data 
# into the variable data 

def _getToday():
    return datetime.date.today().strftime("%Y%m%d")

def all_info():
    with open('../data/data_all_info.json') as json_file: 
        data = json.load(json_file) 

    _id = []
    title = []
    description = []
    url = []
    language = []
    viewCount = []
    subscriberCount = []
            
    for item in data['channelinfos']:
        for snip in item['items']:
            _id.append(snip['id'])
            title.append(snip['snippet']['title'])
            description.append(snip['snippet']['description'])
            url.append(snip['snippet']['thumbnails']['high']['url'])
            language.append(snip['snippet']['country'])       
            viewCount.append(snip['statistics']['viewCount'])
            subscriberCount.append(snip['statistics']['subscriberCount'])


    df = pd.DataFrame(list(zip(_id,title,description,url,language,viewCount,subscriberCount)), 
                columns =['channelid','title','description','url','language','viewcount','subscribercount'])

    filename = "%s%s%s" % ("data/data_all_info", _getToday() ,".csv")
    df.to_csv(filename)

    return df

