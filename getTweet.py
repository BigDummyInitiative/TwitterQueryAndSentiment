import tweepy
import json
from datetime import datetime, timezone
import os

rate_limit_window = 15 * 60

rate_limit = 450

request_interval = rate_limit_window / rate_limit

request_count = 0

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

start_date = datetime.strptime('2023-02-05', '%Y-%m-%d')
end_date = datetime.strptime('2023-02-11', '%Y-%m-%d')

tweets = api.search_tweets(q='pokemon', lang='en',
                           result_type="popular", tweet_mode="extended", count=10)
all_mentions = []

for tweet in tweets:
    created_at = tweet.created_at.astimezone(timezone.utc).replace(tzinfo=None)
    if created_at >= start_date and created_at < end_date:
        all_mentions.append({
            'text': tweet.full_text,
            'screen_name': tweet.user.screen_name,
            'likes_count': tweet.favorite_count,
            'retweets_count': tweet.retweet_count
        })

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy

for mention in all_mentions:
    all_max_scores = []

    tweet = mention["text"]
    tweet_words = []
   
    print(">>",tweet)

    for word in tweet.split():
        if word.startswith("@"):
                tweet_words.append("@user")
        else:
            tweet_words.append(word)

    tweet_proc = " ".join(tweet_words)

    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    max_index = numpy.argmax(scores)
    max_score = scores[max_index]
    all_max_scores.append(max_score)
        
sentiment = sum(all_max_scores) / len(all_max_scores)

if sentiment < 0.33:
    print("Negative")
elif sentiment < 0.66 > 0.33:
    print("Neutral")
else:
    print("Positive")
