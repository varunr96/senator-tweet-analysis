from textblob import TextBlob
import json, re
import preprocess

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
        self.tf = {}

def TopicSentiment(sentiment, topics, senator, senator_tweet_tokens, senator_topic_sentiments):
    proceed = False
    for topic in topics:
        if topic.lower() in senator_tweet_tokens:
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


def main():
    tweets_file = open("tweets.json", "r")
    tweets = json.loads(tweets_file.read()) # key: senator username value: list of {'date', 'text'}

    senator_info = {}
    senator_handles_file = open("handles.txt", "r").read().split()
    for line in senator_handles_file:
        state, gender, username, age, party = line.split(',')
        senator_info[username] = Senator(username, party, state, gender, age)

    senator_topic_sentiments = {}

    topics = ["gun", "guns"]
    count = 0
    for senator in tweets:
        count += 1
        print("senator # " + str(count) + ": " + senator)
        senator_tweets = tweets[senator]
        senator_info[senator].total_tweets = len(tweets[senator])
        for senator_tweet in senator_tweets:
            tokens = preprocess.tokenizeText(senator_tweet['text'])
            tokens = preprocess.removeStopwords(tokens)
            for token in tokens:
                if len(token) == 1:
                    continue
                if token not in senator_info[senator].tf:
                    senator_info[senator].tf[token] = 0
                senator_info[senator].tf[token] += 1
            sentiment = get_tweet_sentiment(senator_tweet['text'])
            TopicSentiment(sentiment, topics, senator, tokens, senator_topic_sentiments)
            if sentiment == 'positive':
                senator_info[senator].positive_count += 1
            elif sentiment == 'negative':
                senator_info[senator].negative_count += 1
            elif sentiment == 'neutral':
                senator_info[senator].neutral_count += 1
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
    for senator in senator_info:
        total = 0.0
        for term in senator_info[senator].tf:
            total += senator_info[senator].tf[term]
        for term in senator_info[senator].tf:
            senator_info[senator].tf[term] /= float(total)

    filename = ""
    for topic in topics:
        filename = filename + "_" + topic
    filename = filename[1:] + ".txt"
    f = open(filename, 'w')
    for tuple in topicList:
        f.write(tuple[0] + "," + tuple[1])
        for term, tf in senator_info[tuple[0]].tf.items():
            f.write("," + term + "," + str(tf))
        f.write("\n")
    f.close()



if __name__ == "__main__":
    main()