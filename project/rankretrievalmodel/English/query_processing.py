from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

class query_reduction():

    """
        this function is used to remove stop-words , punctuation and case folding in query
        firstly query is tokenized, then punctuations are removed and further stop words are removed alonge with case folding 
    """
    """def __init__(self, query):
        self.query = query
    """
    def reducedQuery_stopwords(self,query):
        #query = "rank of the retrieval this is and model 1234 in information to be and not to be retrieval for searching of and"
        t_words = word_tokenize(query)
        punctuations = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', "''", '``', '+', ',', '-', '.', '/', ':', ';',
                        '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
        words = []
        # removing punctuations
        for w in t_words:
            if w not in punctuations:
                words.append(w)
        stop_words = set(stopwords.words("english"))
        filtered_query = []
        """
        for w in words:
            if w not in stop_words:
                filtered_query.append(w.lower())
        """

        for w in range(len(words)):
            if words[w] not in stop_words:
                filtered_query.append(words[w].lower())
            elif w<len(words)-2 and words[w] in stop_words and words[w+1] in stop_words and words[w+2] in stop_words:
                filtered_query.append(words[w].lower())
            elif w>0 and w<len(words)-1 and words[w] in stop_words and words[w+1] in stop_words and words[w-1] in stop_words:
                filtered_query.append(words[w].lower())
            elif w>1 and words[w] in stop_words and words[w-1] in stop_words and words[w-2] in stop_words:
                filtered_query.append(words[w].lower())
        return filtered_query

    """
        this function implements Porter stemming which reduces each words to it reduced form 
    """
    def reducedQuery_stemming(self, query1):
        ps = PorterStemmer()
        Stemmed_query = []
        for w in query1:
            Stemmed_query.append(ps.stem(w))

        return Stemmed_query



