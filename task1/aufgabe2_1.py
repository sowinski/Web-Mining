import nltk
from nltk.book import *


def frequ(text):
    fdist = FreqDist(text)
    keys = fdist.keys()
    return keys[:30]

print frequ(text1)
print frequ(text5)
