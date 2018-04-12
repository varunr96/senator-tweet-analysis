import tweepy
from tweepy import OAuthHandler
import json


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

senators = set()

filename = 'senators.txt'

f = open(filename, 'r')

for line in f:
	senators.add(line.rstrip('\n'))

f.close()

f = open('tweets.json', 'w')
all_tweets = dict.fromkeys(senators, [])
all_num_tweets = {}
num_tweets = 0


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
				tweet['text'] = status.full_text
				all_tweets[senator].append(tweet)
				num_tweets += 1
		else:
			print('{}: scrapped {} tweets!'.format(senator, num_tweets))

			break
		page += 1
	json_data = json.dumps(all_tweets, indent=4)
	f.write(json_data)
	f.close()
	exit(1)


f = open('num_tweets.txt', 'w')
for senator in senators:
	f.write("{} {}".format(senator, all_num_tweets[senator]))
f.close()
