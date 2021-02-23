import pickle
import math

with open("fij.txt","rb") as fp:
	fij = pickle.load(fp)

with open("ni.txt","rb") as fp:
	ni = pickle.load(fp)

with open("vocab.txt","rb") as fp:
	vocab = pickle.load(fp)

file1 = open('animal_list.txt','r')
lines = file1.readlines()

idfi = [0 for i in range(len(vocab))]
tfij = [[0 for i in range(len(vocab))] for j in range(len(lines))]

for i in range(len(vocab)):
	#print(i," ",vocab[i])
	for j in range(len(lines)):
		if fij[j][i]>0:
			tfij[j][i] = 1 + math.log2(fij[j][i])

N = len(lines)
for i in range(len(vocab)):
	idfi[i] = math.log2(N/ni[i])


tf_idf = [[0 for i in range(len(vocab))] for j in range(len(lines))]
for i in range(len(vocab)):
	#print(i," ",vocab[i])
	for j in range(len(lines)):
		if fij[j][i]>0:
			tf_idf[j][i] = tfij[j][i]*idfi[i]

q = input("Enter a query: ")
query_words = q.split(' ')
query_words = [i.lower() for i in query_words]
qw = [0 for i in range(len(vocab))]
qtf = [0 for i in range(len(vocab))]
qidf = [0 for i in range(len(vocab))]

for word in query_words:
	wi=0
	for i in range(len(vocab)):
		if vocab[i]==word:
			wi=i
			break
	c = 0
	for j in range(len(query_words)):
		if query_words[j]==word:
			c+=1
	qtf[wi] = 1 + math.log2(c)

for word in query_words:
	wi=0
	for i in range(len(vocab)):
		if vocab[i]==word:
			wi=i
			break
	ni = 0
	for j in range(len(lines)):
		animal = lines[j].strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')
		for k in range(len(text)):
			if(text[k]==word):
				ni+=1
				break
	if ni>0:
		qidf[wi] = math.log2(N/ni)

for word in query_words:
	wi=0
	for i in range(len(vocab)):
		if vocab[i]==word:
			wi=i
			break
	qw[wi] = qtf[wi]*qidf[wi]

cos_similarity = [0 for i in range(len(lines))]

qsquare=0
for i in range(len(qw)):
	qsquare += (qw[i]*qw[i])

for i in range(len(lines)):
	num = 0
	for j in range(len(vocab)):
		num += tf_idf[i][j]*qw[j]

	di_square=0
	for j in range(len(vocab)):
		di_square += (tf_idf[i][j]*tf_idf[i][j])
	den = math.sqrt(di_square*qsquare)

	cos_similarity[i] = num/den

similarity = []
for i in range(len(lines)):
	animal = lines[i].strip()
	similarity.append([cos_similarity[i],animal,"d"+str(i+1)])

similarity = sorted(similarity,reverse=True)

for i in range(len(similarity)):
	if i==len(similarity)-1:
		print(similarity[i][2])
	else:
		print(similarity[i][2]," -> ",end='')

for i in range(len(similarity)):
	print(similarity[i][2]," = ",similarity[i][1]," -> ",similarity[i][0])