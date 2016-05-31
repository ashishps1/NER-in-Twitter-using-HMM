import sys
from collections import defaultdict
import math
from countFreq import *

class Hmm(object):

    def __init__(self, n=3):
        assert n>=2, "Expecting n>=2."
        self.n = n
        self.emissionCounts = defaultdict(int)
        self.ngramCounts = [defaultdict(int) for i in range(self.n)]
        self.allStates = set()

    def train(self, corpus_file):
        
        ngramIterator = get_ngrams(sentenceIterator(corpusIterator(corpus_file)), self.n)

        for ngram in ngramIterator:
    
            assert len(ngram) == self.n, "ngram in stream is %i, expected %i" % (len(ngram, self.n))

            tagsonly = tuple([neTag for word, neTag in ngram])            
            for i in range(2, self.n+1):
                self.ngramCounts[i-1][tagsonly[-i:]] += 1
            
            if ngram[-1][0] is not None:
                self.ngramCounts[0][tagsonly[-1:]] += 1
                self.emissionCounts[ngram[-1]] += 1

            if ngram[-2][0] is None:
                self.ngramCounts[self.n - 2][tuple((self.n - 1) * ["*"])] += 1

    def write_counts(self, output, printngrams=[1,2,3]):
     
        for word, neTag in self.emissionCounts:            
            output.write("%i WORDTAG %s %s\n" % (self.emissionCounts[(word, neTag)], neTag, word))

        for n in printngrams:            
            for ngram in self.ngramCounts[n-1]:
                ngramstr = " ".join(ngram)
                output.write("%i %i-GRAM %s\n" %(self.ngramCounts[n-1][ngram], n, ngramstr))

    def read_counts(self, corpusfile):

        self.n = 3
        self.emissionCounts = defaultdict(int)
        self.ngramCounts = [defaultdict(int) for i in range(self.n)]
        self.allStates = set()

        for line in corpusfile:
            parts = line.strip().split(" ")
            count = float(parts[0])
            if parts[1] == "WORDTAG":
                neTag = parts[2]
                word = parts[3]
                self.emissionCounts[(word, neTag)] = count
                self.allStates.add(neTag)
            elif parts[1].endswith("GRAM"):
                n = int(parts[1].replace("-GRAM",""))
                ngram = tuple(parts[2:])
                self.ngramCounts[n-1][ngram] = count


if __name__ == "__main__":

	inputF = 'train.txt'

    try:
        input = file(inputF,"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    counter = Hmm(3)
   
    counter.train(inputF)
   
    counter.write_counts(sys.stdout)
