import string
from math import log
import pickle

table = string.maketrans("","")
sample = []
with open('stories.txt') as f:
    for line in f.readlines():
        l = line.decode('utf-8').encode('ascii', 'ignore')
        l = l.translate(table, string.punctuation.replace('.',''))
        l = l.lower().replace('.',' _END_ _START_')
        sample.append(l)

N = 356033418959 # US american english v2 google ngrams
with open('ngramsFixed.pkl', 'r') as f:
    ngrams = pickle.load(f)

with open('nm1gramsFixed.pkl', 'r') as f:
    nm1grams = pickle.load(f)

nm1grams['_START_'] = float(sum([ ngrams[w] for w in ngrams.keys() if w[0] == '_START_']))

def calc_prob(sentences, ngra=ngrams, nm1gra=nm1grams, ALPHA=0.1):
    results = []
    Vng = len(ngrams.keys())
    Tk = log(N + ALPHA * len(nm1grams.keys()))
    for inx, sent in enumerate(sentences):
        tokens = ['_START_'] + sent.split()
        try:
            for t in xrange(0, len(tokens) - 2):
                if tokens[t+1] != '_START_' and tokens[t+1] != '_END_':
                    num = ngra[(tokens[t], tokens[t + 1])]  + ALPHA
                    denom = nm1gra[tokens[t]] + ALPHA * Vng
                    freq = nm1gra[tokens[t+1]]+ ALPHA
                    results.append([inx,
                                    t+1,
                                    tokens[t+1],
                                    log(num) - log(denom),
                                    log(freq) - Tk])
            results.append([inx,
                            len(tokens) - 1,
                            tokens[len(tokens)-1],
                            log(ngra[(tokens[len(tokens) - 2], tokens[len(tokens) - 1])] + ALPHA) - log(nm1gra[tokens[len(tokens) - 2]] + ALPHA*Vng),
                            log(nm1gra[tokens[len(tokens) - 2]] + ALPHA) - Tk])
        except:
            results.append([inx, 'NA'])
    return [', '.join([str(y) for y in x]) for x in results]

result = calc_prob(sample)
printstring = "\n".join(result)
with open('LangModelOut2.csv', 'w') as f:
    f.write(printstring)
