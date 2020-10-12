# YOUTUBER RECOMMENDATION SYSTEM
If you are a marketing Professional and you want to do a collaboration with an influencer, you must have asked yourself how to choose any of their product that you would like to sell.

The objective of this app is to help and guide you with a choice.  You will get the possibility to review the statistics of each youtuber's channel and be able to recommend another as per the categories or featured channels of the latter.

## 1. Collecting YouTube Data
For this project, youtube api was used to get the required data that will be stored in a mongo database.  For the models, hugging face will be used, and a Flask application will be deployed to be able to access the recommendation system.

### 1.1 Getting Started with YouTube API

Use Youtube API: https://developers.google.com/youtube/v3/quickstart/python

#### Activate API from Google console
Create a New Project:
- Login to Google, if you don't have an account create one and then login.
- Visit the Google developer dashboard, create a new project from the top of the page as in below image, click “Select a project” from the top :

![Image of Youtube API -1](https://lh6.googleusercontent.com/zJ_nff9EbRY5PPHP0s7REUynxw8mfOGPieZN5LV678WjZqIWZInWiEc0ydx4hfQFESaOAX1ZMqEci-tTNKmQTbWnijQKM7U4mDb2wafsWM9MR5-UOcojA1xJizcFqzrzCL8wexV1)

- Now Click on “New Project” as in the below one and proceed.

!['Image of Youtube API - 2'](https://lh5.googleusercontent.com/BsSMME3vzQ3RL17XPnz4EoDqq-9U9SDKJB99oCfH-I3F7dv1MDnNm9qhxEr_fOhEwRimKhUPUHW940LFQD3KAeITei8BLiCSXgf9_LyMA-dTWHilpqM09We9M4SP6YU3IG137QaR)

Once done you will be automatically redirected to the Google APIs dashboard.
- The next step is to activation of YouTube API, so for that navigate to the API & Services from the side panel.
- Then click on Enable API & Services from the top of the page.
- Search for Youtube and then select YouTube Data API v3.

![Image of Youtube API - 3](https://lh4.googleusercontent.com/6782PYxnPaoQKjJi3lXzFuxU5M_-ReJRAvTabjx0NDorBMHpcaUjtEcdUC5aHcB8dIUI6GSa2cC1Wqg1rczPX6YQ6b6N86dGYs6OChEmwcZg5pxYeW1Wx51K02jBO-JKxf1VO4ds)
- After that Enable the API by clicking on the Enable as shown in the below figure.

![Image of Youtube API - 4](https://lh3.googleusercontent.com/MGEwY67Wb18AuEGXXbkFBhzs74Uxe80SbdCUWE2xC4q7-pBtyEJpKb-e_pjMulncMvSb90pSFRDPTK0XIsoVcVy2c66ZrDeJagK0IJ8BRfGw377EKao225eFyTGqt94WFpFZR7CB)
- Now again click on the API & Services and select credentials. Navigate to the Create Credentials from the top of the page in that select API key.

![Image of Youtube API - 5](https://lh5.googleusercontent.com/d6eCMY5vi8oL2eLrDdhpX0NUN8KSdUGUhUn9PAyyCJjGaw6ZfsXy0oNyHQZK8ysDEOE_eHOkpBH6znQ_gtIcfMIpRmlrgnswHKjIHnxQpex_J9kI5U9aNBhQLTwmNSgGeM4r3p95)
- Now click the file download button (Download JSON) to the right of the client ID. Finally, move the downloaded file to your working directory where is "youtube_api.py" and rename it client_secret.json.

![Image of Youtube API - 6](https://python.gotrained.com/?attachment_id=1421)

#### Prerequisites: Client Installation
Now that you have setup the credentials to access the API, you need to install the Google API client library. 

Python 2.7 or Python 3.5+ 
The pip package management tool

```python
# The Google APIs Client Library for Python
pip install --upgrade google-api-python-client
# The google-auth-oauthlib and google-auth-httplib2 libraries for user authorization
pip install --upgrade google-auth-oauthlib google-auth-httplib2
```
#### Extraction of Data from YouTube Channels
Since the Google API client is usually used to access to access all Google APIs, you need to restrict the scope the to YouTube.

When you run the script you will be presented with an authorization URL. Copy it and open it in your browser.
![Image of Google API - 1](https://i2.wp.com/python.gotrained.com/wp-content/uploads/2019/02/screenshot20.png?w=1202&ssl=1)
Select your desired account and grant your script the requested permissions. Confirm your choice.
![Image of Google API - 2](https://python.gotrained.com/?attachment_id=1431)

Copy and paste the code from the browser back in the Terminal / Command Prompt.
At this point, your script should exit successfully indicating that you have properly setup your client.

If you run the script again you will notice that a file named token.pickle is created. Once this file is created, running the script again does not launch the authorization flow.


### 1.2 Without YouTube API
Because we have a quota for Youtube API: https://developers.google.com/youtube/v3/determine_quota_cost.
The limit is 10,000 quota per day.

So we looked for a way to make requests without the API using : It's a simple script for downloading Youtube comments without using the Youtube API (https://github.com/egbertbouman/youtube-comment-downloader)

### 1.3 Create Dataset
#### Get List of top 1000 Youtubers
[Top 1000 Youtuber List](https://www.noxinfluencer.com/youtube-channel-rank/top-1000-all-all-youtuber-sorted-by-subs-weekly)

Use of Selenium and Beautiful Soup to scrape the top 1000 Youtubers avatars, Channel ids, Channel Infos, Categories, Subscribers, Avg.Views and Scores -> Scrapping/youtuber_list.py

We selected 25 of the 1000 Youtubers on the list to make API requests. 
We get the following information: profils, channelIDs, channelinfos, videoIDLists, videoIDs, videostats,comments.

#### Get list of featured channels
Use of youtube api to get featured channel of different channels.

## 2. Build model
Here we used Hugging Face for sequence classification, summarization and translation text.
- https://github.com/huggingface/transformers
- https://huggingface.co/transformers/task_summary.html

There are two models, one with API and without Youtube API.

### 2.1 Sequence Classification: 
Here we used a pipelines to do sentiment analysis: identifying if a sequence is positive or negative. It leverages a fine-tuned model on sst2, which is a GLUE task.

This returns a label (“POSITIVE” or “NEGATIVE”). 

After counting the number of elements for each label, we display the predominant result and the wordcloud for each of the labels.

### 2.2 Summarization: 
Summarization is the task of summarizing a document or an article into a shorter text.

### 2.3 Translation: 
Translation is the task of translating a text from one language to another.

We used pytube3 for collect caption tracks from youtube video: https://python-pytube.readthedocs.io/en/latest/user/quickstart.html#subtitle-caption-tracks

```python
pip install pytube3
```

## 3. Creating DataBase

### 3.1 Get Started with Atlas
https://docs.atlas.mongodb.com/getting-started/

### 3.2 Get Started with MongDB and MongoDB Compass
Create Account on [mongo](https://www.mongodb.com/) and follow instruction: https://docs.mongodb.com/compass/master/connect/

For the application, you need to get the connection string URI: https://docs.mongodb.com/manual/reference/connection-string/

- if you used MongoDB on local, your URI is like this: "mongodb://localhost:27017/[db_name]"
- if you used MongoDB Atlas, your URI is like this: mongodb+srv://[username]:[password]@[projectname]-gktww.gcp.mongodb.net/[authDB]

Use the config.py file to configure your URI settings. Do not forget to fill in the import:
```python
# Here I placed the file in a folder named "secret" 
import sys
sys.path.insert(0, '../secret/')
from secret.config import MongodbConfig
```

More informations: https://docs.mongodb.com/guides/server/drivers/

## 4. Creating graph database with Neo4j
### Working with Neo4j Desktop

**[Download link](https://neo4j.com/download-neo4j-now/?utm_source=google&utm_medium=cpc&utm_campaign=eu-search-branded&utm_adgroup=neo4j-desktop&gclid=CjwKCAjw_Y_8BRBiEiwA5MCBJiaxGCM8xIJDjxedgI_QvvhsovEjW3-UJwrSfuBkVgeUvH8vQ3NQYBoCgTAQAvD_BwE)**

**Creating a database**

- Click on the section that says Add Database: You should see two buttons appear for creating a local database or connecting to a remote dbms.
- Choose the Create a Local Database and fill in details on the entry form for your database. For the dropdown field, you can leave whatever version is defaulted. Once that is complete, click Create.
- Start your database by clicking the Start button on it.

**Importing CSV Data** : 

<img src="https://github.com/TAINGL/Youtube-Trends/tree/feature/app/helpers/neo4j_manage.png"/>

- Click on Manage
- In the Manage panel, you should see the button for Open Folder in the upper panel. Right next to that button is a dropdown arrow button. If you click that, you will see a menu of options for different folders.
- Choose the Import folder. This will open up another Finder window.
- Put the csv files in the folder

**Translate the data into nodes and relationships**

Use Cypher’s commands to create the nodes
Cypher is Neo4j’s graph query language that allows users to store and retrieve data from the graph database.

<img src="https://github.com/TAINGL/Youtube-Trends/tree/feature/app/helpers/neo4j-Browser.png"/>
<p align="center"><img width=100% src="https://github.com/Nohossat/exploradome_tangram/blob/numpy---team-4/data/imgs/logo.jpg"></p>


To enter and run Cypher statements: Click on Open Neo4j Browser, type statements into input box at top, and execute with the play button on the right.

Example of Statement to create nodes from the data found in the youtuber_list_20201006 csv:
```python
LOAD CSV WITH HEADERS FROM 'file:///youtuber_list_20201006.csv' AS youtubelist
MERGE (e:Channel {Channelid: youtubelist.Channelid, ChannelInfo: youtubelist.ChannelInfo, Category: youtubelist.Category, Subscribers: youtubelist.Subscribers})
```
<img src="https://github.com/TAINGL/Youtube-Trends/tree/feature/app/helpers/neo4j-nodes.png"/>

Example of Statement to create relationship between nodes:
```python

// Upload the CSV file on neo4j with specific content as nodes 'featureChannel'
// Verify that feature channels ids is not null
LOAD CSV WITH HEADERS FROM 'file:///featured_channels.csv' AS featureChannel
WITH featureChannel.youtuberchannelid AS Channelid, featureChannel.featuredChannelsUrls AS FeaturedChannelsUrls
WHERE FeaturedChannelsUrls IS NOT NULL
MERGE (f:FeatureChannel {Channelid:Channelid,FeaturedChannelsUrls:FeaturedChannelsUrls})

// Upload the CSV file on neo4j with specific content as nodes 'featureData'
LOAD CSV WITH HEADERS FROM 'file:///featured_channels_info.csv' AS featureData
MERGE (f:FeatureData {Channelid:  featureData.featurechannelid, Title: featureData.title})

// Select channelid from 'featureChannel' node and match it with the channelid of 'featureData'
MATCH (e:Channel { Channelid: e.Channelid })
MATCH (f:FeatureChannel { Channelid: e.Channelid })
MATCH (d:FeatureData { Channelid: f.FeaturedChannelsUrls })
// Establish the relationship
MERGE (e)-[r:KNOWS]->(f)-[h:HAVE]->(d)
RETURN e.ChannelInfo, type(r), f.FeaturedChannelsUrls, type(h), d.Title
```
<img src="https://github.com/TAINGL/Youtube-Trends/tree/feature/app/helpers/neo4j-relationship.png"/>

## 5. Run Application
### 5.1 On Local 

 ```python
export FLASK_APP=hello.py
flask run
# * Running on http://127.0.0.1:5000/
 ```
### 5.2 With Docker

From Docker-Compose
```cmd
docker-compose up
docker-compose down
```

From Dockerfile
```cmd
docker build -t <NameImage>
docker images
docker run <NameImage or ImageID>
docker stop <NameImage or ImageID>
```

From Docker Hub: https://hub.docker.com/repository/docker/taing/youtube_app
```cmd
docker pull taing/youtube_app:<LastTag>
docker images
docker run -p 5000:5000 <ImageID>
```
Running on http://0.0.0.0:5000/
