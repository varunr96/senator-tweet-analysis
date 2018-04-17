import tweepy
from tweepy import OAuthHandler
import json, re

# Your own keys and tokens based off your Twitter Account
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Using twitter API
# wait_on_rate_limit=True so it automatically waits
api = tweepy.API(auth, wait_on_rate_limit=True)

# Adding all Senator Twitter handles to set
senators = set()
filename = 'senators.txt'
f = open(filename, 'r')
for line in f:
	senators.add(line.rstrip('\n'))

f.close()

# all tweets needed to create output json
all_tweets = dict.fromkeys(senators, [])
# all num_tweets is checking on our side
all_num_tweets = {}
num_tweets = 0

for senator in senators:
	all_tweets[senator] = []

# Algorithm
for senator in senators:
	page = 1
	num_tweets = 0
	while True:
		print("{}'s page #{}...".format(senator, page))
		# Obtaining latest 3200 tweets from a user
		statuses = api.user_timeline(senator, page=page, tweet_mode='extended')
		if statuses:
			for status in statuses:
				# cleaning tweet for things we don't care about
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

# writing json file
json_data = json.dumps(all_tweets, indent=4)
f = open('tweets.json', 'w')
f.write(json_data)
f.close()

# writing file for our sanity check
f = open('num_tweets.txt', 'w')
for senator in senators:
	f.write("{} {}".format(senator, all_num_tweets[senator]))
f.close()
