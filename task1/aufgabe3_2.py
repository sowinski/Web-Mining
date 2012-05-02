from nltk.book import *
import pylab
def con(text):
    alfa = []
    fdist = FreqDist(text)
    keys = fdist.keys()
    vals = fdist.values()
    maxiFreq = vals[0]
    for i in range(1, maxiFreq + 1):
	k = len([w for w in keys if fdist[w] == i])
	alfa.append(k)

    xs = range(1, maxiFreq + 1)
    ys = alfa
    pylab.plot(xs, ys)
    pylab.show()	
    return alfa

con(text1)
con(text5)
