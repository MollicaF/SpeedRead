from zs import ZS
import string
import pickle

table = string.maketrans("","")
sample = []
with open('stories.txt') as f:
    for line in f.readlines():
        l = line.decode('utf-8').encode('ascii', 'ignore')
        l = l.translate(table, string.punctuation.replace('.',''))
        l = l.lower().replace('.',' _END_ _START_')
        sample.append(l)

google1 = ZS('../../Corpus/cpl-data.ucsd.edu/zs/google-books-20120701/eng-us-all/google-books-eng-us-all-20120701-1gram.zs')
google2 = ZS('../../Corpus/cpl-data.ucsd.edu/zs/google-books-20120701/eng-us-all/google-books-eng-us-all-20120701-2gram.zs')
# |V| = 356033418959


#  break sentences into strings
def populate(sentences):
    ngra = dict()
    nm1gra = dict()
    for sentence in sentences:
        tokens = ['_START_'] + sentence.split()
        for t in xrange(0, len(tokens) - 2):
            ngra[(tokens[t], tokens[t + 1])] = 0
            nm1gra[tokens[t]] = 0
        ngra[(tokens[len(tokens) - 2], tokens[len(tokens) - 1])] = 0
        nm1gra[tokens[len(tokens) - 1]] = 0
        nm1gra[tokens[len(tokens) - 2]] = 0
    return ngra, nm1gra

#  fetch ngram and n-1gram
def fetch(ngra, z=google2, zm1=google1):
    ngram_c = 0
    ngram_str = " ".join(ngra)
    for record in z.search(prefix=ngram_str):
        entry = record.split()
        ngram_c += int(entry[3])
    if nm1grams[ngra[0]] > 0:
        nm1gram_c = nm1grams[ngra[0]]
    else:
        nm1gram_c = 0
        for record in zm1.search(prefix=ngra[0]):
            entry = record.split()
            nm1gram_c += int(entry[2])
    return ngram_c, nm1gram_c

ngrams, nm1grams = populate(sample)

for ngram in ngrams.keys():
    print ngram
    ngrams[ngram], nm1grams[ngram[0]] = fetch(ngram)

with open('ngrams.pkl', 'w') as f:
    pickle.dump(ngrams, f)

with open('nm1grams.pkl', 'w') as f:
    pickle.dump(nm1grams, f)
