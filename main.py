import queue
import re
from imgur_downloader import ImgurDownloader
from urlextract import URLExtract
from time import sleep
from RedditApi import RedditApi

filename = "account_details.json"
reddit_api = RedditApi(filename=filename)

print(f'Logged in as {reddit_api.GetUsername()}')
q = queue.Queue()
extractor = URLExtract()
table = {}
while(True):
    for submission in reddit_api.GetNewSubmissions():
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
        
        

    
 