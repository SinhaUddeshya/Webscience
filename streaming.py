import tweepy
import json
from pymongo import MongoClient
from pprint import pprint

#Connecting to the MongoDB database twitter_db
MONGO_HOST= 'mongodb://localhost/twitter_db'  
 
hashtags = ["Glasgow", "Brexit", "theresa may","brexitchaos"]
 
#Providing keys for OAuth
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
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
            
            #insert the data into the mongoDB into a collection called twitter_search2
            db.twitter_search2.insert(datajson)
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

