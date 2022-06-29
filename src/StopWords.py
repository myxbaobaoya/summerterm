import nltk
from nltk.corpus import stopwords
import os
nltk.download('stopwords')

def readFile():
    path = '../spyderResult'
    files = os.listdir(path)
    for file in files:
        f = open(path + '/' + file, encoding='utf-8')
        words = f.read().split()
        stop_words = set(stopwords.words('english'))
        for r in words:
            if not r in stop_words:
                appendFile = open('../stopWords/' + file, 'a',encoding='utf-8')
                appendFile.write(r + " ")
                appendFile.close()




readFile()
