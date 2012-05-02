from nltk.book import *


def letterFrequ(text):
    freq_dist = FreqDist()
    for word in text:
        for char in word:
	    freq_dist.inc(char)


    return freq_dist
    
print letterFrequ(text1)
print letterFrequ(text5)
