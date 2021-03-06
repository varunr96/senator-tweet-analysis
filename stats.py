import sentiment, sys
import matplotlib.pyplot as plt
import numpy as np
import operator

fig, ax = plt.subplots()

# Attach a text label above each bar displaying its height
def autolabel(rects):
    for rect in rects:
        height = float(rect.get_height())
        ax.text(float(rect.get_x() + rect.get_width()/2.), 1.0*height,
                '%d' % float(height),
                ha='center', va='bottom')

# function to plot the bar graphs
def plot(list1, list2, category):
	category1 = ''
	category2 = ''
	if category == 'Gender':
		category1 = "Male"
		category2 = "Female"
	if category == 'Political Party':
		category1 = "Democrat"
		category2 = "Republican"
	if category == 'Age':
		category1 = 'Younger than or equal to 62'
		category2 = 'Older than 62'
	total1 = sum(list1)
	total2 = sum(list2)
	N = 3
	width = 0.35
	ind = np.arange(N)
	# we want the percents so we divide by total # and multiply by 100
	values_1 = (list1[0]*100/total1, list1[1]*100/total1, list1[2]*100/total1)
	values_2 = (list2[0]*100/total2, list2[1]*100/total2, list2[2]*100/total2)
	# for 3 seperate graphs
	rects1 = ax.bar(ind, values_1, width, color='r')
	rects2 = ax.bar(ind + width, values_2, width, color='b')

	ax.set_ylabel("Senator Sentiment Percentage")
	ax.set_xlabel("Gun Control Topic")
	ax.set_title("Percentage of Senator Sentiments by " + category)
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(('POS', 'NEU', 'NEG'))

	ax.legend((rects1[0], rects2[0]), (category1, category2))
	autolabel(rects1)
	autolabel(rects2)

	plt.show()

# print top k words in a format
def printTopK(dict, k):
	sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
	for i in range(k):
		print("#{}: {}".format(i, sorted_dict[i]))

def main():
	# recreating senator information including age, party, and gender
	senator_info = {}
	senator_handles_file = open("handles.txt", "r").read().split()
	for line in senator_handles_file:
	    state, gender, username, age, party = line.split(',')
	    senator_info[username] = sentiment.Senator(username, party, state, gender, age)

	# reading passed in files from command line
	sentimentClass = {}
	tf = {}
	filename = sys.argv[1]
	f = open(filename, 'r').read().split()
	for line in f:
		# parsing line to retrieve senator twitter data
		# senator twitter data format:
		# twitter_user_id,sentiment_classification,term1,weight1,term2,weight2,...
		info = line.split(',')
		senator = info[0]
		tf[senator] = {}
		sentimentClass[senator] = info[1]

		# Recreate the term-frequency dictionary for this senator 
		# Note: doc corpus = all RELEVENT tweets from the senator
		info = info[2:]
		i = 0
		while i < len(info):
			tf[senator][info[i]] = float(info[i+1])
			i += 2
	# code specifically for gender tf's
	male_tf = {}
	female_tf = {}
	for senator in sentimentClass: 
		if senator_info[senator].gender == 'M':
			for term, freq in tf[senator].items():
				if term not in male_tf:
					male_tf[term] = 0
				# aggregate all tf's for all male senators
				male_tf[term] += freq
		elif senator_info[senator].gender == 'F':
			for term, freq in tf[senator].items():
				if term not in female_tf:
					female_tf[term] = 0
				# aggregate all tf's for all female senators
				female_tf[term] += freq

	print("Male Top 20 Words:")
	printTopK(male_tf, 20)
	print("Female Top 20 Words:")
	printTopK(female_tf, 20)

	# code for calculating adjusted top 20 words
	total = 0.0
	for term, freq in male_tf.items():
		total += freq
	for term in male_tf:
		male_tf[term] /= float(total)
	total = 0.0
	for term, freq in female_tf.items():
		total += freq
	for term in female_tf:
		female_tf[term] /= float(total)

	# subtracting words that appear in opposite sides tf corpus
	# used to give more weight to words said specifically by a certain group
	adjusted_male_tf = {}
	adjusted_female_tf = {}
	for term in male_tf:
		if term in female_tf:
			adjusted_male_tf[term] = male_tf[term] - female_tf[term]
		else:
			adjusted_male_tf[term] = male_tf[term]
	for term in female_tf:
		if term in male_tf:
			adjusted_female_tf[term] = female_tf[term] - male_tf[term]
		else:
			adjusted_female_tf[term] = female_tf[term]

	print("\n\nAdjusted Male Top 20 Words:")
	printTopK(adjusted_male_tf, 20)
	print("Adjusted Female Top 20 Words:")
	printTopK(adjusted_female_tf, 20)

	# counting values needed for bar graphs
	# specifically for gender
	malePosCount = 0; femalePosCount = 0
	maleNeuCount = 0; femaleNeuCount = 0
	maleNegCount = 0; femaleNegCount = 0
	for senator in sentimentClass: 
		if senator_info[senator].gender == 'M':
			if sentimentClass[senator] == "pos":
				malePosCount += 1
			elif sentimentClass[senator] == "neg":
				maleNegCount += 1
			else:
				maleNeuCount += 1
		elif senator_info[senator].gender == 'F':
			if sentimentClass[senator] == "pos":
				femalePosCount += 1
			elif sentimentClass[senator] == "neg":
				femaleNegCount += 1
			else:
				femaleNeuCount += 1

	# counting values needed for bar graphs
	# specifically for party
	demPosCount = 0; repPosCount = 0
	demNeuCount = 0; repNeuCount = 0
	demNegCount = 0; repNegCount = 0
	for senator in sentimentClass: 
		if senator_info[senator].party == 'D':
			if sentimentClass[senator] == "pos":
				demPosCount += 1
			elif sentimentClass[senator] == "neg":
				demNegCount += 1
			else:
				demNeuCount += 1
		elif senator_info[senator].party == 'R':
			if sentimentClass[senator] == "pos":
				repPosCount += 1
			elif sentimentClass[senator] == "neg":
				repNegCount += 1
			else:
				repNeuCount += 1

	# counting values needed for bar graphs
	# specifically for age
	youngPosCount = 0; oldPosCount = 0
	youngNeuCount = 0; oldNeuCount = 0
	youngNegCount = 0; oldNegCount = 0
	for senator in sentimentClass: 
		if senator_info[senator].age <= 62:
			if sentimentClass[senator] == "pos":
				youngPosCount += 1
			elif sentimentClass[senator] == "neg":
				youngNegCount += 1
			else:
				youngNeuCount += 1
		else:
			if sentimentClass[senator] == "pos":
				oldPosCount += 1
			elif sentimentClass[senator] == "neg":
				oldNegCount += 1

	# creating lists of all values we care about for graphing
	gender1 = [malePosCount, maleNeuCount, maleNegCount]
	gender2 = [femalePosCount, femaleNeuCount, femaleNegCount]
	party1 = [demPosCount, demNeuCount, demNegCount]
	party2 = [repPosCount, repNeuCount, repNegCount]
	age1 = [youngPosCount, youngNeuCount, youngNegCount]
	age2 = [oldPosCount, oldNeuCount, oldNegCount]

	# can only show one graph at a time
	# need to uncomment line for graph we want to see
	# and comment other lines
	plot(gender1, gender2, "Gender")
	# plot(party1, party2, "Political Party")
	# plot(age1, age2, "Age")

if __name__ == "__main__":
    main()