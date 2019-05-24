from lshash import LSHash
import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

store_ascii_tweets=[]
geotagged_groups={}
dictionary_group={}
HASH_SIZE=16
INPUT_DIMENSION=300
NUM_HASHTABLES=200
temp=set()
groups={}
#connecting to the mongodb database twitter_db 
MONGO_HOST= 'mongodb://localhost/twitter_db'  
client = MongoClient(MONGO_HOST)
db = client.twitter_db

lsh=LSHash(HASH_SIZE,INPUT_DIMENSION,NUM_HASHTABLES)
string_dict = {}
def append_dummy(arr):
    if len(arr)<INPUT_DIMENSION:
        for x in range(INPUT_DIMENSION-len(arr)):
            arr.append(0)

#This function takes a string and returns the ASCII value since the LSH Hash only deals with ASCII.
def conversion_to_get_ascii(string, insert):
    #stores ASCII for each tweet's Text
    global string_dict
    #stores geo-tagged tweets
    global dictionary_group
    value = [ord(c) for c in string["text"]]
    if len(value) <INPUT_DIMENSION:
       append_dummy(value)
    if insert:   
        string_dict[string["id"]] = value 
        dictionary_group[string["id"]]=string 
    return value

#This function converts the ASCII back to string.
def back_to_string(search_item):
    global string_dict
    for key, value in string_dict.items():
        if value[:INPUT_DIMENSION] == list(search_item):
            return key
    return None   

#Getting all tweets from the twitter_search3 library
temp_db_collection = db.twitter_search3.find().limit(490)
#Converting string to ASCII and storing in store_ascii_tweets.
for data in temp_db_collection:
    lsh.index(conversion_to_get_ascii(data, True))
    store_ascii_tweets.append(data)

#Formation of Groups
for data in store_ascii_tweets:
    if data["id"] not in temp:
        output=lsh.query(conversion_to_get_ascii(data, False))
        temp.add(data["id"])
        if len(output)>0:
            for value in output:
                loc=None
                tweetid= back_to_string(value[0]) 
                temp.add(tweetid)
                tweetobj=dictionary_group[tweetid] 
                if tweetobj["user"]["geo_enabled"]==True: 
                    loc=tweetobj["place"]["name"]
                    groups[loc]=len(output)
                    break
           
    if(data["user"]["geo_enabled"]==True and data["place"] is not None):
        place=data["place"]["name"]
        t=1
        if place in geotagged_groups:
            t=geotagged_groups[place]+1
        geotagged_groups[place]=t
        
        
for key,value in groups.items():
    print(key, "=",value)
#Total number of groups formed   
print('Number of groups = ', len(groups)) 

#Number of tweets per group
x=np.zeros(len(groups))
y=np.zeros(len(groups))
i=0
fig=plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel("Group of Tweets")
ax1.set_ylabel("Total tweets in each group")
ax1.set_title("Number of tweets in each group")
for key,value in groups.items():
    x[i]=i
    print("location= ",key," index=", i)
    y[i]=value
    i+=1
#Graph to show number of tweets per group
ax1.plot(x,y)
plt.show()