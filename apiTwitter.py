from itertools import count
from os import access
import tweepy
from env_vars import *
import time
import datetime

def update_Twitter_status(status):
    # Authenticate to Twitter

    auth = tweepy.OAuthHandler(apiTwitter_access_key, apiTwitter_access_secret)
    auth.set_access_token(api_Twitter_consumer_key, apiTwitter_consumer_secret)

    #api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    response = api.update_status(status)

    print(response)

def upload_Twitter_status_with_media(icao, timestamp, flight_index, airports):

    time.sleep(86400)
    api_key = apiTwitter_access_key
    api_secret = apiTwitter_access_secret
    #bearer_token = apiTwitter_bearer_token
    acces_token = api_Twitter_consumer_key
    access_token_secret = apiTwitter_consumer_secret

    # For 2.0 endpoints
    api_2 = tweepy.Client(consumer_key=api_key, consumer_secret=api_secret, access_token=acces_token, access_token_secret=access_token_secret)

    # For 1.1 endpoints
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, acces_token, access_token_secret)
    api = tweepy.API(auth)


    dt_object = datetime.datetime.fromtimestamp(timestamp)
    date = dt_object.date()

    try:
        if icao == '4b7f4c':
            status_icao = f'On {date}, the Falcon 900EX has flown from {airports[0][0]}, {airports[0][1]} to {airports[1][0]}, {airports[1][1]} using the following route:'
        elif icao == '4b7fd4':
            status_icao = f'On {date}, the Citation Excel has flown from {airports[0][0]}, {airports[0][1]} to {airports[1][0]}, {airports[1][1]} using the following route:'
        else:
            status_icao = f'TEST: On {date}, airplane {icao} has flown from {airports[0][0]}, {airports[0][1]} to {airports[1][0]}, {airports[1][1]} using the following route:'
    except Exception as error:
        print(error)

    try:
        print('Uploading media...')
        filename = os.path.join(os.getcwd(), '/media', f'flight_{icao}-{flight_index}.png')
        #filename = f'media/flight_{icao}-{flight_index}.png'
        upload = api.simple_upload(filename=filename)

        print('Tweeting...')
        api_2.create_tweet(text=status_icao, media_ids=[upload.media_id])
        # Depreceated
        # api.update_status(status=status_icao, media_ids=[upload.media_id])
    except Exception as error:
        print(f'An error has occured while trying to post to Twitter: {error}')