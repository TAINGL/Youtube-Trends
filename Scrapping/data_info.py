# Python program to convert 
# JSON file to CSV 
  
import json 
import csv
import pandas as pd
import sys
import os 

arguments = str(sys.argv)
# Opening JSON file and loading the data 
# into the variable data 
print(arguments)
with open(sys.argv[1]) as json_file: 
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
        if 'country' in snip['snippet']:
            language.append(snip['snippet']['country'])
        else:
            language.append("") 
        viewCount.append(snip['statistics']['viewCount'])
        subscriberCount.append(snip['statistics']['subscriberCount'])
  
df = pd.DataFrame(list(zip(_id,title,description,url,language,viewCount,subscriberCount)), 
               columns =['channelid','title','description','url','language','viewcount','subscribercount']) 

filename='../data/data_all_info.csv'

with open(filename, 'a') as f:
    df.to_csv(f, header=f.tell()==0)
    

