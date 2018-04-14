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

class TopicTweet:
    def __init__(self, username):
        self.username = username
        self.positive_count = 0
        self.negative_count = 0
        self.neutral_count = 0

class Senator:
    def __init__(self, username, party, state, gender, age):
        self.username = username
        self.party = party
        self.state = state
        self.gender = gender
        self.age = int (age)
        self.total_tweets = 0 # for normalization
        self.positive_count = 0
        self.negative_count = 0
        self.neutral_count = 0

def TopicSentiment(topics, senator, senator_tweet, senator_topic_sentiments):
    proceed = False
    for topic in topics:
        if topic in senator_tweet['text']:
            proceed = True
            break
    if proceed:
        if senator not in senator_topic_sentiments:
            senator_topic_sentiments[senator] = TopicTweet(senator)
        if sentiment == 'positive':
            senator_topic_sentiments[senator].positive_count += 1
        elif sentiment == 'negative':
            senator_topic_sentiments[senator].negative_count += 1
        elif sentiment == 'neutral':
            senator_topic_sentiments[senator].neutral_count += 1

tweets_file = open("tweets.json", "r")
tweets = json.loads(tweets_file.read()) # key: senator username value: list of {'date', 'text'}

senator_info = {}
senator_handles_file = open("handles.txt", "r").read().split()
for line in senator_handles_file:
    state, gender, username, age, party = line.split(',')
    senator_info[username] = Senator(username, party, state, gender, age)

senator_topic_sentiments = {}

topics = ["privacy"]
for senator in tweets:
    senator_tweets = tweets[senator]
    senator_info[senator].total_tweets = len(tweets[senator])
    for senator_tweet in senator_tweets:
        sentiment = get_tweet_sentiment(senator_tweet['text'])

        TopicSentiment(topics, senator, senator_tweet, senator_topic_sentiments)
        if sentiment == 'positive':
            senator_info[senator].positive_count += 1
        elif sentiment == 'negative':
            senator_info[senator].negative_count += 1
        elif sentiment == 'neutral':
            senator_info[senator].neutral_count += 1

filename = ""
for topic in topics:
    filename = filename + "_" + topic
filename = filename + ".txt"
f = open(filename, 'w')

topicList = []
for senator in senator_topic_sentiments:
    largest = -1
    type = ""
    if senator_topic_sentiments[senator].positive_count > largest:
        largest = senator_topic_sentiments[senator].positive_count
        type = "pos"
    if senator_topic_sentiments[senator].negative_count > largest:
        largest = senator_topic_sentiments[senator].negative_count
        type = "neg"
    if senator_topic_sentiments[senator].neutral_count > largest:
        largest = senator_topic_sentiments[senator].neutral_count
        type = "neu"
    topicList.append((senator, type))

for tuple in topicList:
    f.write(tuple[0] + "," + tuple[1] + "\n")
f.close()

# malePosCount = 0; femalePosCount = 0
# maleNeuCount = 0; femaleNeuCount = 0
# maleNegCount = 0; femaleNegCount = 0
# for tuple in topicList:
#     if senator_info[tuple[0]].gender == 'M' and tuple[1] == "pos":
#         malePosCount += 1
#     elif senator_info[tuple[0]].gender == 'F' and tuple[1] == "pos":
#         femalePosCount += 1

#     if senator_info[tuple[0]].gender == 'M' and tuple[1] == "neg":
#         maleNegCount += 1
#     elif senator_info[tuple[0]].gender == 'F' and tuple[1] == "neg":
#         femaleNegCount += 1

#     if senator_info[tuple[0]].gender == 'M' and tuple[1] == "neu":
#         maleNeuCount += 1
#     elif senator_info[tuple[0]].gender == 'F' and tuple[1] == "neu":
#         femaleNeuCount += 1

# demPosCount = 0; repPosCount = 0
# demNeuCount = 0; repNeuCount = 0
# demNegCount = 0; repNegCount = 0
# for tuple in topicList:
#     if senator_info[tuple[0]].party == 'D' and tuple[1] == "pos":
#         demPosCount += 1
#     elif senator_info[tuple[0]].party == 'R' and tuple[1] == "pos":
#         repPosCount += 1

#     if senator_info[tuple[0]].party == 'D' and tuple[1] == "neg":
#         demNegCount += 1
#     elif senator_info[tuple[0]].party == 'R' and tuple[1] == "neg":
#         repNegCount += 1

#     if senator_info[tuple[0]].party == 'D' and tuple[1] == "neu":
#         demNeuCount += 1
#     elif senator_info[tuple[0]].party == 'R' and tuple[1] == "neu":
#         repNeuCount += 1

# youngPosCount = 0; oldPosCount = 0
# youngNeuCount = 0; oldNeuCount = 0
# youngNegCount = 0; oldNegCount = 0
# for tuple in topicList:
#     if senator_info[tuple[0]].age >= 40 and senator_info[tuple[0]].age <= 62 and tuple[1] == "pos":
#         youngPosCount += 1
#     elif senator_info[tuple[0]].age >= 63 and tuple[1] == "pos":
#         oldPosCount += 1

#     if senator_info[tuple[0]].age >= 40 and senator_info[tuple[0]].age <= 62 and tuple[1] == "neg":
#         youngNegCount += 1
#     elif senator_info[tuple[0]].age >= 63 and tuple[1] == "neg":
#         oldNegCount += 1

#     if senator_info[tuple[0]].age >= 40 and senator_info[tuple[0]].age <= 62 and tuple[1] == "neu":
#         youngNeuCount += 1
#     elif senator_info[tuple[0]].age >= 63 and tuple[1] == "neu":
#         oldNeuCount += 1