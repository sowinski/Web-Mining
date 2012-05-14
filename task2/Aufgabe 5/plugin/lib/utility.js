/*
Tokenize a text at whitespace.
Some punctuations are removed
*/
function tokenize(text) {
	var lct = text.toLowerCase();
	lct = lct.replace(/(\.|,|!|\?|'|"|\\|\/|\|)/g,"");
	var result = lct.split(/\W/g);
	return result;
}


exports.tokenize = tokenize;
