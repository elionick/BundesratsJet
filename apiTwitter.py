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