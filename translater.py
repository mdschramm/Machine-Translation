#usr/bin/env python
# encoding: utf-8
# CS124 Homework 6 Translate
# David Beam (dbeam@stanford.edu) Mark Schramm (mschramm@stanford.edu)

import itertools as it
import re, collections, string, io, operator

# Utility functions
def loadList(file_name):
    """Loads text files as lists of lines. Used in evaluation."""
    with io.open(file_name, "r", encoding="utf-8") as f:
	l = [line.strip() for line in f]
    return l
 
def normalizeVec(vec):
	mag = sum(vec)
	for i in xrange(len(vec)):
		vec[i] = vec[i]/mag

def removeNonAlphas(sentence):
	for word in sentence:
		if not re.search('[a-zA-Z]', word):
			sentence.remove(word)
	return sentence

class EMTrainer():

	def __init__(self):
		self.englishList = loadList("es-en/train/europarl-v7.es-en.en")
		self.spanishList = loadList("es-en/train/europarl-v7.es-en.es")

		# default dicts, so no need to check if an element exists in a dict
		self.transCounts = collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0))
		self.transProbs = collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0))
		self.transProbsZeros = None
		self.Iterations = 20
		self.eng_vocab = set([])
		self.prev = [float('inf')] * 100
		self.sample = []
		self.keys = []
		self.eta = .01
	
	def normalizeTable(self, table):
		for span_word in table:
			row_sum = sum(table[span_word].values())
			for eng_word in table[span_word]:
				table[span_word][eng_word] /= row_sum # len(self.eng_vocab)


	def initializeTables(self):
		for i in xrange(len(self.spanishList)):
			eng_sent = self.englishList[i].replace(" " + u'\u2019' + " ", "'")
			span_sent = self.spanishList[i]
			eng_words = eng_sent.split(" ")
			span_words = span_sent.split(" ")
					
			#updates sentence in original list to contained stripped punctuation free words
			self.englishList[i] = removeNonAlphas(eng_words)
			self.spanishList[i] = removeNonAlphas(span_words)
			
			for span_word in span_words:
				for eng_word in eng_words:

						# in sets all elements are unique, so each word appears only once
						self.eng_vocab.add(eng_word)

						self.transCounts[span_word][eng_word] = 1.0
						self.transProbs[span_word][eng_word] = 0.0

			if i % 1000 == 0:
				print len(self.eng_vocab)
				#print i

		self.transProbsZeros = self.transProbs.copy()
		
		# Normalization step
		self.normalizeTable(self.transCounts)

	def sentenceProdAndSums(self, eng_words, span_words):
		prod = 1.0
		sums = []
		for ej in eng_words:
			term = 0.0
			for si in span_words:
				term += self.transCounts[si][ej]
			sums.append(term)
			prod *= term
		return prod, sums


	'''
	One iteration of the EM algorithm. Sets transCounts to the new 
	updated probability table, and resets transProbs to a list of 0's
	'''
	def updateTable(self):
		
		length = len(self.englishList)
		for x in xrange(length):
			eng_words = self.englishList[x]
			span_words = self.spanishList[x]

			# moved out function that calculates the product and individual sums for each english word
			prod, sums = self.sentenceProdAndSums(eng_words, span_words)

			for i in xrange(len(eng_words)):
				pairs = []
				for j in xrange(len(span_words)):
					pairs.append(self.transCounts[span_words[j]][eng_words[i]] * prod/sums[i])
				normalizeVec(pairs)
				for j in xrange(len(span_words)):
					self.transProbs[span_words[j]][eng_words[i]] += pairs[j]
			
			#print 'transProbs ', x
		
		self.normalizeTable(self.transProbs)
		self.transCounts = self.transProbs.copy()
		self.transProbs = self.transProbsZeros.copy()

	def alignMonster(self):

		#builds list for table of unique words, processes sentences for later use		
		self.initializeTables()
		
		for i in range(self.Iterations):
			self.updateTable()
			if i == 0:
				counter = 0
				for key in self.transProbs:
					print key.encode('utf-8')
					if counter == 100:
						break
					self.keys.append(key)
					counter += 1
			'''
			sample = []
			sample.append(self.transProbs['casa']['house'])
			#sample.append(self.transProbs['cuchara']['spoon'])
			sample.append(self.transProbs['el']['the'])
			'''
			counter = 0
			for y in xrange(len(self.keys)):
				mk = max(self.transProbs[self.keys[y]], key=self.transProbs[self.keys[y]].get)
				v = self.transProbs[self.keys[y]][mk]
				print self.keys[y].encode('utf8'), v, abs(v - self.prev[y])
				if abs(v - self.prev[y]) < self.eta:
					counter += 1
				self.prev[y] = v
			print 'counter ', counter
			print 'iter ', i
			if counter >= 90:
				break
			'''
			stop = True
			for j in xrange(len(sample)):
				if abs(sample[j] - self.prev[j]) > self.eta:	
					self.prev = sample
					stop = False
			'''
			#builds masterlist	
		'''
		# masterEngWords = []
		# masterSpanWords = []
			for word in span_words:
				if word not in masterSpanWords:
					masterSpanWords.append(word)
			for word in eng_words:
				if word not in masterEngWords:
					masterEngWords.append(word)
			if i % 1000 == 0:
				print i
		print 'out of loop 1'
		length = len(masterEngWords)
		#itiializes translation table
		for word in masterSpanWords:
			self.transCounts[word] = {}
			self.transProbs[word] = {}
			for eng_word in masterEngWords:
				self.transCounts[word][eng_word] = 1.0/length
				self.transProbs[word][eng_word] = 0.0
		
		print 'out of loop 2'
		'''




	def wordTrans(self):
		for i in xrange(len(self.spanishList)):
			print i	
			eng_sent = self.englishList[i].replace(" " + u'\u2019' + " ", "'")
			#.translate(string.maketrans("",""), string.punctuation) (translate line not needed with
			# regexes below, also stopped compling for some reason replace handles '
			#re.sub(r'[^\x00-\x7F]+','\'', eng_sent)

			span_sent = self.spanishList[i]
			eng_words = eng_sent.split(" ")
			span_words = span_sent.split(" ")

			#loops below make bag of words, special cases yet to be accounted for 1 letter accented words? weird markers such as &quote
			#word.decode("utf-8") # instead of just word
			for word in eng_words:
				if re.search('[a-zA-Z]', word) == None:
					eng_words.remove(word)
			for word in span_words:
                                if re.search('[a-zA-Z]', word) == None:
                                        span_words.remove(word)
			for span_word in span_words:
				if span_word.encode('utf-8') not in self.transCounts:
                    			self.transCounts[span_word.encode('utf-8')] = collections.Counter()
				length = len(eng_words)
				for i in xrange(length):
					self.transCounts[span_word.encode('utf-8')][eng_words[i].encode('utf-8')] += 1
					if i < length - 1:
						self.transCounts[span_word.encode("utf-8")][eng_words[i].encode("utf-8") + " " + eng_words[i + 1].encode("utf-8")] += 1
					if i < length - 2:
                                                self.transCounts[span_word.encode("utf-8")][eng_words[i].encode("utf-8") + " " + eng_words[i + 1].encode("utf-8") + " " +eng_words[i+2].encode("utf-8")] += 1
			
			''' here are examples of how to use encoding, doooo not delete or I'll cry
			if u"\u00F3" in span_sent:
				print span_sent.encode('utf-8')
			if 'Elmar' in eng_sent:
				eng_sent = eng_sent.replace(" " + u'\u2019' + " ", "'")
				print eng_sent.encode('utf-8')
			'''
		#print self.transCounts['de']
	def normalize(self):
		i = 0
		print self.transCounts
		print "halp"
		self.transProbs = dict(self.transCounts)
		#print self.transProbs['de']
		for span_word in self.transProbs:
			mag = 0
			for eng_word in self.transCounts[span_word]:
				mag += self.transCounts[span_word][eng_word]
			for eng_word in self.transProbs[span_word]:
				self.transProbs[span_word][eng_word] = float(self.transProbs[span_word][eng_word])/float(mag)
			i += 1
			print i
		for key in self.transProbs:
			print key
		print self.transProbs['comida']
x = EMTrainer()
x.alignMonster()
#x.normalize()
