import json
import os, sys
from math import log10, sqrt
from collections import defaultdict

class TfIdf:
	def __init__(self, processed_corpus_path, inverted_index_path, key_ordering, file_num):
		self.processed_corpus_path = processed_corpus_path
		self.inverted_index_path = inverted_index_path
		self.key_ordering = key_ordering
		self.file_num = file_num

	def tf(self):
		"""
		counts and stores the frequency of a term
		in a document and write it to the same
		document in following order:
		{
			termi: n,
			termj: m,
			...
		}
		n, m are frequencies of termi, termj resp.
		in the document currently being processed
		"""
		for folder in os.listdir(self.processed_corpus_path):
			dir_path = os.path.join(os.sep, self.processed_corpus_path, folder)
			for a_file in os.listdir(dir_path):
				file_path = os.path.join(os.sep, dir_path, a_file)
				term_freq={}
				with open (file_path, 'r') as infile:
					words = infile.readlines()
					for word in words:
						term_freq[word[:-1]] = 0 	
						# ^ -1 to remove '\n' from the end of the word
					for word in words:
						term_freq[word[:-1]] += 1
				with open (file_path, 'w') as dumpfile:
					json.dump(term_freq, dumpfile, ensure_ascii=False)
			print(folder+" tf'ed")

	def inverted_index(self):
		"""
		creates a json file which stores id
		of all documents in which each term
		is present:

		{
			termi:[d1, d2, ...dk],
			termj:[d2, d3, ...dm],
			...
		}
		note that size of list say [d1, d2, ..., dk]
		corresponds to document-freq(df) of termi

		here terms(termi, termj) and documents
		in their lists both are in increasing 
		order to reduce the search time
		"""
		doc_list = defaultdict(list)
		i=0
		for folder in os.listdir(self.processed_corpus_path):
			dir_path = os.path.join(os.sep, self.processed_corpus_path, folder)
			for a_file in os.listdir(dir_path):
				file_path = os.path.join(os.sep, dir_path, a_file)
				with open (file_path, 'r') as infile:
					freq_dict = json.load(infile)
					for key, value in freq_dict.items():
						doc_list[key].append(os.path.join(os.sep, folder, a_file))
			i+=1
			print("Size in MB: "+str(sys.getsizeof(doc_list)/(1024*1024))+". "+folder+" "+str(256-i)+" more to go")
		
		words = sorted(doc_list)
		for word in words:
			doc_list[word].sort()

		print("creating inverted index...")
		with open (self.inverted_index_path, 'w') as dumpfile:
			json.dump(doc_list, dumpfile, ensure_ascii=False)
		print("inverted index created!")
		print("creating ordering file...")
		with open (self.key_ordering, 'w') as dumpfile:
			json.dump(words, dumpfile, ensure_ascii=False)
		print("ordering file created!... Done.")
		
	def tfidf(self):
		"""
		calculates idf(uniqueness) of each word using
		idf_of_term = log10(N/d)
			N: total docs
			d: number of docs in which term t appers
		multiplies uniqueness by term-freq: (1+log10(tf)),
		normalizes it by cosine normalization: 
		1/(sqrt(w1*w1 + w2*w2 +...))
		and stores it in a json file:
		{
			term1: tf_idf weight1,
			term2: tf_idf weight2,
			...
		}
		"""
		uniqueness={}
		order=[]
		with open(self.key_ordering, 'r') as infile:
			order = json.load(infile)
		with open(self.inverted_index_path, 'r') as infile:
			inv_idx = json.load(infile)
			for word in order:
				uniqueness[word] = log10(self.file_num/len(inv_idx[word]))
		
		# traversing through all files in the directories
		for folder in os.listdir(self.processed_corpus_path):
			dir_path = os.path.join(os.sep, self.processed_corpus_path, folder)
			for a_file in os.listdir(dir_path):
				file_path = os.path.join(os.sep, dir_path, a_file)
				weights={}
				divide_by = 0
				with open (file_path, 'r') as infile:
					tfs = json.load(infile)
					# multiply tf and idf
					for word, term_freq in tfs.items():
						term_freq = (1+log10(term_freq))*uniqueness[word]
						tfs[word] = term_freq
						divide_by += (term_freq**2)

					# normalize the tfidf weights
					divide_by = sqrt(divide_by)
					for word, tfidf in tfs.items():
						tfs[word] /= divide_by
					weights = tfs
				with open (file_path, 'w') as dumpfile:
					json.dump(weights, dumpfile, ensure_ascii=False)

	
if __name__=='__main__':
	# test
	processed_corpus_path = '/home/tex/Documents/IR/proc_data'
	inverted_index_path = '/home/tex/Documents/IR/inverted_index'
	sorted_keys = '/home/tex/Documents/IR/order'
	file_num = 9
	
	# final
	# processed_corpus_path = '/home/dennis/Documents/dev/IR/WES/arwiki_parser/processed_corpus'
	# inverted_index_path = '/home/dennis/Documents/dev/IR/WES/arwiki_parser/inverted_index'
	# sorted_keys = '/home/dennis/Documents/dev/IR/WES/arwiki_parser/order'
	# file_num = 96079

	ti = TfIdf(processed_corpus_path, inverted_index_path, sorted_keys, file_num)
	# ti.tf()
	ti.inverted_index()
	# ti.tfidf()