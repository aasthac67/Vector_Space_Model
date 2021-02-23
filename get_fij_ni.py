import pickle

def main():
	file1 = open('animal_list.txt','r')
	lines = file1.readlines()

	vocabulary = set()

	for line in lines:
		animal = line.strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')
		for token in text:
			vocabulary.add(token)

	vocab = list(vocabulary)

	ni = [0 for i in range(len(vocab))]
	fij = [[0 for i in range(len(vocab))] for j in range(len(lines))]

	for i in range(len(vocab)):
		print(i," ",vocab[i])
		for j in range(len(lines)):
			word = vocab[i]
			animal = lines[j].strip()
			f1 = open(f'preprocessed_data/{animal}.txt','r')
			text = f1.read().split(' ')
			for k in range(len(text)):
				if(text[k]==word):
					fij[j][i]+=1

	for i in range(len(vocab)):
		print(i," ",vocab[i])
		for line in lines:
			word = vocab[i]
			animal = line.strip()
			f1 = open(f'preprocessed_data/{animal}.txt','r')
			text = f1.read().split(' ')
			for k in range(len(text)):
				if(text[k]==word):
					ni[i]+=1
					break

	with open("fij.txt","wb") as fp:
		pickle.dump(fij,fp)

	with open("ni.txt","wb") as fp:
		pickle.dump(ni,fp)

	with open("vocab.txt","wb") as fp:
		pickle.dump(vocab,fp)


if __name__=='__main__':
	main()