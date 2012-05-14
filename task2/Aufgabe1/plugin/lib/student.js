var lang = require("language");
var util = require("utility");
var self = require("self");


function isStopWord(stopwords, word)
{
    for(var i=0; i < stopwords.length;i++)
    {
        if(word == stopwords[i] && word != "")
        {
            //console.log(">>" + word + "<< >>" + stopwords[i] + "<<");
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

function student(text) {
    console.log("---------------INIT--------------");    
    text = util.tokenize(text);


    var german = self.data.load("stopwords/german").split(/\r\n|\r|\n/);
    var french = self.data.load("stopwords/french").split(/\r\n|\r|\n/);
    var spanish = self.data.load("stopwords/spanish").split(/\r\n|\r|\n/);
    var english = self.data.load("stopwords/english").split(/\r\n|\r|\n/);
   
    var stopWordsGerman = countStopWords(german, text);
    var stopWordsFrench = countStopWords(french, text);
    var stopWordsSpanish = countStopWords(spanish, text);
    var stopWordsEnglish = countStopWords(english, text);

    console.log(stopWordsGerman);
    console.log(stopWordsFrench);
    console.log(stopWordsSpanish);
    console.log(stopWordsEnglish);

    if(stopWordsGerman > stopWordsFrench && 
       stopWordsGerman > stopWordsSpanish &&
       stopWordsGerman > stopWordsEnglish)
    {
        return lang.german;
    }
    else if (stopWordsFrench > stopWordsSpanish &&
             stopWordsFrench > stopWordsEnglish)
    {
        return lang.french;
    }
    else if (stopWordsSpanish > stopWordsEnglish)
    {
        return lang.spanish;
    }
    else
    {
        return lang.english;
    }

	
}

exports.student = student;
