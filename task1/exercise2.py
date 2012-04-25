import nltk
from nltk.book import *

print "Exercice 1 task 2"

# Gives the 30 must used words (first subtask)
fdkst1 = FreqDist(text1)
fdkst2 = FreqDist(text2)
fdkst3 = FreqDist(text4)
vocabulary1 = fdkst1.keys()
vocabulary2 = fdkst2.keys()
vocabulary3 = fdkst3.keys()
print 'Book 1:'
print vocabulary1[:30]
print 'Book 2:'
print vocabulary2[:30]
print 'Book 3:'
print vocabulary3[:30]

# Second subtask (first with filter)
