'''
Created on May 7, 2016

@author: lxh5147
'''

class Feature(object):
    '''
    Key-value pair
    '''
    def __init__(self, name, value = 1.0):
        self._name = name
        self._value = value
    
    @property
    def name(self):
        return self._name
    
    @property
    def value(self):
        return self._value

class WordBreaker(object):
    '''
    word breaker to split a sentence into words
    '''
    @staticmethod
    def split(sentence):
        if not sentence:
            return []
        else:
            return [word for word in sentence.split(' ') if word]

class NGramFeatureExtractor(object):
    '''
    ngram feature extractor
    '''
    def __init__(self, n = 1, ignore_case = False, frequency_threshold = None):
        self._n = n
        self._ignore_case = ignore_case
        self._frequency_threshold = frequency_threshold
    
    def extract_features(self, lines):
        ngrams = {}
        ngram = ["" for _ in range(self._n)]
        for text in lines:
            text = text.rstrip('\n')
            if self._ignore_case:
                text = text.lower()
            word_sequence = WordBreaker.split(text)
            total_words = len(word_sequence)
            for i in xrange(total_words):
                for j in range(self._n):
                    if i + j < total_words:
                        ngram[j] = word_sequence[i + j]
                    else:
                        ngram[j] = ""
                ngram_name = ' '.join(ngram)
                if ngram_name in ngrams:
                    ngrams[ngram_name] += 1
                else:
                    ngrams[ngram_name] = 1
        for ngram_name, freq in ngrams.items():
            if self._frequency_threshold and freq >= self._frequency_threshold:
                yield Feature("NG-%s:%s" % (self._n, ngram_name), freq)

# TODO: fine tune the parameters
feature_extractors = [NGramFeatureExtractor(1, True, 1), NGramFeatureExtractor(2, True, 1), NGramFeatureExtractor(3, True, 1)]