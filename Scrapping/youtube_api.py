import os
import pickle
import json
import pprint
import requests
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

def get_videoList(service, channelIDs):
    """
    Search results are constrained to a maximum of 500 videos 
    if your request specifies a value for the channelId parameter
    """
    
    request = service.search().list(
        part="snippet",
        channelId= channelIDs, #"-biOGdYiF-I"
        maxResults = 50
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/videoList_of_channelID.json', response)

def get_video_data(service, videoId):
    """
    Get a video’s statistics data with a video ID
    """

    request = service.videos().list(
        part="statistics",
        id= videoId #"-biOGdYiF-I"
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/video_data.json', response)

def get_video_comments(service, videoId):
    """
    Get a video’s comments
    """

    request = service.commentThreads().list(
        part="snippet",
        videoId= videoId #"-biOGdYiF-I"
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/video_comments.json', response)

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

def get_channel_playlist(service, channelId):
    """
    Get a channel’s playlist
    """

    request = service.playlists().list(
        part="snippet",
        channelId= channelId #"UC8CU5nVhCQIdAGrFFp4loOQ"
    )
    response = request.execute()

    pp.pprint(response)

    save_to_json('../data/channel_playlist.json', response)

def save_to_json(files_name, files):
    """
    Save to Json files format
    """
    with open(files_name, 'w') as json_file:
        json.dump(files, json_file)
        print('Your files is saved!')


def get_profil_Info(name_list):
    """
    Collect all channel ID and profil Youtuber name by query search
    """
    results = []
    profils = []
    channelIDs = []
    

    for i in name_list:
        result = get_ID_query(service, query= i)
        results.append(result)
        #print(results)
    
    for item in results:
        profil = item['items'][0]['snippet']['channelTitle']
        channelID = item['items'][0]['snippet']['channelId']
        profils.append(profil)
        channelIDs.append(channelID)

    # print(profils, channelIDs)        

    return profils, channelIDs

def get_video_info(channelIDs):

    videoIDLists = []
    videoIDs = []
    
    for i in channelIDs:
        videoIDList = get_videoList(service, channelIDs= i)
        videoIDLists.append(videoIDList)
        print(videoIDLists)

    for item in videoIDLists:
        for nbr in range(len(item['items'])-2): # because last video doesn't have "videoId"
            videoID = item['items']['id'][nbr]['videoId']
            videoIDs.append(videoID)

    return videoIDs

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    #get_ID_query(service, query= "Machine Learnia")
    #get_videoList(service, 'UCmpptkXu8iIFe6kfDK5o7VQ')

    #profils, channelIDs = get_profil_Info(['Machine Learnia']) # , 'Science4All'
    #get_video_info(channelIDs)

