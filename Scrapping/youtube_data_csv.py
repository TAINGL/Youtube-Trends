# Python program to convert 
# JSON file to CSV 
  
import json 
import csv
import pandas as pd
import sys
import os

def convertChannelJsonToCsv(JsonFilename, CsvFilename):
    """
    Convert channel features json file to csv
    """
    with open(JsonFilename) as json_file: 
        data = json.load(json_file) 

    channelid = []
    featuredChannelsUrls = []
        
    for item in data:
        for i in item:
            channelid.append(i['id'])
            if 'featuredChannelsUrls' in i['brandingSettings']['channel']:
                featuredChannelsUrls.append(i['brandingSettings']['channel']['featuredChannelsUrls'])
            else:
                featuredChannelsUrls.append("")

    #Convert to dataframe
    df = pd.DataFrame(list(zip(channelid,featuredChannelsUrls)), columns =['channelid','featuredChannelsUrls'])

    #Convert list into rows
    df = df.explode('featuredChannelsUrls')

    #Save as csv
    df.to_csv(CsvFilename)

    return df


def convertFeaturesJsonToCsv(JsonFilename, CsvFilename):
    """
    Convert channel features json file to csv
    """
    channelid = []
    title = []
    description = []
    thumbnails = []
    viewCount = []
    subscriberCount = []
    Country = []

    with open(JsonFilename) as json_file: 
        data = json.load(json_file) 

    for item in data:
        for i in item:
            channelid.append(i['id'])
            title.append(i['snippet']['title'])
            description.append(i['snippet']['description'])
            thumbnails.append(i['snippet']['thumbnails']['high']['url'])
            viewCount.append(i['statistics']['viewCount'])
            subscriberCount.append(i['statistics']['subscriberCount'])
            if 'country' in i['snippet']:
                Country.append(i['snippet']['country'])
            else:
                Country.append("") 

    #Convert to dataframe
    df = pd.DataFrame(list(zip(channelid,title,description,thumbnails,viewCount,subscriberCount,Country)),columns =['channelid','title','description','thumbnails','viewCount','subscriberCount','Country'])

    #Save as csv
    df.to_csv(CsvFilename)

    return df


arguments = str(sys.argv)
# Opening JSON file and loading the data 
# into the variable data 
print(arguments)

def convertChannelDataJsonToCsv(JsonFilename):
    """
    Convert multiple channel info data to CSV
    """
    with open(JsonFilename) as json_file: 
        data = json.load(json_file)

    channelid = []
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
    commentId = []
    authorChannelId = []
    authorChannelUrl = []
    authorDisplayName = []
    authorProfileImageUrl = []
    likeCount = []
    textDisplay = []
    commentchannel_id = []
    channelvideo_id = []
    commentvideo_id = []
    categoryId = []
    #Create lists for channel_info
    for item in data['channelinfos']:
        for snip in item['items']:
            channelid.append(snip['id'])
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
    for videodata in data['videoIDLists']:
        for vidata in videodata['items']:
            if 'videoId' in vidata['id']:
                videoId.append(vidata['id']['videoId'])
            else:
                videoId.append("")
            channelvideo_id.append(vidata['snippet']['channelId'])
            video_title.append(vidata['snippet']['title'])
            video_description.append(vidata['snippet']['description'])

    #Create lists for video_stats
    for videostats in data['videostats']:
        for stats in videostats['items']:
            if 'tags' in stats['snippet']:
                video_tags.append(stats['snippet']['tags'])
            else:
                video_tags.append("")
            video_viewCount.append(stats['statistics']['viewCount'])
            video_likeCount.append(stats['statistics']['likeCount'])
            video_dislikeCount.append(stats['statistics']['dislikeCount'])
            video_commentCount.append(stats['statistics']['commentCount'])
            if 'topicDetails' in stats:
                topicCategories.append(stats['topicDetails']['topicCategories'])
            else:
                topicCategories.append("")
            video_thumbnails.append(stats['snippet']['thumbnails']['high']['url'])
            categoryId.append(stats['snippet']['categoryId'])

    #Create lists for video_comment
    for comments in data['comment']:
        for cmts in comments['items']:
            commentvideo_id.append(cmts['id'])
            commentchannel_id.append(cmts['snippet']['topLevelComment']['snippet']['videoId'])
            textDisplay.append(cmts['snippet']['topLevelComment']['snippet']['textDisplay'])
            authorDisplayName.append(cmts['snippet']['topLevelComment']['snippet']['authorDisplayName'])
            authorProfileImageUrl.append(cmts['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])
            authorChannelUrl.append(cmts['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
            if 'authorChannelId' in cmts['snippet']['topLevelComment']['snippet']:
                authorChannelId.append(cmts['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
            else:
                authorChannelId.append("")
            likeCount.append(cmts['snippet']['topLevelComment']['snippet']['likeCount'])
            commentId.append(cmts['snippet']['topLevelComment']['id'])

    #Convert lists for channel_info to dataframe
    channel_info = pd.DataFrame(list(zip(channelid,title,description,url,language,viewCount,subscriberCount)), 
                columns =['channelid','title','description','url','language','viewcount','subscribercount']) 
    #Convert lists for video_data to dataframe
    video_data = pd.DataFrame(list(zip(channelvideo_id,videoId,video_title,video_description,topicCategories,video_thumbnails,video_tags,video_commentCount,video_dislikeCount,video_likeCount,video_viewCount,categoryId)), 
                columns =['channelid','videoid','video_title','video_description','topiccategories','videothumbnails','videotags','videocommentcount','videodislikecount','videolikeCount','videoviewcount','categoryId']) 
    #Convert lists for video_comment to dataframe
    video_comment = pd.DataFrame(list(zip(commentchannel_id,commentId,authorChannelId,authorChannelUrl,authorDisplayName,authorProfileImageUrl,likeCount,textDisplay)), 
                columns =['videoid','commentid','authorchannelid','authorchannelurl','authordisplayname','authorprofileimageurl','likecount','textdisplay'])

    video_data['topiccategories'] = video_data['topiccategories'].replace(regex=True,to_replace=r'https:\/\/en\.wikipedia\.org\/wiki\/',value=r'')
    video_data['topiccategories'] = video_data['topiccategories'].replace(regex=True,to_replace=r'_\(sociology\)',value=r'')

    #Save as csv and add header if not exist
    filename='../data/channel_info.csv'
    filename1='../data/video_data.csv'
    filename2='../data/video_comment.csv'

    with open(filename, 'a') as f:
        channel_info.to_csv(f, header=f.tell()==0)

    with open(filename1, 'a') as f:
        video_data.to_csv(f, header=f.tell()==0)

    with open(filename2, 'a') as f:
        video_comment.to_csv(f, header=f.tell()==0)


if __name__ == '__main__':
    
    #Comment / Uncomment to convert multiple channel info data to CSV
    convertChannelDataJsonToCsv(sys.argv[1])

    #Comment / Uncomment to convert channel features json file to csv
    convertChannelJsonToCsv('channel_info.json','featured_channels.csv')

    #Comment / Uncomment to convert channel features json file to csv
    convertFeaturesJsonToCsv('channel_features_info.json','featured_channels_info.csv')