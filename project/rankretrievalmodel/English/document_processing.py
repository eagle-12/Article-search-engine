from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import os
import json

class document_reduction:
    def decReduction(self,path):
        dir_list = [x[0] for x in os.walk(path)]
        file_list = os.listdir(dir_list[0])
        file_count = 0
        for file in file_list:
            file_path = path+'/'+file
            try:
                s1 = open(file_path,'r')
                file_source = s1.read()
                term_freq = {}
                filtered_doc = self.remove_stopwords(file_source)
                stemmed_doc = self.porter_stemmer(filtered_doc)
                for word in stemmed_doc:
                    term_freq[word]=0
                for word in stemmed_doc:
                    term_freq[word]+=1

                output_path = '/home/tex/Documents/IR/Final_Output2/'+file
                with open(output_path,'w',encoding='utf8') as output_file:
                    json.dump(term_freq,output_file,ensure_ascii=False)
                file_count=file_count+1
                print(" "+str(file_count)+" @@Done:- " + file_path)
                s1.close()
            except Exception as e:
                print(e)

    def remove_stopwords(self,doc):

        t_words = word_tokenize(doc)
        punctuations =['!', '"', '#', '$', '%', '&', "'", '(', ')', '*',"''",'``', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@','[', '\\','–',']', '^', '_', '`', '{', '|', '}', '~',"'s"]
        words = []
        #removing punctuations
        for w in t_words:
            if w not in punctuations:
                words.append(w)

        stop_words = set(stopwords.words("english"))
        filtered_doc = []

        """
        #removing all stop words insted of retaining three adjecent stop words
        for w in words:
            if w not in stop_words:
                filtered_doc.append(w)

        """
        for w in range(len(words)):
            if words[w] not in stop_words:
                filtered_doc.append(words[w])
            elif w<len(words)-2 and words[w] in stop_words and words[w+1] in stop_words and words[w+2] in stop_words:
                filtered_doc.append(words[w])
            elif w>0 and w<len(words)-1 and words[w] in stop_words and words[w+1] in stop_words and words[w-1] in stop_words:
                filtered_doc.append(words[w])
            elif w>1 and words[w] in stop_words and words[w-1] in stop_words and words[w-2] in stop_words:
                filtered_doc.append(words[w])

        return filtered_doc

    def porter_stemmer(self,doc_list):
        ps = PorterStemmer()
        Stemmed_doc = []
        for w in doc_list:
            Stemmed_doc.append(ps.stem(w))

        return Stemmed_doc
