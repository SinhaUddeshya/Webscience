import tweepy
import json
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
from pprint import pprint

#Connecting to the database
MONGO_HOST= 'mongodb://localhost/twitter_db'  
 
CONSUMER_KEY = "F274aHTZLo8bV16Uyyg84u4YR"
CONSUMER_SECRET = "CfVkXSX9vlCNU3Hw6o4taoYLJp7ak455ysiWiNrVjU5woTraVf"
ACCESS_TOKEN = "1054851582511190017-BTuFbbgqcOlGdhfNY4Vdc2fPCz09kM"
ACCESS_TOKEN_SECRET = "MpgogR4p9Fatea10lNVXipzIFVCukcNX7IegTu7lfMwWD"
#Restricting to collect only tweets posted in English.
language = ['en']
 
 
class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 
 
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #This connects to the database and stores all the tweets collected in the mongodb collection
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.twitter_db
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            username = datajson['user']['screen_name']
            text = datajson['text']
            
            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']
 
            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
            
            #insert the data into the mongoDB into a collection called twitter_search3
            db.twitter_search3.insert(datajson)
            print(username + ':' + ' ' + text)
        except Exception as e:
           print(e)
# Providing the bounding box to filter tweets from Glasgow and its surroundings
LOCATIONS = [-4.3932, 55.7, -4.24, 55.9212]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
'''Set up the listener. 
The 'wait_on_rate_limit=True' waits for some time when rate limit is reached for the authenticating user'''
listener = StreamListener(api=tweepy.API(retry_count=3, retry_delay=5, wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: ")
streamer.filter(languages = language, locations = LOCATIONS)
