from flask import Flask, render_template, request
import csv
from pymongo import MongoClient
import pymongo
from bson.json_util import dumps
import re

#app initialization
app = Flask(__name__, template_folder='templates')

# global variables for data persistence across requests
model_output=""

try:
 client = MongoClient("mongodb+srv://youtuber:youtuber123@youtubers.ffrhx.mongodb.net/test?retryWrites=true&w=majority") #host uri
 print("Connected to Avengers MongoClient Successfully from Project Script!!!")
except:
 print("Connection to MongoClient Failed!!!")

db = client.youtube_trends

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