import math, collections

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
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
      	for i in xrange(0, len(sentence.data) - 1):
        	token = (sentence.data[i].word, sentence.data[i + 1].word)
        	self.bigramCounts[token] = self.bigramCounts[token] + 1
        	self.total += 1
  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    for i in xrange(0, len(sentence) - 1):
	tup = (sentence[i], sentence[i+1])
        count = self.bigramCounts[tup] + 1
        score += math.log(count)
        score -= math.log(self.total + len(self.bigramCounts))
    return score
