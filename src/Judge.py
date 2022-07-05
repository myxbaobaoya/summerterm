import csv

file1 = '../drug_description.csv'
file2 = '../drug_semantic_embedding_bert_des2_768_7729.csv'
with open(file1,'r') as csvfile:
    reader1 = csv.DictReader(csvfile)
    column1 = [row['tag']  for row in reader1 if (len(row['des_2']) >= 2)]

with open(file2,'r') as csvfile:
    reader2 = csv.DictReader(csvfile)
    column2 = [row['label'] for row in reader2]


print(set(column1)^set(column2))