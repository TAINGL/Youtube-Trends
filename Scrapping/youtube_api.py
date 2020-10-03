import os
import pickle
import json
import pprint
import requests
import random
import pandas as pd
import google.oauth2.credentials
 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

pp = pprint.PrettyPrinter(indent=4)

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json" # upload your own key API	

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_ID_query(service, query):
    """
    Get a video ID & channel ID with a query
    """

    request = service.search().list(
        part="snippet",
        q= query, #"Jay Chou Mojito"
        maxResults = 1 # get the first resultat => channel of Youtuber
    )
    response = request.execute()

    #pp.pprint(response)
    #pp.pprint(d['items'][0]['id']['channelId'])

    save_to_json('../data/response_from_query.json', response)
    return response

def get_videoList(service, channelId):
    """
    Search results are constrained to a maximum of 500 videos 
    if your request specifies a value for the channelId parameter
    """
    
    request = service.search().list(
        part="snippet",
        channelId= channelId, #"-biOGdYiF-I"
        maxResults = 25
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/videoList_of_channelID.json', response)
    return response

def get_video_data(service, videoId):
    """
    Get a video’s statistics data with a video ID
    """

    request = service.videos().list(
        part="id, snippet, statistics, topicDetails",
        id= videoId #"-biOGdYiF-I"
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/video_data.json', response)
    return response

def get_video_comments(service, videoId):
    """
    Get a video’s comments

    Note - maxResults: This parameter is not supported for use in conjunction with the id parameter. 
    Acceptable values are 1 to 100, inclusive. The default value is 20.
    """

    request = service.commentThreads().list(
        part="snippet",
        videoId= videoId, #"-biOGdYiF-I"
        maxResults = 50
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/video_comments.json', response)
    return response

def get_channel_info(service, channelId):
    """
    Get a channel’s information with channel ID
    """

    request = service.channels().list(
        part="snippet,statistics",
        id= channelId #"UC8CU5nVhCQIdAGrFFp4loOQ"
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/channel_info.json', response)
    return response

def get_channel_subscriptions(service, channelId):
    """
    Get a channel’s subscriptions

    The maxResults parameter specifies the maximum number of items that should be returned in the result set. 
    Acceptable values are 0 to 50, inclusive. The default value is 5.
    """

    request = service.subscriptions().list(
        part="snippet",
        id= channelId, #"UC8CU5nVhCQIdAGrFFp4loOQ"
        maxResults = 20
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/channel_subscriptions.json', response)
    return response

def get_channel_playlist(service, channelId):
    """
    Get a channel’s playlist

    The maxResults parameter specifies the maximum number of items that should be returned in the result set. 
    Acceptable values are 0 to 50, inclusive. The default value is 5.
    """

    request = service.playlists().list(
        part="snippet",
        channelId= channelId, #"UC8CU5nVhCQIdAGrFFp4loOQ"
        maxResults = 20
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/channel_playlist.json', response)
    return response

def get_channel_playlist_items(service, playlistIds):
    """
    Get a channel’s playlist

    The maxResults parameter specifies the maximum number of items that should be returned in the result set. 
    Acceptable values are 0 to 50, inclusive. The default value is 5.
    """

    request = service.playlists().list(
        part="snippet",
        id= playlistIds, #"UC8CU5nVhCQIdAGrFFp4loOQ"
        maxResults = 20
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/channel_playlist_items.json', response)
    return response


def save_to_json(files_name, files):
    """
    Save to Json files format
    """
    with open(files_name, 'w') as json_file:
        json.dump(files, json_file)
        print('Your files is saved!')


def get_profil_info(name_list):
    """
    Collect all channel ID and profil Youtuber name by query search
    """
    results = []
    profils = []
    channelIDs = []
    channelinfos = []
    #playlistIds = []
    #channelplaylists = []
    #playlist_items = [] 
    

    for i in name_list:
        result = get_ID_query(service, query= i)
        results.append(result)
        #print(results)
    
    for item in results:
        profil = item['items'][0]['snippet']['channelTitle']
        channelID = item['items'][0]['snippet']['channelId']
        profils.append(profil)
        channelIDs.append(channelID)

    for i in channelIDs:
        channelinfo = get_channel_info(service, channelId= i)
        #channelplaylist = get_channel_playlist(service, channelId= i)
        channelinfos.append(channelinfo)
        #channelplaylists.append(channelplaylist)

    #for item in channelplaylists:
    #    for ids in item['items']:
    #        playlistId = ids['id']
    #        playlistIds.append(playlistId)

    #for i in playlistIds:
    #    playlist_item = get_channel_playlist_items(service, playlistIds)
    #    playlist_items.append(playlist_item)

    # print(profils, channelIDs)        

    return profils, channelIDs, channelinfos, #channelplaylists , playlistIds, playlist_items

def get_video_info(channelIDs):

    videoIDLists = []
    videoIDs = []
    videostats = []
    comments = []
    
    for i in channelIDs:
        videoIDList = get_videoList(service, channelId= i)
        videoIDLists.append(videoIDList)
        #print(videoIDLists)

    for item in videoIDLists:
        for data in item['items']:
            try:
                videoID = data['id']['videoId']
            except:
                pass
            videoIDs.append(videoID)
        #print(videoIDs)

    for i in videoIDs:
        videostat = get_video_data(service, videoId = i)
        comment = get_video_comments(service, videoId = i)
        videostats.append(videostat)
        comments.append(comment)


    return videoIDLists, videoIDs, videostats, comments

def save_info(name_list):
    profils, channelIDs, channelinfos = get_profil_info(name_list)
    videoIDLists, videoIDs, videostats, comments = get_video_info(channelIDs)

    data={
        'profils':profils,
        'channelIDs':channelIDs,
        'channelinfos':channelinfos,
        'videoIDLists':videoIDLists,
        'videoIDs':videoIDs,
        'videostats':videostats,
        'comment':comments,
        }

    # Convert Lists to Nestings Dictionary 
    # Using list comprehension + zip() 
    # res = [{a: {b: c}} for (a, b, c, d e, f, i) in zip(profils, 
    #                                        channelIDs, 
    #                                        channelinfos, 
    #                                        videoIDLists,
    #                                        videoIDs,
    #                                        videostats,
    #                                        comments
    #                                        )] 
 

    save_to_json('../data/data_all_info.json', data)

    return data

# 1000's first Youtuber list
youtuber = pd.read_csv("../data/youtuber_list_20200930.csv")
#print(youtuber['ChannelInfo'])
youtuber_name = youtuber['ChannelInfo']
list_of_youtubers = youtuber_name.to_list()

print('List of youtubers: ', list_of_youtubers)
print('Type of listOfNames: ', type(list_of_youtubers))

# Remove spaces from list_of_youtubers
youtubers = []
for i in list_of_youtubers:
    j = i.strip()
    #Remove empty string
    if (j != ''):
        youtubers.append(j)

# Remove any duplicates from a List
print(len(youtubers))
mylist = list(dict.fromkeys(youtubers))
print(len(mylist))
#print(mylist)

# Select Random 250 youtuber names
sampling = random.choices(mylist, k=50)
# Remove any duplicates from a List
print(len(sampling))
print(sampling)
print(sampling[:10]) 
# ['Bruno Mars', 'Prince Royce', 'BeyoncéVEVO', 'CookieSwirlC', 'Lil Wayne', 'HaerteTest',
#  'Tyga', 'CNN', 'TED-Ed', 'News24']


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    #get_ID_query(service, query= "Machine Learnia")
    #get_videoList(service, 'UCmpptkXu8iIFe6kfDK5o7VQ')
    #get_video_info(['UCmpptkXu8iIFe6kfDK5o7VQ'])
    #get_video_data(service, 'EUD07IiviJg')
    #get_video_comments(service, 'EUD07IiviJg')
    #get_channel_info(service, 'UCmpptkXu8iIFe6kfDK5o7VQ')
    #get_channel_playlist(service, 'UCmpptkXu8iIFe6kfDK5o7VQ')
    #get_channel_playlist_items(service, 'PLO_fdPEVlfKoHQ3Ua2NtDL4nmynQC8YiS')
    #get_channel_subscriptions(service, 'UC0NCbj8CxzeCGIF6sODJ-7A')

    #profils, channelIDs, channelinfos, channelplaylists, playlistIds, playlist_items = get_profil_info(['Machine Learnia', 'Science4All'])
    #videoIDLists, videoIDs, videostats, comments = get_video_info(channelIDs)


    #save_info(['Bethany Mota', 'TED-Ed']) #data_all_info_1
    #save_info(['CNN']) #data_all_info_2
    #save_info(['News24']) #data_all_info_3
    #save_info(['Bruno Mars']) #data_all_info_4
    #save_info(['Gordon Ramsay']) #data_all_info_5
    #save_info(['Zoella']) #data_all_info_6
    #save_info(['David Dobrik']) #data_all_info_7
    #save_info(['Netflix']) #data_all_info_8
    #save_info(['Vogue']) #data_all_info_9
    #save_info(['Safiya Nygaard']) #data_all_info_10
    #save_info(['TEDx Talks']) #data_all_info_11
    #save_info(['The Tonight Show Starring Jimmy Fallon']) #data_all_info_12
    #save_info(['Billie Eilish']) #data_all_info_13
    #save_info(['BuzzFeedVideo']) #data_all_info_14
    #save_info(['Unbox Therapy']) #data_all_info_15
    #save_info(['nigahiga']) #data_all_info_16
    #save_info(['Kimberly Loaiza']) #data_all_info_17
    #save_info(['CarryMinati']) #data_all_info_18
    #save_info(['AuthenticGames']) #data_all_info_19
    #save_info(['Pencilmation', 'Joey Graceffa']) #data_all_info_20
    #save_info(['Matt Steffanina', 'YOLO']) #data_all_info_21
    #save_info(['Rosanna Pansino']) #data_all_info_22

    #ok-test