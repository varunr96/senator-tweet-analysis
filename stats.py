import sentiment, sys
import matplotlib.pyplot as plt
import numpy as np
import operator

# Attach a text label above each bar displaying its height
def autolabel(rects):
    for rect in rects:
        height = float(rect.get_height())
        ax.text(float(rect.get_x() + rect.get_width()/2.), 1.0*height,
                '%d' % float(height),
                ha='center', va='bottom')

def printTopK(dict, k):
	sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
	for i in range(k):
		print("#{}: {}".format(i, sorted_dict[i]))

def main():
	senator_info = {}
	senator_handles_file = open("handles.txt", "r").read().split()
	for line in senator_handles_file:
	    state, gender, username, age, party = line.split(',')
	    senator_info[username] = sentiment.Senator(username, party, state, gender, age)

	sentimentClass = {}
	tf = {}
	filename = sys.argv[1]
	f = open(filename, 'r').read().split()
	for line in f:
		info = line.split(',')
		senator = info[0]

		tf[senator] = {}
		sentimentClass[senator] = info[1]
		info = info[2:]
		i = 0
		while i < len(info):
			tf[senator][info[i]] = float(info[i+1])
			i += 2

	male_tf = {}
	female_tf = {}
	for senator in sentimentClass: 
		if senator_info[senator].gender == 'M':
			for term, freq in tf[senator].items():
				if term not in male_tf:
					male_tf[term] = 0
				male_tf[term] += freq
		elif senator_info[senator].gender == 'F':
			for term, freq in tf[senator].items():
				if term not in female_tf:
					female_tf[term] = 0
				female_tf[term] += freq

	sorted_male_tf = sorted(male_tf.items(), key=operator.itemgetter(1), reverse=True)
	sorted_female_tf = sorted(female_tf.items(), key=operator.itemgetter(1), reverse=True)
	print("Male Top 20 Words:")
	printTopK(male_tf, 20)
	print("Female Top 20 Words:")
	printTopK(female_tf, 20)

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

	adjusted_male_tf = {}
	for term in male_tf:
		if term in female_tf:
			adjusted_male_tf[term] = male_tf[term] - female_tf[term]
		else:
			adjusted_male_tf[term] = male_tf[term]
	adjusted_female_tf = {}
	for term in female_tf:
		if term in male_tf:
			adjusted_female_tf[term] = female_tf[term] - male_tf[term]
		else:
			adjusted_female_tf[term] = female_tf[term]
	print("\n\nAdjusted Male Top 20 Words:")
	printTopK(adjusted_male_tf, 20)
	print("Adjusted Female Top 20 Words:")
	printTopK(adjusted_female_tf, 20)

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

	youngPosCount = 0; oldPosCount = 0
	youngNeuCount = 0; oldNeuCount = 0
	youngNegCount = 0; oldNegCount = 0
	for senator in sentimentClass: 
		if senator_info[senator].age >= 40 and senator_info[senator].age <= 62:
			if sentimentClass[senator] == "pos":
				youngPosCount += 1
			elif sentimentClass[senator] == "neg":
				youngNegCount += 1
			else:
				youngNeuCount += 1
		elif senator_info[senator].age > 62:
			if sentimentClass[senator] == "pos":
				oldPosCount += 1
			elif sentimentClass[senator] == "neg":
				oldNegCount += 1
			else:
				oldNeuCount += 1

	maleCount = float(malePosCount + maleNeuCount + maleNegCount)
	femaleCount = float(femalePosCount + femaleNeuCount + femaleNegCount)


	# code to graph. for eveyr topic we will have 3 bar graphs
	N = 3
	width = 0.35
	ind = np.arange(N)
	maleValues = (malePosCount*100/maleCount, maleNeuCount*100/maleCount, maleNegCount*100/maleCount)
	femaleValues = (femalePosCount*100/femaleCount, femaleNeuCount*100/femaleCount, femaleNegCount*100/femaleCount)
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, maleValues, width, color='r')
	rects2 = ax.bar(ind + width, femaleValues, width, color='b')

	ax.set_ylabel("Senator Sentiment Percentage")
	ax.set_xlabel("Gun/Guns/Control Topic")
	ax.set_title("Percentage of Senator Sentiments by Gender")
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(('POS', 'NEU', 'NEG'))

	ax.legend((rects1[0], rects2[0]), ('Male', 'Female'))
	autolabel(rects1)
	autolabel(rects2)

	plt.show()

if __name__ == "__main__":
    main()