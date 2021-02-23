import pickle
import math


def main():
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

    tf_type = int(input("Enter the type of TF you want to use: \n1 : Log Normalization \n2 : Double Normalization K \n"))
    idf_type = int(input("Enter the type of IDF you want to use: \n3 : Inverse Frequency Smooth \n4 : Probabilistic Inverse Frequency \n"))
    #Log Normalization = TF
    if tf_type==1:
        for i in range(len(vocab)):
        #print(i," ",vocab[i])
            for j in range(len(lines)):
                if fij[j][i]>0:
                    tfij[j][i] = 1 + math.log2(fij[j][i])

    #Double Normalization K = TF
    if tf_type==2:
        K = float(input("Enter the value of K: "))
        for i in range(len(vocab)):
            #print(i," ",vocab[i])
            max_fij = -10000
            for j in range(len(lines)):
                if fij[j][i]>max_fij:
                    max_fij = fij[j][i]

            for j in range(len(lines)):
                if fij[j][i]>0:
                    tfij[j][i] = K + (((1-K)*(fij[j][i]))/max_fij)

    N = len(lines)
    #Inverse Frequency Smooth
    if idf_type==3:
        for i in range(len(vocab)):
            idfi[i] = math.log2(1 + (N/ni[i]))

    #Probabilistic Inverse Frequency
    if idf_type==4:
        for i in range(len(vocab)):
            if N-ni[i]==0:
                idfi[i]=0
            else:
                idfi[i] = math.log2((N-ni[i])/ni[i])

    w = [[0 for i in range(len(vocab))] for j in range(len(lines))]
    for i in range(len(vocab)):
        #print(i," ",vocab[i])
        for j in range(len(lines)):
            if fij[j][i]>0:
                w[j][i] = tfij[j][i]*idfi[i]



    #processing the query
    q = input("Enter a query: ")
    query_words = q.split(' ')
    query_words = [i.lower() for i in query_words]
    qw = [0 for i in range(len(vocab))]
    qtf = [0 for i in range(len(vocab))]
    qidf = [0 for i in range(len(vocab))]
    qfi = [0 for i in range(len(vocab))]

    max_fij = -10000
    for word in query_words:
        for i in range(len(vocab)):
            if vocab[i]==word:
                qfi[i]+=1

    for i in range(len(vocab)):
        if qfi[i]>max_fij:
            max_fij=qfi[i]

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
        # qtf[wi] = 1 + math.log2(c)
        K=0.5

        for j in range(len(vocab)):
            if qfi[i]>0:
                qtf[wi] = K + (((1-K)*(qfi[i]))/max_fij)

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

        qidf[wi] = math.log2(1 + (N/ni))
        
        # if ni>0:
        #     if N-ni==0:
        #         qidf[wi]=0
        #     else:
        #         qidf[wi] = math.log2((N-ni)/ni)

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
            num += w[i][j]*qw[j]

        di_square=0
        for j in range(len(vocab)):
            di_square += (w[i][j]*w[i][j])
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

if __name__=='__main__':
    main()