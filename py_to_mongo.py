import pymongo
import praw
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["rdb"]

mycol = mydb["rd_data"]

record = []

reddit = praw.Reddit(client_id='###########', 
                     client_secret='#######', 
                     user_agent='#########', 
                     username='#########',  
                     password='######')

flair_type = ["Reddiquette","Policy","Politics","AskIndia","Non-Political"]
subreddit = reddit.subreddit('india')
records_dict = {"flair":[], "title":[], "id":[], "url":[], "created": [], "body":[], "comments":[]}

for flair in flair_type:
  
  get_subreddits = subreddit.search(flair, limit=10)
  
  for x in get_subreddits:
    
    records_dict["flair"].append(flair)
    records_dict["title"].append(x.title)
    records_dict["id"].append(x.id)
    records_dict["url"].append(x.url)
    records_dict["created"].append(x.created)
    records_dict["body"].append(x.selftext)
    
    x.comments.replace_more(limit=None)
    comment = ''
    for top_level_comment in x.comments:
      comment = comment + ' ' + top_level_comment.body
    records_dict["comments"].append(comment)

#inseting data in database
temp = mycol.insert_one(records_dict)
