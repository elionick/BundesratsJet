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

def upload_Twitter_status_with_media(icao, flight_index):

    api_key = apiTwitter_access_key
    api_secret = apiTwitter_access_secret
    #bearer_token = apiTwitter_bearer_token
    acces_token = api_Twitter_consumer_key
    access_token_secret = apiTwitter_consumer_secret

    # For 2.0 End-points, currently not needed
    # client = tweepy.Client(bearer_token, api_key, api_secret, acces_token, access_token_secret)

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, acces_token, access_token_secret)
    api = tweepy.API(auth)

    filename = f'media/flight_{icao}-{flight_index}.png'
    upload = api.simple_upload(filename=filename)

    api.update_status(status=f'Flight {icao} has flown the following route:', media_ids=[upload.media_id])

    # client.create_tweet(text='Hello Twitter')

    # Upload image on it's own to twitter by using "simple_upload"

    #upload = api.simple_upload(filename='flight_3E175B-1.png')

    # Get update.media_id

    # Include Media ID in status update as a list

    #api.update_status(status='This is a test tweet with an image', media_ids=['1647695799738875906'])


    # upload = api.simple_upload(filename='map.png')

    # id = upload.media_id

    # api.update_status(status='another test, trying out HTML', media_ids=[id])


    # client.create_tweet(in_reply_to_tweet_id=1647692196932464642, text='HellO user')
    
    
    
    
    
    
    # # Authenticate to Twitter
    # auth = tweepy.OAuthHandler(apiTwitter_access_key, apiTwitter_access_secret)
    # auth.set_access_token(api_Twitter_consumer_key, apiTwitter_consumer_secret)

    # #api = tweepy.API(auth)
    # api = tweepy.API(auth, wait_on_rate_limit=True)

    # api.update_status_with_media(status = 'Test', filename=map_path)













# def new_update_Twitter_status(status):

#     auth = tweepy.OAuthHandler(apiTwitter_access_key, apiTwitter_access_secret)
#     auth.set_access_token(api_Twitter_consumer_key, apiTwitter_consumer_secret)

#     #api = tweepy.API(auth)
#     api = tweepy.API(auth, wait_on_rate_limit=True)

#     api.create_tweet()

