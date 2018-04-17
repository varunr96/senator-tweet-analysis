from textblob import TextBlob
import json, re
import preprocess

# clean tweet for unnecesary symbols and what not
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# using textblob API to get sentiment of tweet
def getTweetSentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# class needed for return output
class TopicTweet:
    def __init__(self):
        self.positive_count = 0
        self.negative_count = 0
        self.neutral_count = 0
        self.type = ""
        self.tf = {}

# filling this info out from "handles.txt"
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

# preprocess and tokenize tweets
def getAllTokens(senator_tweet_text):
    tokens = preprocess.tokenizeText(senator_tweet_text)
    tokens = preprocess.removeStopwords(tokens)
    tokens = [t for t in tokens if len(t) > 1]
    for token in tokens:
        if token == 'w/':
            token = 'with'
    return tokens

# get sentiment per topic for each senator and also calculate tf for the topic
def topicSentiment(sentiment, topics, senator, senator_tweet_tokens, senator_topic_sentiments):
    proceed = False
    for topic in topics:
        if topic.lower() in senator_tweet_tokens:
            proceed = True
            break
    if proceed:
        if senator not in senator_topic_sentiments:
            senator_topic_sentiments[senator] = TopicTweet()
        if sentiment == 'positive':
            senator_topic_sentiments[senator].positive_count += 1
        elif sentiment == 'negative':
            senator_topic_sentiments[senator].negative_count += 1
        elif sentiment == 'neutral':
            senator_topic_sentiments[senator].neutral_count += 1
        for token in senator_tweet_tokens:
            if token not in senator_topic_sentiments[senator].tf:
                senator_topic_sentiments[senator].tf[token] = 0
            senator_topic_sentiments[senator].tf[token] += 1
        #Debug
        # if "utpol" in senator_tweet_tokens:
        #     print("Senator {} said : {}".format(senator, senator_tweet['text']))
        #Debug

def main():
    # load all tweets into python readable and parsable format
    tweets_file = open("tweets.json", "r")
    tweets = json.loads(tweets_file.read()) # key: senator username value: list of {'date', 'text'}

    # load all senator information from "handles.txt" into dictionary
    senator_info = {}
    senator_handles_file = open("handles.txt", "r").read().split()
    for line in senator_handles_file:
        state, gender, username, age, party = line.split(',')
        senator_info[username] = Senator(username, party, state, gender, age)

    senator_topic_sentiments = {}

    # modify topics for which topic you want to parse for
    topics = ["gun", "guns"]
    count = 0
    # going through every senator
    for senator in tweets:
        count += 1
        print("senator # " + str(count) + ": " + senator)
        senator_tweets = tweets[senator]
        senator_info[senator].total_tweets = len(tweets[senator])
        # storing overall sentiments in general and topic specific
        for senator_tweet in senator_tweets:
            tokens = getAllTokens(senator_tweet['text'])
            sentiment = getTweetSentiment(senator_tweet['text'])
            if sentiment == 'positive':
                senator_info[senator].positive_count += 1
            elif sentiment == 'negative':
                senator_info[senator].negative_count += 1
            elif sentiment == 'neutral':
                senator_info[senator].neutral_count += 1
            topicSentiment(sentiment, topics, senator, tokens, senator_topic_sentiments)
            
    # calculating what type overall sentiment a senator is for a topic
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
        senator_topic_sentiments[senator].type = type

    # calculating term frequency totals
    for senator in senator_topic_sentiments:
        total = 0.0
        for term in senator_topic_sentiments[senator].tf:
            total += senator_topic_sentiments[senator].tf[term]
        for term in senator_topic_sentiments[senator].tf:
            senator_topic_sentiments[senator].tf[term] /= float(total)

    # outputting information in format to be read by stats.py
    filename = ""
    for topic in topics:
        filename = filename + "_" + topic
    filename = filename[1:] + ".txt"
    f = open(filename, 'w')
    for senator in senator_topic_sentiments:
        f.write(senator + "," + senator_topic_sentiments[senator].type)
        for term, tf in senator_topic_sentiments[senator].tf.items():
            f.write("," + term + "," + str(tf))
        f.write("\n")
    f.close()

if __name__ == "__main__":
    main()