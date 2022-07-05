import re
import torch
from transformers import BertModel, BertTokenizer, BertConfig
import csv
import numpy as np
import torch.nn as nn

np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt

filename = '../drug_description.csv'
max_length = 256

model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
label = []
des = []
with open(filename, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if (row['tag'] == ""):
            break
        if (row['des'] != None and row['des'] != '\n' and row['des'] != "" and row['des'] != " " and row['des'] != "\t" and row['des'] != '.') or (row['des_2'] != None and row['des_2'] != '\n' and row['des_2'] != "" and row['des_2'] != " "and row['des_2'] != "\t" and row['des_2'] != '.'):
        # if (row['des_2'] != None and row['des_2'] != '\n' and row['des_2'] != "" and row['des_2'] != " " and row['des_2'] != "\t" and row['des_2'] != "."):
            label.append(row['tag'])
            # des.append(row['des'])
            # des.append(row['des_2'])
            des.append(row['des'] + row['des_2'])
for index in range(len(label)):
    sentence = re.sub("([:.;,?!])", "", des[index])

    tokens = tokenizer(sentence, padding='max_length', max_length=max_length, truncation=True, return_tensors="pt")

    with torch.no_grad():
        # hidden_states = model(tokens['input_ids'], tokens['attention_mask'])
        hidden_states = model(tokens['input_ids'], attention_mask=tokens['attention_mask'], output_hidden_states=True,
                              output_attentions=True)
        hidden_states = hidden_states[2]

    token_vecs = hidden_states[-2][0]
    sentence_embedding = torch.mean(token_vecs, dim=0).detach().numpy()
    sentence_embedding = np.round(sentence_embedding, 1)
    sentence_embedding = np.append(sentence_embedding,label[index])
    # print("Our final sentence embedding vector of shape:", sentence_embedding)
    with open("../drug_semantic_embedding_bert_des1+des2_768_7981.csv", "a+", newline='') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow(sentence_embedding)