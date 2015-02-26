#!/usr/bin/env python
# CS124 Homework 6 Translate
# David Beam (dbeam@stanford.edu) Mark Schramm (mschramm@stanford.edu)

import itertools as it
import re, collections, string, codecs

def loadList(file_name):
    """Loads text files as lists of lines. Used in evaluation."""
    with codecs.open(file_name) as f:
        l = [line.strip() for line in f]
    return l


class EMTrainer():
	def __init__(self):
		self.englishList = loadList("es-en/train/europarl-v7.es-en.en")
		self.spanishList = loadList("es-en/train/europarl-v7.es-en.es")
		self.transProbs = collections.Counter()


	def wordTrans(self):
		for i in xrange(len(self.englishList)):

			eng_sent = self.englishList[i].translate(string.maketrans("",""), string.punctuation)
			#re.sub(r'[^\x00-\x7F]+','\'', eng_sent)
			span_sent = self.spanishList[i]
			if 'ó' in span_sent:
				print span_sent	

x = EMTrainer()
x.wordTrans()