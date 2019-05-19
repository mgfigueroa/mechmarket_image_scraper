import praw
import json

class RedditApi:
    def __init__(self, filename):
        if filename:
            with open(filename, 'r') as f:
                account_details = json.load(f)
    
        self.reddit_api = praw.Reddit(client_id=account_details["client_id"],
                            client_secret=account_details["client_secret"],
                            password=account_details["password"],
                            user_agent=account_details["user_agent"],
                            username=account_details["username"])

    def GetNewSubmissions(self, limit=10):
        return self.reddit_api.subreddit('mechmarket').new(limit=10)

    def GetUsername(self):
        return self.reddit_api.user.me()