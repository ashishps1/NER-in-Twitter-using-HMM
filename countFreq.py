import sys
from collections import defaultdict
import math

def corpusIterator(corpus_file):
    
    l = corpus_file.readline()
    while l:
        line = l.strip()
        if line:
            fields = line.split(" ")
            ne_tag = fields[-1]
            word = " ".join(fields[:-1])
            yield word, ne_tag
        else:
            yield (None, None)                        
        l = corpus_file.readline()

def sentenceIterator(corpus_iterator):
   
    current_sentence = []
    for l in corpus_iterator:        
            if l==(None, None):
                if current_sentence:
                    yield current_sentence
                    current_sentence = []
                else:
                    sys.stderr.write("WARNING: Got empty input file/stream.\n")
                    raise StopIteration
            else:
                current_sentence.append(l)

    if current_sentence:
        yield current_sentence

def get_ngrams(sent_iterator, n):
    
    for sent in sent_iterator:
         w_boundary = (n-1) * [(None, "*")]
         w_boundary.extend(sent)
         w_boundary.append((None, "STOP"))
         ngrams = (tuple(w_boundary[i:i+n]) for i in range(len(w_boundary)-n+1))
         for n_gram in ngrams:
            yield n_gram        
