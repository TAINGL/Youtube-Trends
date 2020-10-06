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
CLIENT_SECRETS_FILE = "/Users/oorvasisooprayen/Desktop/Youtube-Trends/Scrapping/client_secret.json" # upload your own key API	

API = "AIzaSyDo1lUE_k9FZiXHScOl5yFDjHrb9tufBcg"
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

def get_channel_features(service, channelIds, part):
    """
    Get Channel info with channel features with part
    """

    request = service.channels().list(
        part=part,
        id= channelIds
    )
    response = request.execute()
    return response


def save_to_json(files_name, files):
    """
    Save to Json files format
    """
    with open(files_name, 'w') as json_file:
        json.dump(files, json_file)
        print('Your files is saved!')


def get_features_info(list_of_Channelids, rangeLength, part, filename):
    """
    Collect all channel features
    """
    Allfeatures = []

    for i in range(0, rangeLength):
        chunks = [list_of_Channelids[x:x+50] for x in range(0, len(list_of_Channelids), 50)][i]
        print(len(chunks))
        features = get_channel_features(service, chunks,part)
        Allfeatures.append(features['items'])
        i+=1
    
    save_to_json(filename, Allfeatures)

    return Allfeatures

def getChannelIds():
    """
    Get the list of channel ids
    """
    # 1000's first Youtuber list
    youtuber = pd.read_csv("data/youtuber_list_20201006.csv")
    Channelid = youtuber['Channelid']

    # Convert column to list
    list_of_Channelids = Channelid.to_list()
    return list_of_Channelids

def getChannelFeatureIds():
    """
    Get the list of channel features ids
    """
    youtuber = pd.read_csv("data/featured_channels.csv")
    featuredChannels = youtuber['featuredChannelsUrls'].to_list()
    featuredChannels = list(dict.fromkeys(featuredChannels))

    return featuredChannels


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    #Comment / Uncomment to get channels data
    #get_features_info(getChannelIds(), 19, 'brandingSettings','channels_data.json')
    get_features_info(getChannelFeatureIds(), 91, 'snippet,statistics','channels_features_data.json')