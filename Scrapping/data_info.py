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
videoId = []
video_title = []
video_description = []
topicCategories = []
video_thumbnails = []
video_tags = []
video_commentCount = []
video_dislikeCount = []
video_likeCount = []
video_viewCount = []
commentvideo_id = []
commentId = []
authorChannelId = []
authorChannelUrl = []
authorDisplayName = []
authorProfileImageUrl = []
likeCount = []
textDisplay = []

#Create lists for channel_info
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

# Create lists for video_data
for videos in data['videoIDLists']:
    for vids in videos['items']:
        if 'videoId' in vids['id']:
            videoId.append(vids['id']['videoId'])
        else:
            videoId.append("")
        video_title.append(vids['snippet']['title'])
        video_description.append(vids['snippet']['description'])

#Create lists for video_data
for videos in data['videostats']:
    for vids in videos['items']:
        if 'tags' in vids['snippet']:
            video_tags.append(vids['snippet']['tags'])
        else:
            video_tags.append("")
        video_viewCount.append(vids['statistics']['viewCount'])
        video_likeCount.append(vids['statistics']['likeCount'])
        video_dislikeCount.append(vids['statistics']['dislikeCount'])
        video_commentCount.append(vids['statistics']['commentCount'])
        if 'topicDetails' in vids:
            topicCategories.append(vids['topicDetails']['topicCategories'])
        else:
            topicCategories.append("")
        video_thumbnails.append(vids['snippet']['thumbnails']['high']['url'])

#reate lists for video_comment
for videos in data['comment']:
    for vids in videos['items']:
        commentvideo_id.append(vids['snippet']['topLevelComment']['snippet']['videoId'])
        textDisplay.append(vids['snippet']['topLevelComment']['snippet']['textDisplay'])
        authorDisplayName.append(vids['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        authorProfileImageUrl.append(vids['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])
        authorChannelUrl.append(vids['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
        if 'authorChannelId' in vids['snippet']['topLevelComment']['snippet']:
            authorChannelId.append(vids['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
        else:
            authorChannelId.append("")
        likeCount.append(vids['snippet']['topLevelComment']['snippet']['likeCount'])
        commentId.append(vids['snippet']['topLevelComment']['id'])

#Convert lists for channel_info to dataframe
channel_info = pd.DataFrame(list(zip(_id,title,description,url,language,viewCount,subscriberCount,videoId)), 
               columns =['channelid','title','description','url','language','viewcount','subscribercount','videoid']) 
#Convert lists for video_data to dataframe
video_data = pd.DataFrame(list(zip(_id,videoId,video_title,video_description,topicCategories,video_thumbnails,video_tags,video_commentCount,video_dislikeCount,video_likeCount,video_viewCount,commentvideo_id,commentId)), 
               columns =['channelid','videoid','video_title','video_description','topiccategories','videothumbnails','videotags','videocommentcount','videodislikecount','videolikeCount','videoviewcount','commentvideoid','commentid']) 
#Convert lists for video_comment to dataframe
video_comment = pd.DataFrame(list(zip(_id,videoId,commentvideo_id,commentId,authorChannelId,authorChannelUrl,authorDisplayName,authorProfileImageUrl,likeCount,textDisplay)), 
               columns =['channelid','videoid','commentvideoid','commentid','authorchannelid','authorchannelurl','authordisplayname','authorprofileimageurl','likecount','textdisplay']) 

#Save as csv and add header if not exist
filename='channel_info.csv'
filename1='video_data.csv'
filename2='video_comment.csv'

with open(filename, 'a') as f:
    channel_info.to_csv(f, header=f.tell()==0)

with open(filename1, 'a') as f:
    video_data.to_csv(f, header=f.tell()==0)

with open(filename2, 'a') as f:
    video_comment.to_csv(f, header=f.tell()==0)