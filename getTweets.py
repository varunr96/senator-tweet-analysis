import tweepy
from tweepy import OAuthHandler
import json
import re

consumer_key = 'jHtpxFPXLdFYjo1v4GUQQBFA4'
consumer_secret = 'mxYbUQMq0UtdIMpDcqX9cuCcZqmi2wHU4CXb3bBXl5RGl9w8aT'
access_token = '167688459-pMTFKjvnY3ter9y8PP5qAai5Dj1JuFNPE4s08C7q'
access_secret = 'Ipjtt9MpjlJCIbxvIStUkQamaS6XMS84DCEdEkcnXSro3'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

senators = set()
filename = 'senators.txt'
f = open(filename, 'r')
for line in f:
	senators.add(line.rstrip('\n'))

f.close()

all_tweets = dict.fromkeys(senators, [])
all_num_tweets = {}
num_tweets = 0

for senator in senators:
	all_tweets[senator] = []

for senator in senators:
	page = 1
	num_tweets = 0
	while True:
		print("{}'s page #{}...".format(senator, page))
		statuses = api.user_timeline(senator, page=page, tweet_mode='extended')
		if statuses:
			for status in statuses:
				tweet = {}
				tweet['date'] = '{:%B %d, %Y}'.format(status.created_at)
				clean_text = re.sub(r"http\S+", "", status.full_text)
				clean_text = clean_text.encode('ascii', 'ignore').decode("utf-8")
				clean_text = clean_text.replace('\"', '')
				clean_text = clean_text.replace('\n', ' ')
				tweet['text'] = clean_text
				all_tweets[senator].append(tweet)
				num_tweets += 1
		else:
			print('{}: scrapped {} tweets!'.format(senator, num_tweets))
			all_num_tweets[senator] = num_tweets
			break
		page += 1

json_data = json.dumps(all_tweets, indent=4)
f = open('tweets.json', 'w')
f.write(json_data)
f.close()

f = open('num_tweets.txt', 'w')
for senator in senators:
	f.write("{} {}".format(senator, all_num_tweets[senator]))
f.close()