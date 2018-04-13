from textblob import TextBlob
import json, re

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

class Senator:
    def __init__(self, username, party, state, gender, age):
        self.username = username
        self.party = party
        self.state = state
        self.gender = gender
        self.age = age
        self.positive_count = 0
        self.negative_count = 0
        self.neutral_count = 0

tweets_file = open("tweets.json", "r")
tweets = json.loads(tweets_file.read()) # key: senator username         value: list of {'date', 'text'}

senator_sentiments = {}
all_senator_info = open("handles.txt", "r").read().split()
for senator_info in all_senator_info:
    state, gender, username, age, party = senator_info.split(',')
    senator_sentiments[username] = Senator(username, party, state, gender, age)

#for key in senator_sentiments:
    #print "{}: {} {} {} {}".format(key, senator_sentiments[key].gender, senator_sentiments[key].age, senator_sentiments[key].party, senator_sentiments[key].state)
#exit(1)

for senator in tweets:
    senator_tweets = tweets[senator]
    for senator_tweet in senator_tweets:
        sentiment = get_tweet_sentiment(senator_tweet['text'])
        if sentiment == 'positive':
            senator_sentiments[senator].positive_count += 1
        elif sentiment == 'negative':
            senator_sentiments[senator].negative_count += 1
        elif sentiment == 'neutral':
            senator_sentiments[senator].neutral_count += 1

for senator in senator_sentiments:
    print("New Senator")
    print senator_sentiments[senator].username
    print senator_sentiments[senator].state
    print senator_sentiments[senator].gender
    print senator_sentiments[senator].age
    print senator_sentiments[senator].party
    print senator_sentiments[senator].positive_count
    print senator_sentiments[senator].negative_count
    print senator_sentiments[senator].neutral_count
    print("\n")

#print senator_sentiments['RoyBlunt'].positive_count + senator_sentiments['RoyBlunt'].negative_count + senator_sentiments['RoyBlunt'].neutral_count
