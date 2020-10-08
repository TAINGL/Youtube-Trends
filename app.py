from flask import Flask, render_template, request
import csv
from pymongo import MongoClient
import pymongo
from bson.json_util import dumps
import re

import sys
sys.path.insert(0, '../secret/')
from secret.config import MongodbConfig

#app initialization
app = Flask(__name__, template_folder='templates')

# global variables for data persistence across requests
model_output=""

# If you work on local mongo compass write "local", 
# and if you work on mongo atlas write "altas" in MongodbConfig
URI = MongodbConfig("atlas")
client = pymongo.MongoClient(URI)
db = client.get_database('youtube_trends')

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

@app.route('/youtuber', methods=['GET','POST'])
def youtubers():
    youtuberList = db.youtuber_list.find(limit=100)
    if request.method == "POST":
        #youtuber search
        youtuberSearch = request.form['youtuberSearch']
        if youtuberSearch != "":
            regex = ".*".join((youtuberSearch, ".*"))
            youtuberList = db.youtuber_list.find({'ChannelInfo': re.compile(regex, re.IGNORECASE)})
    return render_template('youtuber_list.html',youtuberList=youtuberList)

@app.route('/dashboard')
def page_test():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)