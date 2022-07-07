import os
import re
import torch
from transformers import BertModel, BertTokenizer, BertConfig,GPT2Tokenizer, GPT2Model
import csv
import numpy as np

label = []
des = []
max_length = 512
# model = BertModel.from_pretrained('bert-base-uncased')     #Bert
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')         #Gpt-2
model = GPT2Model.from_pretrained('gpt2')
path = '../stopWords'
files = os.listdir(path)
for file in files:
    f = open(path + '/' + file, encoding='utf-8')
    words = f.read()
    des.append(words)
    label.append(file[:-4:].strip().replace('_',' '))


# for index in range(len(label)):
#     sentence = re.sub("([:.;,?!])", "", des[index])
#
#     tokens = tokenizer(sentence, padding='max_length', max_length=max_length, truncation=True, return_tensors="pt")
#
#     with torch.no_grad():
#         # hidden_states = model(tokens['input_ids'], tokens['attention_mask'])
#         hidden_states = model(tokens['input_ids'], attention_mask=tokens['attention_mask'], output_hidden_states=True,
#                               output_attentions=True)
#         hidden_states = hidden_states[2]
#
#     token_vecs = hidden_states[-2][0]
#     sentence_embedding = torch.mean(token_vecs, dim=0).detach().numpy()
#     sentence_embedding = np.round(sentence_embedding, 1)
#     sentence_embedding = np.append(sentence_embedding,label[index])
#     # print("Our final sentence embedding vector of shape:", sentence_embedding)
#     with open("../Bert_embedding.csv", "a+", newline='') as f:
#         writer = csv.writer(f,delimiter=',')
#         writer.writerow(sentence_embedding)

for index in range(len(label)):
    sentence = re.sub("([:.;,?!])", "", des[index])
    #     # text = "Replace me by any text you'd like."
    encoded_input = tokenizer(sentence, max_length=1024,return_tensors='pt')
    output = model(**encoded_input)
    token_vecs = output.last_hidden_state[0]
    sentence_embedding = torch.mean(token_vecs, dim=0).detach().numpy()
    sentence_embedding = np.round(sentence_embedding, 1)
    sentence_embedding = np.append(sentence_embedding, label[index])

    with open("../Gpt2_embedding.csv", "a+", newline='') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow(sentence_embedding)