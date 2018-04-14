
senator_info = {}
senator_handles_file = open("handles.txt", "r").read().split()
for line in senator_handles_file:
    state, gender, username, age, party = line.split(',')
    senator_info[username] = Senator(username, party, state, gender, age)

sentimentClass = {}
filename = "gun_guns_control.txt"
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