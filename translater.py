#!/usr/bin/env python
# encoding: utf-8
# CS124 Homework 6 Translate
# David Beam (dbeam@stanford.edu) Mark Schramm (mschramm@stanford.edu)

import itertools as it
import re, collections, string, io

def loadList(file_name):
    """Loads text files as lists of lines. Used in evaluation."""
    with io.open(file_name, "r", encoding="utf-8") as f:
	l = [line.strip() for line in f]
    return l


class EMTrainer():
	def __init__(self):
		self.englishList = loadList("es-en/train/europarl-v7.es-en.en")
		self.spanishList = loadList("es-en/train/europarl-v7.es-en.es")
		self.transProbs = collections.Counter()


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
				if span_word.encode('utf-8') not in self.transProbs:
                    			self.transProbs[span_word.encode('utf-8')] = collections.Counter()
				length = len(eng_words)
				for i in xrange(length):
					self.transProbs[span_word.encode('utf-8')][eng_words[i].encode('utf-8')] += 1
					if i < length - 1:
						self.transProbs[span_word.encode("utf-8")][eng_words[i].encode("utf-8") + " " + eng_words[i + 1].encode("utf-8")] += 1
					if i < length - 2:
                                                self.transProbs[span_word.encode("utf-8")][eng_words[i].encode("utf-8") + " " + eng_words[i + 1].encode("utf-8") + " " +eng_words[i+2].encode("utf-8")] += 1
			''' here are examples of how to use encoding, doooo not delete or I'll cry
			if u"\u00F3" in span_sent:
				print span_sent.encode('utf-8')
			if 'Elmar' in eng_sent:
				eng_sent = eng_sent.replace(" " + u'\u2019' + " ", "'")
				print eng_sent.encode('utf-8')
			'''
		print self.transProbs['de']
x = EMTrainer()
x.wordTrans()
