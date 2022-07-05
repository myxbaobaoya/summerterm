from transformers import GPT2Tokenizer, GPT2Model
import torch
import csv
import re
import numpy as np

filename = '../drug_description.csv'
label = []
des = []
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2Model.from_pretrained('gpt2')
num = 0
with open(filename, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if (row['tag'] == ""):
            break
        if (row['des'] != None and row['des'] != '\n' and row['des'] != "" and row['des'] != " " and row['des'] != "\t" and row['des'] != '.') or (row['des_2'] != None and row['des_2'] != '\n' and row['des_2'] != "" and row['des_2'] != " " and row['des_2'] != "\t" and row['des_2'] != '.'):
            label.append(row['tag'])
            # des.append(row['des'])
            # des.append(row['des_2'])
            des.append(row['des'] + row['des_2'])
for index in range(len(label)):
    sentence = re.sub("([:.;,?!])", "", des[index])
    # text = "Replace me by any text you'd like."
    encoded_input = tokenizer(sentence, return_tensors='pt')
    output = model(**encoded_input)
    token_vecs = output.last_hidden_state[0]
    sentence_embedding = torch.mean(token_vecs, dim=0).detach().numpy()
    sentence_embedding = np.round(sentence_embedding, 1)
    sentence_embedding = np.append(sentence_embedding, label[index])

    with open("../drug_semantic_embedding_gpt2_des1+des2_768_7687.csv", "a+", newline='') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow(sentence_embedding)
