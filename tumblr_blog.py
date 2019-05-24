import pytumblr
import json
from pymongo import MongoClient

# Connecting to the Tumblr database
MONGO_HOST= 'mongodb://localhost/tumblr_db'
# Make the request
client = pytumblr.TumblrRestClient('8dNjRe7UGCRSHZMHRJY2Bc9cOcNvtOpyCkntJGfAKYGGLsG897')

client2 = MongoClient(MONGO_HOST)

db = client2.tumblr_db
'''Here, 20 posts from the blog "Probably Angry Politics are being collected. Offset value is given to retrieve older posts as well
since only the 20 most recent posts can be extracted by default. The reblog_info and notes_info is set to true which means the posts 
collected also gives information about the number of times the blog was reblogged and the number of notes it received.'''
blog_posts = client.posts('probablyangypolitics.tumblr.com',offset=80,reblog_info=True, notes_info=True)
#Decode the JSON
str1 = json.dumps(blog_posts)
datajson = json.loads(str1)
##inserting the collected documents to the collection: tumblr_blog
db.tumblr_blog.insert(datajson)