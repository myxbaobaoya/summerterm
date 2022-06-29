import re
import torch
from transformers import BertModel, BertTokenizer
import csv
import numpy


filename = '../drug_description.csv'
max_length = 128
model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
label= []
des1 = []
des2 = []
with open(filename,'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        label.append(row['tag'])
        des1.append(row['des'])
        des2.append(row['des_2'])
        print(label,des1,des2)
        break
sentence = re.sub("([:.;,?!])", "", des1[0])
# sentence = 'I love beijing and I love you'
tokens = tokenizer(sentence, padding='max_length', max_length=max_length, truncation=True,return_tensors="pt")
output = model(tokens['input_ids'], attention_mask = tokens['attention_mask'])
#print('embedding:' , output[0][:,0,:].detach().numpy().tolist())
list = []
for i in range(max_length):
    list.append(str(output[0][0][i].detach().numpy().tolist()))
list.append(str(label))
# #print('hidden_states:' , len(output[0][0][0]))

with open("../drug_semantic_embedding_bert_128.csv","w",newline='') as f:
    writer = csv.writer(f, delimiter=',')
    for i in list:                # 对于每一行的，将这一行的每个元素分别写在对应的列中
        writer.writerow(i)
