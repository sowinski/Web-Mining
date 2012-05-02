from nltk.corpus import stopwords
import nltk
from nltk.book import *


def freqWithoutStops(text, filterwords):
    stopwords = filterwords
    content = [w for w in text if w.lower() not in stopwords]
    fdist = FreqDist(content)
    keys = fdist.keys()
    return keys[:30]


print freqWithoutStops(text1, stopwords.words('english'))
print freqWithoutStops(text5, stopwords.words('english'))
