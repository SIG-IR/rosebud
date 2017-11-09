import math
from textblob import TextBlob as tb

class Character():

    def __init__(self, name, lines):
        self.name = name
        self.lines = lines
        self.blob = tb(' '.join(lines))

    def gen_tf_idf_vec(self, bloblist):
        self.tf_idf_vec = []
        for word in self.all_words_in(bloblist):
            self.tf_idf_vec.append(self.tf_idf(word, bloblist))

    def all_words_in(self, bloblist):
        words = []
        for blob in bloblist:
            words += blob.words
        return words

    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob.words)

    def idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def tf_idf(self, word, bloblist):
        return self.tf(word, self.blob) * self.idf(word, bloblist)

    def cosine_sim(self, other):
        sum_components = sum([self.tf_idf_vec[i] * other.tf_idf_vec[i] for i in range(len(self.tf_idf_vec))])
        sqrt_self = math.sqrt(sum([a ** 2 for a in self.tf_idf_vec]))
        sqrt_other = math.sqrt(sum([b ** 2 for b in other.tf_idf_vec]))
        return sum_components / (sqrt_self * sqrt_other)



'''
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
'''
