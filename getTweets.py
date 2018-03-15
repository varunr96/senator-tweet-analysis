import tweepy
from tweepy import OAuthHandler
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

senators = set()

filename = 'senators.txt'

f = open(filename, 'r')

for line in f:
	senators.add(line.rstrip('\n'))

f.close()

print(senators)

f = open('tweets.txt', 'w')

for senator in senators:
	page = 1
	f.write(senator + '\n')
	while True:
	    statuses = api.user_timeline(senator, page=page, tweet_mode='extended')
	    if statuses:
	        for status in statuses:
	            f.write('{:%B %d, %Y}'.format(status.created_at) + '\n')
	            f.write(str(status.full_text) + '\n')
	    else:
	        break
	    page += 1
	break

f.close()
