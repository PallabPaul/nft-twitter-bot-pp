import time
import sys
import tweepy
# from dotenv import load_dotenv
from random import randint
from list_of_tweets import status_arr, hashtag_arr, comment_arr

# load_dotenv()

# from credentials import *  # use this one for testing

# use this for production; set vars in heroku dashboard
from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

INTERVAL = 60 * 60 * 1  # tweet every 6 hours
# INTERVAL = 5  # every 15 seconds, for testing

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def generate_status(prev_status_index):

    status_index = randint(0,len(status_arr)-1)

    while prev_status_index == status_index:
        status_index = randint(0,len(status_arr)-1)
    
    status = status_arr[status_index]+" "+hashtag_arr[randint(0,len(hashtag_arr)-1)]
    return status,status_index if len(status) <= 140 else generate_status(prev_status_index)

def get_random_media_file():
    png_filename = "./images/{}.png".format(randint(1,19))
    gif_filename = "./images/1.gif"
    return gif_filename if randint(1,5) == 5 else png_filename

# results = api.search_tweets(q="NFT")

# for result in results:
#     print (result.text)
count = 1
status_index = -1
while True:
    print("updating status # {}".format(count))
    status,status_index = generate_status(status_index)
    print(status)
    media_or_not = randint(1,4)
    if media_or_not == 4:
        api.update_status(status)
    else:
        api.update_status_with_media(status, get_random_media_file())
    count += 1
    time.sleep(INTERVAL)