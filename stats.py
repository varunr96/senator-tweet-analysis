import sentiment

senator_info = {}
senator_handles_file = open("handles.txt", "r").read().split()
for line in senator_handles_file:
    state, gender, username, age, party = line.split(',')
    senator_info[username] = Senator(username, party, state, gender, age)
    print(state)

sentimentClass = {}
filename = "gun_guns_control.txt"
f = open(filename, 'r').read().split()
for line in f:
	senator, sentiment = line.split(',')
	sentimentClass[senator] = sentiment

malePosCount = 0; femalePosCount = 0
maleNeuCount = 0; femaleNeuCount = 0
maleNegCount = 0; femaleNegCount = 0
print("parsed")
for senator in sentimentClass: 
	if senator.gender == 'M':
		if senator.sentiment == "pos":
			malePosCount += 1
		elif senator.sentiment == "neg":
			maleNegCount += 1
		else:
			maleNeuCount += 1
	elif senator.gender == 'F':
		if senator.sentiment == "pos":
			femalePosCount += 1
		elif senator.sentiment == "neg":
			femaleNegCount += 1
		else:
			femaleNeuCount += 1

demPosCount = 0; repPosCount = 0
demNeuCount = 0; repNeuCount = 0
demNegCount = 0; repNegCount = 0
for senator in sentimentClass: 
	if senator.party == 'D':
		if senator.sentiment == "pos":
			dePosCount += 1
		elif senator.sentiment == "neg":
			deNegCount += 1
		else:
			deNeuCount += 1
	elif senator.party == 'R':
		if senator.sentiment == "pos":
			repPosCount += 1
		elif senator.sentiment == "neg":
			repNegCount += 1
		else:
			repNeuCount += 1

youngPosCount = 0; oldPosCount = 0
youngNeuCount = 0; oldNeuCount = 0
youngNegCount = 0; oldNegCount = 0
for senator in sentimentClass: 
	if senator.age >= 40 and senator.age <= 62:
		if senator.sentiment == "pos":
			youngPosCount += 1
		elif senator.sentiment == "neg":
			youngNegCount += 1
		else:
			youngNeuCount += 1
	elif senator.gender > 62:
		if senator.sentiment == "pos":
			oldPosCount += 1
		elif senator.sentiment == "neg":
			oldNegCount += 1
		else:
			oldNeuCount += 1