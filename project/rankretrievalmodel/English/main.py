#from query_processing import query_reduction as qr
#from document_processing import document_reduction as dr
#from indexing import indexing as indx

import json
import math
import operator

"""runQuery = qr()
filter_query = runQuery.reducedQuery_stopwords()
#print(filter_query)
#print(runQuery.reducedQuery_stemming(filter_query))


#this line is used for document processing which includes stemming, removal of stop words, case folding and removal of punctuation
runDoc = dr()
path = '/home/tex/Downloads/wikiextractor/Output1'
runDoc.decReduction(path)



runIndexing = indx()
runIndexing.file_indexing()
"""

class QueryProcessor:

	# load the inverted index and inverse document frequency file
	def __init__(self,addr_invert_idx,addr_idf):
		self.score = {}
		self.q_score = {}
		with open(addr_invert_idx) as json_data:
			self.inver_idx = json.load(json_data)
			json_data.close()
		with open(addr_idf) as json_data:
			self.idf = json.load(json_data)
			json_data.close()

	# generate the vector in the vector space model corresponding to query
	def score_query(self,input_query):
		self.query = input_query.split(' ')
		self.mod = 0
		for i in range(0,len(self.query)):
			if self.query[i] in self.q_score.keys():
				continue
			else:
				ct = 0
				for j in range(i,len(self.query)):
					if(self.query[j]==self.query[i]):
						ct=ct+1
				self.q_score[self.query[i]] = ct
				self.mod = self.mod + ct*ct

		for term in self.q_score:
			self.q_score[term] = (self.q_score[term])/(math.sqrt(self.mod))

		print(self.q_score)

	"""folder_addr containing the tf of individual docs. Generate the dict containing the doc-Id of all the docs containing any of the terms in the query.
	Using the vector representing the query and tf-idf value of the docs determine the proximity between the vector representing the query and vector representing
	the docs(cosine similarity)"""

	def score_docs1(self,folder_addr):
		"""determines all the documents containing any of the terms present 
		   in the query and initializes their score to zero which is updated 
		   						in each step"""
		for term in self.q_score.keys():
			for j in range(0,len(self.inver_idx[term])):
				if self.inver_idx[term][j] in self.score.keys():
					continue
				else:
					self.score[self.inver_idx[term][j]] = 0
		#print(self.score)

		#print(self.score.keys())
		for doc in self.score.keys():
			mod = 0
			for term in self.q_score.keys():
				"""obtain the documents term frequency list"""
				if doc[0]==',':
					path = folder_addr+'/'+doc[1:][:-1]
				else:
					path = folder_addr+'/'+doc[:-1]

				with open(path) as json_data:
					self.doc_indx = json.load(json_data)
					json_data.close()
				try:
					self.score[doc] += ((self.q_score[term]) * (math.log(1 + self.doc_indx[term])) * (self.idf[term]))
					mod = mod + (math.log(1 + self.doc_indx[term])) * (self.idf[term]) * (math.log(1 + self.doc_indx[term])) * (self.idf[term])
				except:
					pass
				#print(term, doc, self.score[doc], self.q_score[term], self.doc_indx[term])#self.idf[term])
				"""update the score of the particular document corresponding to the particular term of the query"""
				#self.score[doc] += ((self.q_score[term])*(math.log(1+self.doc_indx[term]))*(self.idf[term]))
				#mod = mod + (math.log(1+self.doc_indx[term]))*(self.idf[term])*(math.log(1+self.doc_indx[term]))*(self.idf[term])

			self.score[doc] = (self.score[doc])/math.sqrt(mod)

	def return_docs(self):

		"""sorting the docs in descending orderbased on their rank values"""
		self.score = sorted(self.score.items(),key=operator.itemgetter(1),reverse=True)
		return self.score

if __name__=='__main__':
	input_query = input()
	inver_index = '/home/tex/Documents/IR/Inverted_Index/inverted_indx.txt'
	add_idf = '/home/tex/Documents/IR/Inverted_Index/idf.txt'
	folder_addr ='/home/tex/Documents/IR/Final_Output1000'
	process = QueryProcessor(inver_index,add_idf)
	process.score_query(input_query)
	process.score_docs1(folder_addr)
	docs = process.return_docs()
	print(docs)
