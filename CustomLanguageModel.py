import math, collections

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.trigramCounts = collections.defaultdict(lambda: 0)
    self.unigramTotal = 0
    self.bigramTotal = 0
    self.trigramTotal = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    #    for sentence in corpus.corpus:
    #       for datum in sentence.data:  
    #         word = datum.word
    for sentence in corpus.corpus:
        for i in xrange(0, len(sentence.data) - 2):
                tritoken = (sentence.data[i].word, sentence.data[i + 1].word, sentence.data[i + 2].word)
                bitoken = (sentence.data[i].word, sentence.data[i + 1].word)
                token = sentence.data[i].word
		self.trigramCounts[tritoken] = self.trigramCounts[tritoken] + 1
                self.bigramCounts[bitoken] = self.bigramCounts[bitoken] + 1
                self.unigramCounts[token] = self.unigramCounts[token] +1
                self.unigramTotal += 1
                self.bigramTotal +=1
                self.trigramTotal +=1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for i in xrange(0, len(sentence) - 2):
        trip = (sentence[i], sentence[i+1], sentence[i + 2])
        tup = (sentence[i], sentence[i+1])
        tricount = self.trigramCounts[trip]
	bicount = self.bigramCounts[tup]
        unicount = self.unigramCounts[sentence[i + 1]]
	tup2 = (sentence[i + 1], sentence[i+2])
        bicount2 = self.bigramCounts[tup2]
        if tricount > 0:
                score += math.log(tricount)
                score -= math.log(bicount)
        elif bicount2 > 0:
                score += math.log(bicount2)
                score += math.log(.4)
                score -= math.log(unicount)
        else:
	 	unicount = self.unigramCounts[sentence[i + 2]] + 1
		score += math.log(unicount)
		score += math.log(.4)
		score += math.log(.4)
		score -= math.log(self.unigramTotal + len(self.unigramCounts))
    return score
