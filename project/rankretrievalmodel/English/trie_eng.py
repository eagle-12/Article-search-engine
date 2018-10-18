import pickle
import json
import os

suggestions = []

class Node:
	"""Creates a Node for the Trie"""
	def __init__(self):
		self.child=[None]*36
		self.isEnd = False
		self.map = {}
		idx = 0
		for i in range(97,123):
			self.map[idx] = chr(i)
			idx = idx+1

		for i in range(0,10):
			self.map[idx] = str(i)
			idx = idx+1


	def all_words(self,prefix):

		"""fetches all the terms starting with given prefix and appends them into a list named suggestions"""
		if self.isEnd==True:
			suggestions.append(prefix)

		for i in range(36):
			if self.child[i] and i<26:
				self.child[i].all_words(prefix + self.map[i])
			elif self.child[i]:
				self.child[i].all_words(prefix + self.map[i+1])
		
class Trie:

	def __init__(self):
		self.root = Node()

	def index(self,ch):
		"""Determines the index coressponding to a given starting character"""
		if ord(ch)>=97 and ord(ch)<=122:
			return ord(ch)-ord('a')
		else:
			return 25+ord(ch)-ord('0')

	def insert(self,ele):

		"""inserts an element ele in the Trie"""
		l = len(ele)
		curr = self.root
		for i in range(l):
			#looks for the first character of the element in trie
			idx = self.index(ele[i])
			if not curr.child[idx]:
				curr.child[idx]=Node()

			curr = curr.child[idx]

		curr.isEnd = True

	def search(self,key):
		"""Looks for a particular element in trie i.e. returns True if Element found else return False"""
		curr = self.root
		l = len(key)
		for i in range(l):
			idx = self.index(key[i])
			if not curr.child[idx]:
				return False
			curr = curr.child[idx]

		return curr.isEnd and curr!=None

	def autocomplete(self,query):

		"""to provide suggestions for completion of the given word"""
		self.curr = self.root
		self.l = len(query)

		suggestions[:] = []

		for i in range(self.l):
			idx = self.index(query[i])
			if not self.curr.child[idx]:
				return False
			self.curr = self.curr.child[idx]

		self.curr.all_words(query)

		return suggestions



"""to save a Trie object in the file"""
def save_object(obj,filename):
	with open(filename,'wb') as output:
		pickle.dump(obj,output,pickle.HIGHEST_PROTOCOL)


"""to load pickle file of Trie Object"""
def load_object(filename):
	with open(filename,"rb") as input_file:
		obj = pickle.load(input_file)
		return obj

if __name__=='__main__':
	t = Trie()
	addr_tf = '/home/tex/Documents/IR/Tries/'
	files = os.listdir('/home/tex/Documents/IR/Tries/')
	keys = []
	for filename in files:
		with open(addr_tf+filename) as json_data:
			idf = json.load(json_data)
			for key in idf.keys():
				keys.append(str(key))

			json_data.close()

	print(len(keys))
	#keys = ["the","a","there","any","answer","ans9w","ffhhhgv","ffuffy",'peerreview', 'system', 'rest', 'guid','aquina','emot', 'length', 'controversi', 'cultur', 'us', 'cri', 'kaplan', 'furnitur', 'compliment', 'magazin', 'jewish', 'plan''around', 'desper', 'know', 'employ', 'recast', 'garri', 'privat', 'open', 'ayin', 'limit', 'compel', 'contact', 'inspir', 'reader', 'peerreview', 'system', 'rest', 'guid', 'aquina', 'emot', 'length', 'controversi', 'cultur', 'us', 'cri', 'kaplan', 'furnitur', 'compliment', 'magazin', 'jewish', 'plan', 'such', 'rich', 'promot', 'month', 'cancer', 'michael', 'an', 'casket', 'live', 'splendor', 'nonobserv', 'studio', 'rude', 'permiss', 'indian', 'ford', 'cult', 'experi', 'favor', 'cite']

	for key in keys:
		key_processed = ""
		for i in range(0,len(key)):
			if ord(key[i])>=97 and ord(key[i])<=122:
				key_processed+=key[i]
			elif (ord(key[i])-ord('0'))>=0 and (ord(key[i])-ord('0'))<=9:
				key_processed+=key[i]
		t.insert(key_processed)

	"""to save trie object as a pickle file. The trie contains """
	#save_object(t,"/home/nikhil/searchengine/Article-Search-Engine/project/rankretrievalmodel/English/a.pkl")

	"""to load the trie object saved as pickle file"""
	#trie = load_object("/home/nikhil/searchengine/Article-Search-Engine/project/rankretrievalmodel/English/a.pkl")


	x = t.search("england")
	print(x)

	t.autocomplete("engl")
	print(suggestions)
