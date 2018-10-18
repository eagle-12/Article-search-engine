import json
import os
from collections import defaultdict
from math import log10, sqrt
from nltk.stem.isri import ISRIStemmer
from nltk.tokenize import wordpunct_tokenize as w_tokenizer


def loadModel(inverted_index_path):
	with open (inverted_index_path, 'r') as loadfile:
		model = json.load(loadfile)
	return model

class QueryProcessor:
	def __init__(self, query, model, processed_corpus_path):
		self.model = model
		self.processed_corpus_path=processed_corpus_path
		self.query = query
		self.query_tokens=[]
		self.query_term_freq={}
		self.term_weights={}
		self.stemmer = ISRIStemmer()
		self.threshold = 0.005
		self.top_res = 5
		self.ar_stop_words=[]
		with open ("/home/tex/Documents/IR/Wikipedia-Search-Engine/project/rankretrievalmodel/Arabic/stop_words", 'r') as infile:
			self.ar_stop_words=[word[:-1] for word in infile.readlines()]

		self.tokenize() 
		self.remove_stop_words()
		self.stem_tokens()
		self.term_freq()
		self.tfidf()

	def tokenize(self):
		self.query_tokens = w_tokenizer(self.query)

	def remove_stop_words(self):
		self.query_tokens = [token for token in self.query_tokens 
							if not 
							(token in self.ar_stop_words or len(token)==1)]
	
	def stem_tokens(self):
		self.query_tokens = [self.stemmer.stem(token) 
							for token in self.query_tokens]

	def term_freq(self):
		self.query_term_freq = {token: 0 for token in self.query_tokens}
		for token in self.query_tokens:
			self.query_term_freq[token] += 1

	def tfidf(self):
		divide_by=1
		for term, freq in self.query_term_freq.items():
			doc_freq=0
			try:
				doc_freq = len(self.model[term])
				uniqueness = log10(len(self.model)/doc_freq)
				self.term_weights[term]=uniqueness*(1+log10(freq))
				#normalization
				divide_by += self.term_weights[term]**2
			except:
				self.term_weights[term]=0
		divide_by = sqrt(divide_by)
		self.term_weights = {term: weight/divide_by 
							for term, weight in self.term_weights.items()}
	
	def search(self):
		score={}
		score=defaultdict(lambda: 0, score)
		
		for term, weight in self.term_weights.items():
			doc_list=[]
			try:
				doc_list = self.model[term]
			except:
				pass
			for doc in doc_list:
				file_path = os.path.join(os.sep, self.processed_corpus_path, doc[1:])
				with open (file_path, 'r') as loadfile:
					file = json.load(loadfile)
					score[doc] += weight*file[term]
		
		ans=[]
		for doc, weight in score.items():
			if weight>self.threshold:
				ans.append((doc, weight))
		ans = sorted(ans, reverse=True, key=lambda x: x[1])
		if len(ans)>self.top_res:
			return ans[:self.top_res]
		else: return ans


if __name__=='__main__':
	#raw_corpus_path = '/home/dennis/Documents/dev/IR/testdata'
	processed_corpus_path = '/home/tex/Documents/IR/proc_data'
	inverted_index_path = '/home/tex/Documents/IR/inverted_index'

	# inverted_index_path = '/home/dennis/Documents/dev/IR/WES/arwiki_parser/inverted_index'
	# raw_corpus_path = '/home/dennis/Documents/dev/IR/WES/arwiki_parser/arabic_corpus'
	# processed_corpus_path = '/home/dennis/Documents/dev/IR/WES/arwiki_parser/processed_corpus'
	model = loadModel(inverted_index_path)
	"""while (1):
		query = input("Enter the query: ")
		qp = QueryProcessor(query, model, processed_corpus_path)
		ans = qp.search()
		print(ans)"""
