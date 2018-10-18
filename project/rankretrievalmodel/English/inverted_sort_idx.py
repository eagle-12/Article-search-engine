import os
import glob

import json
import math

class Inverted_Indx:
	def __init__(self,addr):
		self.files = os.listdir(addr)
		self.folder_addr = addr + '/'
		self.Number_Docs = len(files)
		self.indx = {}

	def index_construct(self):
		"""Creates a dictionary conatining all the terms of all the docs with each term 
		hashed to a list containing list of all the documents containing that term. The 
		docs in a particular list are sorted according to their docId"""
		for filename in self.files:
			with open(self.folder_addr+filename) as f:
				text = f.read()
				words = []
				str = ''
				fl=0
				for c in text:
					if c=='"' and fl==0:
						str+=c
						fl=1
					elif c=='"' and fl==1:
						str+=c
						fl=0
						words.append(str[1:-1])
						str=''
					elif fl==1:
						str+=c
						

				words.sort()

				for word in words:
					if word in self.indx.keys():
						self.indx[word].append(','+filename+' ')
					else:
						self.indx[word]=[]
						self.indx[word].append(filename+' ')

	
	def save_file(self,file_addr):
		"""It saves the Dictionary as a Json object in a file"""
		with open (file_addr, 'w') as invert_idx:
			json.dump(self.indx, invert_idx, ensure_ascii=False)	


if __name__=='__main__':
	addr = '/home/nikhil/wikipediasearch/termfrequencydocs'
	indx = Inverted_Indx(addr)
