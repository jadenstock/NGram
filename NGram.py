import math
import random
import os
import collections

Start = "***!START!***"
Stop = "***!STOP!***"
UNK = "***!UNK!***"


"""This data structure holds all the parameters of the program. Acts as the root of an n-gram tri structure"""
class Ngram:
	def __init__(self, N = 3, K = 1, UNK_size = 1, UNK_probability=1):
		self.N = N #the N in N-gram
		self.number = 0
		self.children = {}

		self.UNK_size = UNK_size
		self.UNK_probability = UNK_probability
		self.K = K #this is the K smoothing constant

	def increment(self):
		self.number += 1

	#adds an example of legnth N to the NGram model
	def add_N_gram(self, example):
		self.increment()
		s = self #point to self
		for i, word in enumerate(example):
			if word not in s.children:
				s.children[word] = Gram(word)
			else:
				s.children[word].increment()
			s = s.children[word]

	#adds a sentence to the NGram model
	def add_sentence(self, sentence):
		sentence.append(Stop) #add end symbold to the sentence
		sentence = [Start for _ in xrange(self.N-1)] + sentence #add n-1 start symbols to the start of the sentence
		for i in xrange(len(sentence) - self.N + 1):
			self.add_N_gram(sentence[i:i+self.N])

	def train_from_file(self, file_name):
		UNK_set = find_UNK_set(file_name, self.UNK_size, self.UNK_probability)
		f = open(file_name, "r")
		for line in f:
			sentence = line.lower().split()

			for i,w in enumerate(sentence):#replace uncommon words with an UNK symbol
				if w in UNK_set:
					sentence[i] = UNK

			self.add_sentence(sentence)

	#returns the log of the probability of seeing an Ngram in the form of an array
	def log_prob_of_ngram(self, example):
		s = self #pointer to the root
		t = self
		
		for i, c in enumerate(example[:-1]):
			if c in s.children:
				s = s.children[c]
			else:
				s = 0
				break
		if s != 0:
			s = s.number

		for i, c in enumerate(example):
			if c in t.children:
				t = t.children[c]
			else:
				t = 0
				break
		if t != 0:
			t = t.number

		return math.log(t + self.K) - math.log(s + self.K*(len(self.children)))

	#return the log of the probability of seeing a sentence in the form of an array
	def log_prob_of_sentence(self, sentence):
		sentence.append(Stop)
		sentence = [Start for _ in xrange(self.N-1)] + sentence
		
		for i, word in enumerate(sentence): #replace unseen words with UNK
			if word not in self.children:
				sentence[i] = UNK

		return sum([self.log_prob_of_ngram(sentence[i:i+self.N]) for i in xrange(len(sentence) - self.N + 1)])


	def perplexity(self, file_name):
		M = 0
		log_prob = 0

		f = open(file_name, "r")
		for line in f:
			line = line.lower().split()
			M += len(line)
			log_prob += self.log_prob_of_sentence(line)

		l = (float(1)/M) * log_prob
		return 2**(-l)




"""this data structure holds individual words and their counts 
and a dictionary of all words that appear after the word"""
class Gram:
	def __init__(self, name):
		self.name = name
		self.number = 1
		self.children = {}

	def increment(self):
		self.number += 1


#given a file, return the set of works that appear less than k times in that file.
#there is an optional prob parameter with makes each word appearing less than k times appear in the unk set wiht that probability.
def find_UNK_set(file, k, prob = 1.0):
	words = collections.Counter()
	f = open(file, "r")
	for line in f:
		sentence = line.lower().split()
		words.update(sentence)
	UnkSet = set([x for x in words if words[x] <= k])
	return set([x for x in UnkSet if random.random() < prob])

#an example of how to run the program
#model = Ngram()
#model.train_from_file("./data/brown.train.txt")
#print(model.perplexity(".data/brown.test.txt"))
