import tweepy
import json
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

#connecting to the mongodb database twitter_db 
MONGO_HOST= 'mongodb://localhost/twitter_db'  
                                             
#gathering tweets containing the keyword "." in it.
hashtags = ["."] 

#declaring keys for OAuth 
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
            
            # Use twitterdb database.
            db = client.twitter_db
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            #To get the user who printed the tweet
            username = datajson['user']['screen_name']
            #To get the actual text of tweet collected
            text = datajson['text']
            
            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']
 
            #print out a message to the screen that we have collected a tweet along we the time of collection of the tweets.
            print("Tweet collected at " + str(created_at))
            
            #insert the data into the mongoDB into a collection called twitter_search1
            db.twitter_search1.insert(datajson)
            print(username + ':' + ' ' + text)
        except Exception as e:
           print(e)
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
'''Set up the listener. 
The 'wait_on_rate_limit=True' waits for some time when rate limit is reached for the authenticating user'''
listener = StreamListener(api=tweepy.API(retry_count=3, retry_delay=5, wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(hashtags))
#Tracking starts based on the keyword and the second arguement restricts the tweets collected to be in english.
streamer.filter(track=hashtags,languages = language)
