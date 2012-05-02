from nltk.book import *
import pylab
def zipfPlot(text):
    fdist = FreqDist(text)
    vals = fdist.values()
    pylab.plot(range(1, 31), vals[:30])
    pylab.show()
    
    pylab.plot(range(1, 31), vals[:30])
    pylab.xscale('log')
    pylab.yscale('log')
    pylab.show()

zipfPlot(text1)
zipfPlot(text5)
