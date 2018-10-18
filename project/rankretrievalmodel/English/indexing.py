import os
from nltk.tokenize import word_tokenize
import csv

class indexing:
    def file_indexing(self):
        path='/home/tex/Documents/IR/Final_Output'
        file_list = os.listdir(path)
        unique_words = []

        for file in file_list:
            file_path = path+'/'+file
            print(file_path)
            with open(file_path,"r") as source:
                text=source.read()
                #print(text)
                t_words = word_tokenize(text)
                #print(t_words)
                for words in t_words:
                    if words not in unique_words:
                        unique_words.append(words)

        tf_file = '/home/tex/Documents/IR/Wikipedia-Search-Engine/project/rank-retrieval-model/English/tf.csv'
        with open(tf_file,"w") as tf:
            writer = csv.writer(tf,delimiter=' ',quotechar=',',quoting = csv.QUOTE_MINIMAL)
            writer.writerow(unique_words)

        for file in file_list:
            file_path = path + '/' + file
            print(file_path)
            with open(file_path, "r") as source:
                text = source.read()
                t_words = word_tokenize(text)
                row = [0]*unique_words
                for w in range(len(unique_words)):
                    if unique_words[w] in t_words:
                        row[w]+=1
                writer.writerow(row)

        #print(len(unique_words))

