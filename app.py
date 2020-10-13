from flask import Flask, render_template, request, json, jsonify
import os
import csv
from pymongo import MongoClient
import pymongo
import re
from bson import BSON
from bson import json_util

import sys
sys.path.insert(0, '../secret/')
sys.path.insert(0, '../mongodb/')
sys.path.insert(0, 'nlp/')
sys.path.insert(0, '../Scrapping/')
from secret.config import MongodbConfig
from model_API import Prediction
from model_noapi import Predictions_noapi
import numpy as np
import pandas as pd
from nlp.video_summary import caption_text, splitting_text, summarizer_text

#app initialization
app = Flask(__name__, template_folder='templates')

# global variables for data persistence across requests
model_output=""

# If you work on local mongo compass write "local", 
# and if you work on mongo atlas write "altas" in MongodbConfig
URI = MongodbConfig("atlas")
client = pymongo.MongoClient(URI)
db = client.get_database('youtube_trends')
wc = Prediction("text")
noapi = Predictions_noapi("link")

# main index page route
@app.route('/', methods=['GET','POST'])
@app.route('/channels', methods=['GET','POST'])
def index():
    channelList = db.channel_info.find(limit=100)
    if request.method == "POST":
        #channel search
        channelSearch = request.form['channelSearch']
        if channelSearch != "":
            regex = ".*".join((channelSearch, ".*"))
            channelList = db.channel_info.find({'title': re.compile(regex, re.IGNORECASE)})

    return render_template('index.html',channelList=channelList)


@app.route('/channelData', methods=['GET'])
def channelData():
    channelList = db.channel_info.find(limit=25)
    title = []
    viewcount = []
    for channel in channelList:
        title.append(channel['title'])
        viewcount.append(channel['viewcount'])

    result = {
        'labels': title,
        'viewcount': viewcount
    }

    return json.dumps(result, default=json_util.default)


# main index page route
@app.route('/channel-details', methods=['GET','POST'])
def channelDetails():
    channelId = request.args.get('channelId')
    videoData = db.video_data.find({'channelid': channelId})
    channelList = db.channel_info.find({'channelid': channelId})

    return render_template('channel-details.html',videoData=videoData, channelList=channelList)


@app.route('/videoData', methods=['GET'])
def videoData():
    channelId = request.args.get('channelId')
    videoData = db.video_data.find({'channelid': channelId})

    title = []
    viewcount = []
    likecount = []
    dislikecount = []
    for video in videoData:
        title.append(video['video_title'])
        viewcount.append(video['videoviewcount'])
        likecount.append(video['videolikeCount'])
        dislikecount.append(video['videodislikecount'])

    result = {
        'labels': title,
        'viewcount': viewcount,
        'likecount':likecount,
        'dislikecount':dislikecount
    }

    return json.dumps(result, default=json_util.default)


@app.route('/youtuber', methods=['GET','POST'])
def youtubers():
    youtuberList = db.youtuber_list.find()
    return render_template('youtuber_list.html',youtuberList=youtuberList)


# features page route
@app.route('/channel-features', methods=['GET','POST'])
def channelFeatures():
    channelId = request.args.get('channelId')
    featureChannels = db.featured_channels.find({'channelid': channelId})
    youtuberList = db.youtuber_list.find({'Channelid': channelId})
    
    featureIdList = []
    for featureId in featureChannels:
        featureIdList.append(featureId['featuredChannelsUrls'])
    

    featureChannelsInfo = db.featured_channels_info.find({"channelid" : {"$in": featureIdList}})
    
    return render_template('channel-features.html', featureChannelsInfo=featureChannelsInfo, youtuberList=youtuberList)


@app.route('/featureData', methods=['GET'])
def featureData():
    channelId = request.args.get('channelId')
    featureChannels = db.featured_channels.find({'channelid': channelId})
    #youtuberList = db.youtuber_list.find({'Channelid': channelId})
    
    featureIdList = []
    for featureId in featureChannels:
        featureIdList.append(featureId['featuredChannelsUrls'])
    
    featureChannelsInfo = db.featured_channels_info.find({"channelid" : {"$in": featureIdList}})

    title = []
    viewcount = []
    subscribercount = []
    country = []

    for feature in featureChannelsInfo:
        title.append(feature['title'])
        viewcount.append(feature['viewCount'])
        subscribercount.append(feature['subscriberCount'])
        country.append(feature['Country'])
    
    nochannel = len(title) > 0

    result = {
        'labels': title,
        'viewcount': viewcount,
        'subscribercount':subscribercount,
        'country':country,
        'nochannel':nochannel
    }

    return json.dumps(result, default=json_util.default)

