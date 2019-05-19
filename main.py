import praw
import queue
import re
import json
from imgur_downloader import ImgurDownloader
from urlextract import URLExtract
from time import sleep
import uuid

filename = "account_details.json"

if filename:
    with open(filename, 'r') as f:
        account_details = json.load(f)
    
reddit = praw.Reddit(client_id=account_details["client_id"],
                     client_secret=account_details["client_secret"],
                     password=account_details["password"],
                     user_agent=account_details["user_agent"],
                     username=account_details["username"])
print(f'Logged in as {reddit.user.me()}')
q = queue.Queue()
extractor = URLExtract()
table = {}
while(True):
    for submission in reddit.subreddit('mechmarket').new(limit=10):
        if(submission.id not in table):
            print(f'{submission.title} by {submission.author}')
            
            table[submission.id] = True
            q.put(submission.id)
            if(q.qsize() > 100):
                item_to_delete = q.get()
                table.pop(item_to_delete)
                
            urls = extractor.find_urls(submission.selftext)
            print(urls)
            for match in urls:
                if('imgur' in match):
                    print(match)
                    try:                        
                        ImgurDownloader(match, dir_download='F:/Timestamps', delete_dne=True).save_images()
                    except:
                        print("failed dl")
    sleep(60)
        
        

    
 