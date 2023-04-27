from itertools import count
from os import access
import tweepy
from env_vars import *

def update_Twitter_status(status):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(apiTwitter_access_key, apiTwitter_access_secret)
    auth.set_access_token(api_Twitter_consumer_key, apiTwitter_consumer_secret)

    #api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    response = api.update_status(status)

    print(response)

def upload_Twitter_status_with_media(icao, flight_index, airports):

    api_key = apiTwitter_access_key
    api_secret = apiTwitter_access_secret
    #bearer_token = apiTwitter_bearer_token
    acces_token = api_Twitter_consumer_key
    access_token_secret = apiTwitter_consumer_secret

    # For 2.0 End-points, currently not needed
    # client = tweepy.Client(bearer_token, api_key, api_secret, acces_token, access_token_secret)

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, acces_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        if icao == '4b7f4c':
            status_icao = f'The Falcon 900EX has flown from {airports[0][0]}, {airports[0][1]} to {airports[1][0]}, {airports[1][1]} using the following route:'
        elif icao == '4b7fd4':
            status_icao = f'The Citation Excel has flown from {airports[0][0]}, {airports[0][1]} to {airports[1][0]}, {airports[1][1]} using the following route:'
        else:
            status_icao = f'Airplane {icao} has flown from {airports[0][0]}, {airports[0][1]} to {airports[1][0]}, {airports[1][1]} using the following route:'
    except Exception as error:
        print(error)

    try:
        print('Uploading media...')
        filename = os.path.join(os.getcwd(), '/media', f'flight_{icao}-{flight_index}.png')
        #filename = f'media/flight_{icao}-{flight_index}.png'
        upload = api.simple_upload(filename=filename)

        print('Tweeting...')
        api.update_status(status=status_icao, media_ids=[upload.media_id])
    except Exception as error:
        print(f'An error has occured while trying to post to Twitter: {error}')