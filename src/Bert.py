import re
import torch
from transformers import BertModel, BertTokenizer
# import tensorflow as tf
import matplotlib.pyplot as plt
# print(tf.__path__)
model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
with open("../spyderResult/Abiotrophia.txt",encoding='UTF-8') as f:
    sentence = re.sub("([:.;,?!])", "", f.read())
# sentence = 'I love beijing and I love you'
tokens = tokenizer.tokenize(sentence)
tokens = ['[CLS]'] + tokens + ['[SEP]']
print('tokens length:',len(tokens))
print(tokens)
attention_mask = [ 1 if t != '[PAD]' else 0 for t in tokens]
print('attention_mask:' , attention_mask)
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print('length token_ids:',len(token_ids))
print('token_ids:',token_ids)
#
# #combine token_ids and attention_mask
# token_ids = tf.convert_to_tensor(token_ids)
# token_ids = tf.reshape(token_ids, [1, -1])
# attention_mask = tf.convert_to_tensor(attention_mask)
# attention_mask = tf.reshape(attention_mask, [1, -1])
token_ids = torch.Tensor(token_ids).to(torch.int64)
token_ids = torch.reshape(token_ids, [1, -1])
attention_mask = torch.Tensor(attention_mask).to(torch.int64)
attention_mask = torch.reshape(attention_mask, [1, -1])
output = model(token_ids, attention_mask = attention_mask)
print('embedding_shape:' , output[0].shape, output[1].shape)
#print('embedding:' , output[0][:,0,:])
print('hidden_states:' , output[0])
