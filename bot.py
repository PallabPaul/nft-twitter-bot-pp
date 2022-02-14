import time
import sys
import tweepy
from random import randint
from os import environ
from list_of_tweets import status_arr, hashtag_arr, comment_arr
# from dotenv import load_dotenv
# load_dotenv()

class TwitterBot:

    def __init__(self):

        CONSUMER_KEY = environ['CONSUMER_KEY']
        CONSUMER_SECRET = environ['CONSUMER_SECRET']
        ACCESS_KEY = environ['ACCESS_KEY']
        ACCESS_SECRET = environ['ACCESS_SECRET']

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

        self.api = tweepy.API(auth)

        self.INTERVAL = 60 * 30

        self.prev_status_index = -1

        self.status_count = 1
        self.comment_count = 1

        self.last_post_id = 0

    def generate_status(self,is_comment=False):

        sentence_arr = comment_arr if is_comment else status_arr

        status_index = randint(0,len(sentence_arr)-1)

        while self.prev_status_index == status_index:
            status_index = randint(0,len(sentence_arr)-1)
        
        status = sentence_arr[status_index]+" "+hashtag_arr[randint(0,len(hashtag_arr)-1)]
        return status if len(status) <= 140 else self.generate_status(is_comment)

    def get_random_media_file(self):

        png_filename = "./images/{}.png".format(randint(1,19))
        gif_filename = "./images/1.gif"
        return gif_filename if randint(1,5) == 5 else png_filename

    def send_tweet(self,is_comment=False,id=None,name=None):

        status = self.generate_status(is_comment)
    
        if is_comment:
            status = "@"+name+" "+status

        media_or_not = randint(1,4)
        if media_or_not == 4 and not is_comment:
            self.api.update_status(status, in_reply_to_status_id=id)
        else:
            self.api.update_status_with_media(status, self.get_random_media_file(), in_reply_to_status_id=id)
        

    def tweet_a_status(self):

        print("Updating status # {}".format(self.status_count))
        self.send_tweet()
        self.status_count += 1

    def query_tweets(self):
        
        results = self.api.search_tweets(
            q="(NFT AND DROP AND YOUR) OR (NFT AND DROP AND YOUR AND BUYING) -ETH",
            count=15,
            since_id=self.last_post_id)

        id_name_dict = {}

        for result in results:
            if (result.text[:2]) == "RT":
                result = result.retweeted_status
            id_name_dict[result.id] = result.user.screen_name

        if id_name_dict:
            self.last_post_id = max(id_name_dict.keys())
        
        return id_name_dict

    def tweet_comments(self):

        tweet_dict = self.query_tweets()
        if tweet_dict:
            for id, name in tweet_dict.items():
                print("Commenting on tweet # {}".format(self.comment_count))
                self.send_tweet(True,id,name)
                self.comment_count += 1
                time.sleep(90)

    def start_bot(self):

        while True:
            self.tweet_a_status()
            time.sleep(self.INTERVAL)
            self.tweet_comments()
            time.sleep(self.INTERVAL)
            self.tweet_comments()
            time.sleep(self.INTERVAL)

if __name__ == '__main__':
     bot = TwitterBot()
     print("Starting bot...")
     bot.start_bot()