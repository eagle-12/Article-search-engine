import os, errno
from bisect import bisect_left
from nltk.stem.isri import ISRIStemmer
from nltk.tokenize import wordpunct_tokenize as w_tokenizer

class TextProcessor:
	def __init__(self, raw_corpus_path, processed_corpus_path):
		self.raw_corpus_path = raw_corpus_path
		self.processed_corpus_path = processed_corpus_path

		# initializing stop words and punctuations
		self.ar_stop_words=[]
		with open ("stop_words", 'r') as infile:
			self.ar_stop_words=[word[:-1] for word in infile.readlines()]

		self.ar_stop_words.sort()
		
	def preprocess(self):
		"""
		Removes characters of languages other than
		Arabic which got in files during scraping
		"""
		# traversing through all the files in the directory
		for folder in os.listdir(self.raw_corpus_path):
			dir_path = os.path.join(os.sep, self.raw_corpus_path, folder)
			for a_file in os.listdir(dir_path):
				file_path = os.path.join(os.sep, dir_path, a_file)
				string=""
				with open (file_path, 'r') as infile:
					lines = infile.readlines()
					for line in lines:
						for char in line:
							asci = ord(char)
							if ((asci <= 1791 and asci >= 1536) or #retain arabic
								 (asci == 32 or asci == 10) or 	   #retain space and \n
								 (asci >= 48 and asci <= 57)):	   #retain numbers
								string+=char
				with open (file_path, 'w') as outfile:
					outfile.write(string)
			print(folder+" processed")
	

	def remove_stop_words(self):
		"""
		Removes the arabic stop words from the
		files
		stop-words are loaded from an input file
		"""
		def not_stop_word(word, lo=0):
			"""
			Searches for the word in self.ar_stop_words.
			Uses binary search to reduce search time.
			return value:
				 -1 if word is not a stop-word
				 else its position in the stop-word list 
			"""
			hi = len(self.ar_stop_words)
			pos = bisect_left(self.ar_stop_words, word, lo, hi)
			return (pos if pos != hi and self.ar_stop_words[pos] == word else -1)

		def initialize_dirs(folder):
			"""
			Initialize the reading and writing directories.
			If writing directory does not exist create it.
			"""
			reading_dir = os.path.join(os.sep, self.raw_corpus_path, folder)
			writing_dir = os.path.join(os.sep, self.processed_corpus_path, folder)
			if not os.path.exists(writing_dir):
				try:
					os.makedirs(writing_dir)
				except OSError as e:
					if e.errno != errno.EEXIST:
						raise
			return (reading_dir, writing_dir)

		# reading from reading_dir and writing to writing_dir
		# while eliminating stop_words
		for folder in os.listdir(self.raw_corpus_path):
			(reading_dir, writing_dir) = initialize_dirs(folder)
			for a_file in os.listdir(reading_dir):
				reading_file = os.path.join(os.sep, reading_dir, a_file)
				writing_file = os.path.join(os.sep, writing_dir, a_file)
				to_write = []
				with open (reading_file, 'r') as infile:
					lines = infile.read()
					words = w_tokenizer(lines)
					for word in words:
						if  not_stop_word(word) == -1:
							to_write.append(word)

				with open (writing_file, 'w') as outfile:
					for word in to_write:
						#remove single chars
						if len(word)!=1:
							outfile.write(word+'\n')
			print(folder+" unstopped ")

	def stem_words(self):
		"""
		Stem all the words in each file	using
		ISRI Arabic stemmer based on algorithm:
			Arabic Stemming without a root dictionary.
		"""
		st = ISRIStemmer()
		for folder in os.listdir(self.processed_corpus_path):
			dir_path = os.path.join(os.sep, self.processed_corpus_path, folder)
			for a_file in os.listdir(dir_path):
				file_path = os.path.join(os.sep, dir_path, a_file)
				to_write = []
				with open (file_path, 'r') as infile:
					words = infile.readlines()
					for word in words:
						to_stem = word[:-1]
						stemmed = st.stem(to_stem)
						to_write.append(stemmed)
				# print(to_write)
				with open (file_path, 'w') as outfile:
					for word in to_write:
						outfile.write(word+'\n')
			print(folder+" stemmed ")

if __name__=='__main__':
	# test with this
	# raw_corpus_path = '/home/dennis/Documents/dev/IR/testdata'
	# processed_corpus_path = '/home/dennis/Documents/dev/IR/processdata'
	
	# run ONLY if checked
	# assuming these paths exist
	# raw_corpus_path = '/home/dennis/Documents/dev/IR/WES/arwiki_parser/arabic_corpus'
	# processed_corpus_path = '/home/dennis/Documents/dev/IR/WES/arwiki_parser/processed_corpus'
	
	tp = TextProcessor(raw_corpus_path, processed_corpus_path)
	# tp.preprocess()
	# tp.remove_stop_words()
	# tp.stem_words()