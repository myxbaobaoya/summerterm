import requests
from bs4 import BeautifulSoup
import csv
import random
import time
import re
import collections
import os
from operator import itemgetter
import pandas as pd

class SpyderDemo:
    def __init__(self,document):
        self.document = document
        self.wrong = 0
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
            'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        ]
    def spyder(self,url):          #crawl data from wiki for one virus
       # url = 'https://en.wikipedia.org/wiki/Monkeypox'
        headers = {
            'User-Agent': random.choice(self.user_agent_list)
        }
        response = requests.get(url,headers = headers)
        if (response.status_code != 200):
            self.wrong = self.wrong +1
            print(str(response.status_code) + url)
            url = 'https://en.wikipedia.org/wiki/' + url[30:].rsplit('_',1)[0]   #replace the name if there is no information in wiki
            print(url)
            response = requests.get(url, headers=headers)
        html = response.text
        obj = BeautifulSoup(html,'html5lib')
        document_name = '../spyderResult/' + url[30:] +'.txt'
        col_name = '../wordsCollection/col_' + url[30:] + '.txt'
        if(os.path.exists(document_name) == False):
            with open(document_name,'w',encoding='utf-8') as file:
                for paragraph in obj.find_all("p"):
                    #text = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", paragraph.text)
                    #text = re.sub(u"([？/ ，。,.:;:''';'''[]{}()（）《》])", "", paragraph.text)
                    text = re.sub("([`~@#$%^&*()_\\-+=|{}<>/~@#￥%……&*（）——+|{}【】‘；：”“’。，、？-])|([\\[0-9\\]])", "", paragraph.text)
                    file.write(text)
            file.close()
            self.wordsCollection(document_name,col_name)
        return url[30:].replace('_',' ')


    def wordsCollection(self,spyderfile,collectionFile):
        with open(spyderfile,'r',encoding='utf-8') as file:
            words = file.read().split()
            collectionResult = collections.Counter(words)
            #print(collectionResult)
        file.close()
        collectionResult = sorted(collectionResult.items(), key=itemgetter(1), reverse=True)
        out_words = ""
        for ss,tt in collectionResult:
            out_words = out_words + ss + '\t' + str(tt) + '\n'
        with open(collectionFile,'w',encoding='utf-8') as file:
                file.write(out_words)
        file.close()

    def virus_list(self):              #get all virus name from virus_list.csv
        with open(self.document,'r') as file:
            reader = csv.reader(file)
            virusName = [row[0].strip().replace(' ','_') for row in reader if (row[0] != "" and row[0] != '0')]
        file.close()
        return virusName


    def interface(self):
        virusName = self.virus_list()
        afterMappingName = []
        for virus in virusName:
            url = 'https://en.wikipedia.org/wiki/' + virus
            afterMappingName.append(self.spyder(url))
            time.sleep(10)
        print(self.wrong)
        print(afterMappingName)
        data = pd.read_csv(self.document)
        afterMappingName = afterMappingName.remove('species name') # 将新列的名字设置为cha
        data['after mapping'] = afterMappingName
        data.to_csv(self.document,index=False)
        # mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
        print(len(data))



if __name__ == "__main__":
    # demo = SpyderDemo('../Buccal_mucosa.csv')
    demo = SpyderDemo('../Stool.csv')
    demo.interface()
    #demo.wordsCollection('../spyderResult/Monkeypox.txt','../wordsCollection/col_Monkeypox.txt')
