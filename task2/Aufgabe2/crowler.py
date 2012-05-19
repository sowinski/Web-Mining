import urllib
import random

from sgmllib import SGMLParser

def getUrlContent(url):
    fp = urllib.urlopen(url)
    html = fp.read()
    return html

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
    
    def crawl(self, url):
        self.urlScanned.append(url)
        if self.counter == 100:
            return
        self.counter += 1
        self.urlContainer.append(url)
        print url
        websiteContent = getUrlContent(url)
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
        
        # Waehle Random eine URL
        i = random.randint(0,len(self.urlContainer)-1)
        while True:
            if not self.urlContainer[i] in self.urlScanned:
                break
            else:
                i = random.randint(0,len(self.urlContainer)-1)
        #Scanne Rekursiv die ausgesuchte URL
        self.crawl(self.urlContainer[i])
            
                

c = Crawler()
c.crawl('http://golem.de')
print "Done"

