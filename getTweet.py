import tweepy
import time
import pandas as pd
from pandas import DataFrame
import json
from datetime import datetime

api_key = 'tZynA4YovEjcErk7VzxiTYfH3'
api_secret = 'n5cC4ufuSFUpFwBqAN42AmxFCxtL4VYVEh7n7p3i5319wYiFN5'

callback_uri = 'oob'
auth = tweepy.OAuthHandler(api_key, api_secret, callback_uri)
redirect_url = auth.get_authorization_url()
print(redirect_url)

user_pin = input('Provide your user pin from the link: ')
user_pin

auth.get_access_token(user_pin)
api = tweepy.API(auth)

tweets_3_months = api.search_full_archive(label='dev',
                                          query='@TO_WinterOps',
                                          fromDate="202201010000",
                                          toDate="202203310000",
                                          maxResults=100
                                          )

min_date = (str(tweets_3_months[-1].created_at)[0:10]).replace('-', '')+'0000'

all_mentions = []
all_mentions.extend(tweets_3_months)
while True:
    tweets_3_months = api.search_full_archive(label='dev',
                                              query='@TO_WinterOps',
                                              fromDate="202201010000",
                                              toDate=min_date,
                                              maxResults=100
                                              )
    if len(tweets_3_months) == 0:
        break

    min_date = (str(tweets_3_months[-1].created_at)
                [0:10]).replace('-', '')+'0000'
    print(min_date)
    all_mentions.extend(tweets_3_months)
    print('Number of tweets in all_mentions dataframe: {}'.format(len(all_mentions)))

    mentions_tweets = [[info.id,
                        info.created_at,
                        info.favorite_count,
                        info.retweet_count,
                        info.text.encode("utf-8").decode("utf-8"),
                        info.entities,
                        info.user.screen_name]
                       for idx, info in enumerate(all_mentions)]
mentions_df = DataFrame(mentions_tweets, columns=[
                        "id", "created_at", "favorite_count", "retweet_count", "text", "entities", "screen_name"])
mentions_df.head()
