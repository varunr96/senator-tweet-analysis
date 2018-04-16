Senator Tweet Analysis

Need to run 
```
pip install tweepy==3.3.0
```
to get twitter client

First run 
```
python getTweets.py
```
to get tweets.json which is json file of all the senators tweets and timestamps

Then run
```
python sentiment.py
```
to create a text file related to information needed for a specific topic.
Modify line 85 in "sentiment.py" to choose which topic you would like to analyze
This should write to a file related to the topic you choose i.e. if topics topics = ["gun", "guns"] then will return gun_guns.txt

Finally run
```
python stats.py ###.txt
```
with ###.txt being the text file that is outputted by sentiment.py

This will then print out on the command line the top 20 words for groups (gender, party, age) of your choice depending on how you change the code. This will also print out graphs denoted by lines 186-188. You will have to comment and rerun the code to get the different graphs.