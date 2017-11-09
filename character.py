import math
from textblob import TextBlob as tb

class Character():

    def __init__(self, name, lines):
        self.name = name
        self.lines = lines
        self.blob = tb(' '.join(lines))

    def gen_tf_idf_vec(self, bloblist, all_words):
        self.tf_idf_vec = [self.tf_idf(word, bloblist) for word in all_words]

    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob.words)

    def idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def tf_idf(self, word, bloblist):
        return self.tf(word, self.blob) * self.idf(word, bloblist)

    def cosine_sim(self, other):
        sum_components = sum(map(lambda x : x[0] * x[1], zip(self.tf_idf_vec, other.tf_idf_vec)))
        sqrt_self = math.sqrt(sum(map(lambda x : x ** 2, self.tf_idf_vec)))
        sqrt_other = math.sqrt(sum(map(lambda x : x ** 2, other.tf_idf_vec)))
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
