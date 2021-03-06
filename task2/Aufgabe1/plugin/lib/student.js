var lang = require("language");
var util = require("utility");
var self = require("self");


function genMap(chars){
	chars = chars.toLowerCase();
	var myArray = chars.split(" ");
	
		var myMap = new Array();
		
		for(var i=0;i<myArray.length-1;i=i+2){
			myMap[myArray[i]]=myArray[i+1];
		}

	return myMap;	
	}

function CosSimi(u, v)
{
    var dotProduct = 0;
    var uNorm = 0;
    var vNorm = 0;
    var minUI = Math.min(u.length,v.length)

    for(var i=0; i < minUI;i++)
    {
        dotProduct += Math.abs(u[i] * v[i])
    }

     for(var i=0; i < minUI;i++)
    {
        uNorm =uNorm +  u[i] * u[i]
    }
    uNorm = Math.sqrt(uNorm) 

     for(var i=0; i < minUI;i++)
    {
        vNorm = vNorm+ v[i] * v[i]
    }
    vNorm = Math.sqrt(vNorm)

    return dotProduct / (uNorm * vNorm);
}

function sortAccordTheFirst(u, v)
{
    var output = new Array();
    for (uKey in u) { 

      for (vKey in v) 
      { 
       if(uKey == vKey)
        {
           output.push(v[vKey]);
        }
      }
    
     }
    
    return output;
}

function processLetters(text) { 
	
    return util.toCharArray(text);
}

function processLetterPairs(text) {	

    return util.toCharPairs(text);
}
////////////////////////////////
function isStopWord(stopwords, word)
{
    for(var i=0; i < stopwords.length;i++)
    {
        if(word == stopwords[i] && word != "")
        {
            return true;
        }
    }
    return false;
}

function countStopWords(stopwords, text)
{
    var stopwordscnt = 0;
    for(var i=0; i < text.length; i++)
    {
        if(isStopWord(stopwords, text[i]))
        {
            stopwordscnt++;
        }
    }
    return stopwordscnt;
}
////////////////////////////////

function student(text) {
     console.log("---------------INIT--------------");    
     text = util.tokenize(text);

     var charMap = new Array();
     // set letter or letter-pair processing function
     // E.G. var letterOrPair = text; for letter-pairs
     var letterOrPair = processLetters(text);

       charMap= util.countElements(letterOrPair);

	var totalCounts=0;
	for (key in charMap){
	totalCounts += charMap[key];
	}
	
	for (key in charMap){
		charMap[key] = charMap[key] * 100 / totalCounts;
	}
    
    // set data for letter or letter-pair processing
    // E.G. var german = self.data.load("letterPairFreq/pairGerman.txt");
    var german = self.data.load("letterFreq/letterGerman.txt");
    var spanish = self.data.load("letterFreq/letterSpanish.txt");
    var english = self.data.load("letterFreq/letterEnglish.txt");



 
    var germanCharMap = genMap(german);
    var spanishCharMap = genMap(spanish);
    var englishCharMap = genMap(english);

    
    var germanFreqList = new Array();
    var spanishFreqList = new Array();
    var englishFreqList = new Array(); 

      for (key in englishCharMap) 
      { 
         englishFreqList.push(englishCharMap[key]); 
      }

      for (key in germanCharMap) 
      { 
         germanFreqList.push(germanCharMap[key]); 
      }

      for (key in spanishCharMap) 
      { 
         spanishFreqList.push(spanishCharMap[key]); 
      }
    

    var textSortedWithGer = sortAccordTheFirst(germanCharMap, charMap);
    var germSimi =  CosSimi(germanFreqList, textSortedWithGer);

    var textSortedWithSpa = sortAccordTheFirst(spanishCharMap, charMap);
    var spanSimi =  CosSimi(spanishFreqList, textSortedWithSpa);

    var textSortedWithEng = sortAccordTheFirst(englishCharMap, charMap);
    var engSimi =  CosSimi(englishFreqList, textSortedWithEng);



    if(spanSimi > engSimi && 
       spanSimi > germSimi) 
    {
        return lang.spanish;
    }
    else if (germSimi > engSimi &&
             germSimi > spanSimi)
    {
        return lang.german;
    }
    else
    {
        return lang.english;
    }

	


	
}

exports.student = student;
