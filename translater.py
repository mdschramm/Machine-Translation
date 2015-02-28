#usr/bin/env python
# encoding: utf-8
# CS124 Homework 6 Translate
# David Beam (dbeam@stanford.edu) Mark Schramm (mschramm@stanford.edu)

''' 
	here are examples of how to use encoding, doooo not delete or I'll cry
	if u"\u00F3" in span_sent:
		print span_sent.encode('utf-8')
	if 'Elmar' in eng_sent:
		eng_sent = eng_sent.replace(" " + u'\u2019' + " ", "'")
		print eng_sent.encode('utf-8')
'''

import itertools as it
import re, collections, string, io, operator
import codecs

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
		self.conv_per = 90
	
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
			if counter >= self.conv_per:
				break
			
def testModel():
	#es_dev = loadList('es-en/dev/newstest2012.es')
	es_dev = loadList('es-en/test/newstest2013.es')
	file_content = ''
	life_count = 0
	for span_line in es_dev:
		span_line = removeNonAlphas(span_line.split(" "))

		translated_line = ''
		for word in span_line:
			if word in x.transProbs:
				translated_word = max(x.transProbs[word], key=x.transProbs[word].get).encode('utf8')
			else:
				translated_word = word.encode('utf8')
			translated_line += (translated_word + ' ')
		life_count += 1
		if life_count % 1000 == 0:
			print translated_line
		translated_line.strip()
		translated_line += '.\n'
		file_content += translated_line.decode('utf8')

	open('Output.txt', 'w').close()
	text_file = codecs.open("Output.txt", "w", "utf-8")
	text_file.write(file_content)
	text_file.close()

x = EMTrainer()
x.alignMonster()
testModel()




