import urllib
import random
import numpy as np
import matplotlib.pyplot as plt
import socket
socket.setdefaulttimeout(5)

from sgmllib import SGMLParser

def getUrlContent(url):
    try:
        fp = urllib.urlopen(url)
        html = fp.read()
        return html
    except:
        print "FAIL TO LOAD"
        return ""

class URLLister(SGMLParser):
    def reset(self):                              
        SGMLParser.reset(self)
        self.urls = []
        
    def start_a(self, attrs):                     
        
        href = [v for k, v in attrs if k=='href'] 
        if href:
            self.urls.extend(href)



class Crawler():
    def __init__(self):
        self.counter = 0
        self.urlContainer = []
        self.urlScanned = []
        self.urlList = []
        self.urlListNew = []
        
    def plotAufgabe1(self, urls, urlsneu):
        print "eins"
    
    def crawlMore(self, count, url):
        for i in range(1, count):
            print i
            url = self.crawl(url)
            self.counter = 0
    
    def crawl(self, url):
        self.urlScanned.append(url)
        if self.counter == 10:
            return url
        self.counter += 1
        self.urlContainer.append(url)
        print url
        websiteContent = getUrlContent(url)
        try:
            extractor = URLLister()
            extractor.feed(websiteContent)
            extractor.close()
            urlsaufseite = 0
            urlsaufseiteneu = 0
            for u in extractor.urls:
                test = u[0:4]
                if test == 'http':
                    urlsaufseite += 1
                    if not u in self.urlContainer:
                        urlsaufseiteneu += 1
                    self.urlContainer.append(u)
            print urlsaufseite
            print urlsaufseiteneu
            #Aufgabe 1
            self.urlList.append(urlsaufseite)
            self.urlListNew.append(urlsaufseiteneu)
        except:
            print "Fehler"
            self.counter -= 1    
        # Waehle Random eine URL
        i = random.randint(0,len(self.urlContainer)-1)
        while True:
            if not self.urlContainer[i] in self.urlScanned:
                break
            else:
                i = random.randint(0,len(self.urlContainer)-1)
        #Scanne Rekursiv die ausgesuchte URL
        return self.crawl(self.urlContainer[i])
            
                

c = Crawler()

c.crawlMore(100, 'http://golem.de')
print "Done"

ind = np.arange(len(c.urlList))  # the x locations for the groups

print ind
width = 0.5       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)
rects1 = ax.bar(ind, c.urlList, width, color='r')

rects2 = ax.bar(ind+width, c.urlListNew, width, color='y')

ax.legend( (rects1[0], rects2[0]), ('URL-Anzahl', 'Neue URL-Anzahl') )

plt.show()

