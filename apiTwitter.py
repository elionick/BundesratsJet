from itertools import count
from os import access
import tweepy
from env_vars import *

# access_key = "hQAKOdouVEDDROoXFs30nABUm"
# access_secret = "PnB15dZIRy2pVyBeAY2n3csU4c2USFzYKT73f9snZHLosnbl7Q"
# consumer_key = "1578508197941444611-l8hvW3GOXeDXJixnIqQQIH4lVm6fjm"
# consumer_secret = "aCceXsTIsBJZpyOGpb0Gj7mosk8GeBKSmJlvSM5XhMnBg"

def update_Twitter_status(status):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(apiTwitter_access_key, apiTwitter_access_secret)
    auth.set_access_token(api_Twitter_consumer_key, apiTwitter_consumer_secret)

    #api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    response = api.update_status(status)

    print(response)