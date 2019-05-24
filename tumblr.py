'''This program extracts posts from Tumblr based on keywords. However Tumblr
  does not allow developers to fetch real-time data.
'''

import pytumblr
import json
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt

# Connecting to the Tumblr database
MONGO_HOST= 'mongodb://localhost/tumblr_db'
# Make the request
client = pytumblr.TumblrRestClient(
  API KEYS
)


client2 = MongoClient(MONGO_HOST)
            
            
db = client2.tumblr_db
'''Because of tumblr restrictions, only one keyword can be used at a time to gather posts
Here, I have used 4 Keywords to gather the posts - "brexit", "stop brexit", "theresa may", "glasgow"
Another restriction is that at once only 20 most recent posts will be retrieved so I used the before
parameter to get posts before the last collected post using timestamps.
Limit parameter determines the number of posts to be collected and could be any value between 0-20. 
The before parameter collects 20 posts before the timestamp provided.
'''
#data1 = client.tagged('brexit', limit=20)
#data2 = client.tagged('stop brexit', limit=20)
#data3 = client.tagged('theresa may', limit=20)
#Here, 20 posts having glasgow as a tag are being collected before the specified timestamp.
data = client.tagged('glasgow', before=1541985878, limit=20)
#Decoding JSON
str1 = json.dumps(data)
datajson = json.loads(str1)
#inserting the collected documents to the collection: tumblr_search1
db.tumblr_search1.insert(datajson)
#printing total number of posts collected
print(db.tumblr_search1.count())
#printing total number of posts collected with the keyword Glasgow
print(db.tumblr_search1.find({"tags": { "$eq":"Glasgow" }}).count())
'''printing total number of posts that have atleast one note. Notes are the sum of likes and reblogs on
a Tumblr post'''
print(db.tumblr_search1.find({"note_count":{"$ne":0}}).count())
'''A Tumblr post could be either a text, photo, video, link, quote, chat or an audio
printing the number of text posts'''
print("Number of text posts:")
t1 = db.tumblr_search1.find({"type":{"$eq":"text"}}).count()
print(t1)
#printing the number of photo posts
print("Number of photo posts:")
t2 = db.tumblr_search1.find({"type":{"$eq":"photo"}}).count()
print(t2)
#printing the number of video posts
print("Number of video posts:")
t3 = db.tumblr_search1.find({"type":{"$eq":"video"}}).count()
print(t3)
#printing the number of link posts
print("Number of link posts:")
t4 = db.tumblr_search1.find({"type":{"$eq":"link"}}).count()
print(t4)
#printing the number of quote posts
print("Number of quote posts:")
t5 = db.tumblr_search1.find({"type":{"$eq":"quote"}}).count()
print(t5)
#printing the number of chat posts
print("Number of chat posts:")
t6 = db.tumblr_search1.find({"type":{"$eq":"chat"}}).count()
print(t6)
#printing the number of audio posts
print("Number of audio posts:")
t7 = db.tumblr_search1.find({"type":{"$eq":"audio"}}).count()
print(t7)

x = np.array([t1,t2,t3,t4,t5,t6,t7])
y = np.array(["Text","photo","video","link","quote","chat","audio"])

#Plotting the total amount of data collected vs type of data collected.
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.set_title("Type of posts collected vs amount of posts collected")
ax.set_xlabel("Type of posts collected")
ax.set_ylabel("Number of posts collected")
plt.plot(y,x,marker="o",markersize=10)
plt.show()
