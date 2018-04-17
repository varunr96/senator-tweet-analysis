# Name: Byoung Hyun Bae 						Unique Name: bbae

import sys
import re
import porterstemmer
from os import listdir

def removeSGML(raw_text):
	cleanr = re.compile('<.*?>')
	clean_text = re.sub(cleanr, '', raw_text)
	return clean_text

def tokenizeText(clean_text):
	raw_tokens = clean_text.split()
	tokens = []
	for token in raw_tokens:
		# to lower case
		token = token.lower()
		token = token.replace('-', '')
		token = token.replace('#', '')
		token = token.replace(':', '')
		token = token.replace(';', '')
		token = token.replace('&amp', '')
		token = token.replace('rt', '')
		# remove all commas
		token = token.replace(',', '')
		# remove all quotes
		token = token.replace('"', '')
		# remove fullstop periods
		if token == '.' or token == '':
			continue
		if token.endswith('.') and token.count('.') == 1:
			token = token[:-1]
		# possessive
		if token == "i'm":
			tokens.append('i')
			tokens.append('am')
			continue
		if token == "i've":
			tokens.append('i')
			tokens.append('have')
			continue
		if token == "she's":
			tokens.append('she')
			tokens.append('is')
			continue
		if token == "he's":
			tokens.append('he')
			tokens.append('is')
			continue
		if token == "you're":
			tokens.append('you')
			tokens.append('are')
			continue
		if token == "we're":
			tokens.append('we')
			tokens.append('are')
			continue
		if token == "they're":
			tokens.append('they')
			tokens.append('are')
			continue
		if token == "wouldn't":
			tokens.append('would')
			tokens.append('not')
			continue
		if token == "shouldn't":
			tokens.append('should')
			tokens.append('not')
			continue
		if token == "couldn't":
			tokens.append('could')
			tokens.append('not')
			continue
		if token == "haven't":
			tokens.append('have')
			tokens.append('not')
			continue
		if token == "hadn't":
			tokens.append('had')
			tokens.append('not')
			continue
		if token == "aren't":
			tokens.append('are')
			tokens.append('not')
			continue
		if token.count("'") == 1:
			tokens += [t for t in token.split("'") if t]
			continue

		tokens.append(token)
	return tokens

def removeStopwords(tokens):
	stopwords = ["a","all","an","and","any","are","as","at","be","been","but","by","few","from","for","have","he","her","here","him","his","how","i","in","is","it","its","many","me","my","none","of","on","or","our","she","some","the","their","them","there","they","that","this","to","us","was","what","when","where","which","who","why","will","with","you","your"]
	return [token for token in tokens if token not in stopwords]

def stemWords(tokens):
	p = porterstemmer.PorterStemmer()
	for i in range(len(tokens)):
		tokens[i] = p.stem(tokens[i], 0,len(tokens[i])-1)

