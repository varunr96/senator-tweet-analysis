import sentiment, sys
import matplotlib.pyplot as plt
import numpy as np

# Attach a text label above each bar displaying its height
def autolabel(rects):
    for rect in rects:
        height = float(rect.get_height())
        ax.text(float(rect.get_x() + rect.get_width()/2.), 1.0*height,
                '%d' % float(height),
                ha='center', va='bottom')

senator_info = {}
senator_handles_file = open("handles.txt", "r").read().split()
for line in senator_handles_file:
    state, gender, username, age, party = line.split(',')
    senator_info[username] = sentiment.Senator(username, party, state, gender, age)

sentimentClass = {}
filename = sys.argv[1]
f = open(filename, 'r').read().split()
for line in f:
	senator, sentiment = line.split(',')
	sentimentClass[senator] = sentiment

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

N = 3
maleValues = (malePosCount*100/maleCount, maleNeuCount*100/maleCount, maleNegCount*100/maleCount)
ind = np.arange(N)
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, maleValues, width, color='r')

femaleValues = (femalePosCount*100/femaleCount, femaleNeuCount*100/femaleCount, femaleNegCount*100/femaleCount)
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