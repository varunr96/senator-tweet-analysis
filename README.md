Senator Tweet Analysis

Need to run
```
pip install tweepy==3.3.0
```
to get twitter client

Data Files Needed for getTweets.py:
```
senators.txt
```
will be attached in submission

First run 
```
python getTweets.py
```
to get tweets.json which is json file of all the senators tweets and timestamps which will take around 4 hours because of Twitter's API call limitations. You will require Twitter credentials in the form of consumer_key, consumer_secret, access_token, acess_secret. 
We will attach "tweets.json" which is the output of getTweets.py

Data Files Needed for sentiment.py:
```
handles.txt, tweets.json, porterstemmer.py, preprocess.py
```
both will be attached in submission

Then run
```
python sentiment.py
```
to create a text file related to information needed for a specific topic.
Modify line 95 in "sentiment.py" to choose which topic you would like to analyze
This should write to a file related to the topic you choose i.e. if topics = ["gun", "guns"] then will return gun_guns.txt

Data Files Needed for stats.py:
```
gun_guns.txt, terror.txt, net.txt
```
all will be attached in submission, should 

Finally run
```
python stats.py ###.txt
```
with ###.txt being the text file that is outputted by sentiment.py (for our project we used gun_guns.txt, terror.txt, net.txt)

This will then print out on the command line the top 20 words for groups (gender, party, age) of your choice depending on how you change the code. This will also print out graphs denoted by lines 214-216. You will have to comment and rerun the code to get the different graphs.