@app.route('/video-comments', methods=['GET','POST'])
def videoComments():
    videoId = request.args.get('videoId')
    videoData = db.video_data.find({'videoid': videoId})
    videoComments = db.video_comment.find({'videoid': videoId})

    return render_template('video-comments.html',videoComments=videoComments, videoData=videoData)

@app.route('/comments-sentiments', methods=['GET'])
def videoCommentsSentiment():
    videoId = request.args.get('videoId')

    df_comments = pd.DataFrame(db.video_comment.find({'videoid': videoId}),columns=['textdisplay'])
    #print(df_comments)

    sentiments = wc.sentiment_analysis_comments(videoId, df_comments)
    #print(sentiments)

    title = ['POSITIVE','NEGATIVE']
    sentiment = []
    sentiment.append(sentiments[1])
    sentiment.append(sentiments[2])

    positive = sentiments[1] > sentiments[2]

    result = {
        'title': title,
        'sentiment': sentiment,
        'positive' : positive
    }

    return json.dumps(result, default=json_util.default)


@app.route('/statistics', methods=['GET'])
def statistics():
    return render_template('statistics.html')




@app.route('/sentiments', methods=['GET','POST'])
def Sentiment_noapi():
    
    # if request.method == "POST":
    #     #youtube search
    #     youtubeSearch = request.form['youtubeSearch']
    #     if youtubeSearch != "":
    #         ysentiments = noapi.sentiment_analysis(youtubeSearch)
    #         sentiment_noapi=[]
    #         sentiment_noapi.append(ysentiments[1])
    #         sentiment_noapi.append(ysentiments[2])
    #         positive = ysentiments[1] > ysentiments[2]
    #         sentiment_result = {
    #             'title': ['POSITIVE','NEGATIVE'],
    #             'sentiment_noapi': sentiment_noapi,
    #             'positive' : positive
    #         }
    #         print(sentiment_result)
    #         return render_template('sentiments.html')

    return render_template('sentiments.html')

@app.route('/sentiments-data', methods=['GET'])
def sentimentsData():
    youtubeSearch = request.args.get('youtubeSearch')
    sentiment_result = {
        'title': ['POSITIVE','NEGATIVE'],
        'sentiment_noapi': [0,0],
        'positive' : 'false'
    }
    if youtubeSearch != "":
        ysentiments = noapi.sentiment_analysis(youtubeSearch)
        sentiment_noapi=[]
        sentiment_noapi.append(ysentiments[1])
        sentiment_noapi.append(ysentiments[2])
        positive = ysentiments[1] > ysentiments[2]
        sentiment_result = {
            'title': ['POSITIVE','NEGATIVE'],
            'sentiment_noapi': sentiment_noapi,
            'positive' : positive
        }

    return json.dumps(sentiment_result, default=json_util.default)

@app.route('/statistics-data', methods=['GET','POST'])
def statisticsData():

    df_youtuber = pd.DataFrame(db.youtuber_list.find(),columns=['ChannelInfo', 'Category','Subscribers', 'Avg', 'NoxScore'])
    #viewList = db.youtuber_list.find()
    cat = df_youtuber.groupby(['Category']).size().reset_index(name='Count')
    categoryCount = cat['Count'].tolist()
    catList = cat['Category'].str.strip().tolist()
    categoryName = ["None" if x == '' else x for x in catList]
    
    channelInfo = df_youtuber['ChannelInfo'].str.strip().tolist()
    subscribercount = df_youtuber['Subscribers'].tolist()
    #avg = df_youtuber['Avg']
    viewcountList = []
    for view in df_youtuber['Avg']:
        viewcountList.append(view['Views'])

    # viewcountList = df_youtuber['Avg'].tolist()
    viewcountList = [word.replace('719.8%','') for word in viewcountList]
    viewcountList = [word.replace('↑','').strip() for word in viewcountList]
    viewcountList = [word.replace('-','0').strip() for word in viewcountList]

    tbl = {'K':1, 'M':1_000, 'B':1_000_000}
    subscribercount = [int(i) for i in (re.sub(r'([\d\.]+)(K|M|B)', lambda v: str(int(float(v.groups()[0]) * tbl[v.groups()[1]])), i) for i in df_youtuber['Subscribers'])]

    viewcount = [int(i) for i in (re.sub(r'([\d\.]+)(K|M|B)', lambda v: str(int(float(v.groups()[0]) * tbl[v.groups()[1]])), i) for i in viewcountList)]
    score = []

    result = {
        'categoryName': categoryName,
        'categoryCount' : categoryCount,
        'channelInfo' : channelInfo,
        'viewcount': viewcount,
        'subscribercount':subscribercount,
        'score':score
    }

    return json.dumps(result, default=json_util.default)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
