import tweepy
import json
from datetime import datetime, timezone

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

start_date = datetime.strptime('2022-12-22', '%Y-%m-%d')
end_date = datetime.strptime('2022-12-29', '%Y-%m-%d')

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
print(all_mentions)
