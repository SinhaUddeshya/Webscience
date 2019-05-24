# Collecting tweets from a user/profile but it also includes past tweets...
from pymongo import MongoClient

import tweepy
import json

#Twitter API credentials
CONSUMER_KEY = "F274aHTZLo8bV16Uyyg84u4YR"
CONSUMER_SECRET = "CfVkXSX9vlCNU3Hw6o4taoYLJp7ak455ysiWiNrVjU5woTraVf"
ACCESS_TOKEN = "1054851582511190017-BTuFbbgqcOlGdhfNY4Vdc2fPCz09kM"
ACCESS_TOKEN_SECRET = "MpgogR4p9Fatea10lNVXipzIFVCukcNX7IegTu7lfMwWD"


class TwitterHarvester(object):
    """Create a new TwitterHarvester instance"""
    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret,
                 wait_on_rate_limit=False,
                 wait_on_rate_limit_notify=False):

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.secure = True
        self.auth.set_access_token(access_token, access_token_secret)
        self.__api = tweepy.API(self.auth,
                                wait_on_rate_limit=wait_on_rate_limit,
                                wait_on_rate_limit_notify=wait_on_rate_limit_notify)
    
    @property
    def api(self):
        return self.__api

def twitter_logic():
    # instantiate an object of TwitterHarvester to use it's api object
    # make sure to set the corresponding flags as True to whether or 
    # not automatically wait for rate limits to replenish
    a = TwitterHarvester(CONSUMER_KEY, CONSUMER_SECRET, 
                         ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                         wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)
    api = a.api

    # Connecting to MongoDB database twitter_db
    conn = MongoClient('localhost', 27017)
    db = conn['twitter_db']
    #Creating a collection for storing user-based tweets
    collection = db['twitter_search5']

    # use the cursor to skip the handling of the pagination mechanism 
    # Extracting tweets from Theresa May's profile
    tweets = tweepy.Cursor(api.user_timeline, screen_name="theresa_may").items()
    while True:
        try:
            data = tweets.next()
        except StopIteration:
            break
        #Decode to JSON format
        jsoned_data = json.dumps(data._json)
        tweet = json.loads(jsoned_data)
        #Insert the tweets collected in the collection.
        collection.insert(tweet)


if __name__ == "__main__":
    #calling the function to start collecting tweets and storing them.
    twitter_logic()
    