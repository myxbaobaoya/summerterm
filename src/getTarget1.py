import pandas as pd
import numpy as np
import csv

filename_pairwise = '../pairwise.csv'
df = pd.read_csv(filename_pairwise,skiprows=1,header=None,sep=',')
microbiome1 = df.iloc[:,0]
microbiome2 = df.iloc[:,1]
filename_Bert = '../Bert_embedding.csv'
df=pd.read_csv(filename_Bert,skiprows=1,header=None,sep=',')
embedding = df.iloc[:,:768].values
label = df.iloc[:,768]

for i in range(len(microbiome1)):
    embedding_virus1 = df[label == microbiome1[i]].index.tolist()[0]
    embedding_virus2 = df[label == microbiome2[i]].index.tolist()[0]
    target = "1"
    embedding_total = np.append(embedding[embedding_virus1], embedding[embedding_virus2])
    data = np.append(embedding_total, target)

    with open("../trainX.csv", "a+", newline='') as f:
            writer = csv.writer(f,delimiter=',')
            writer.writerow(data)


