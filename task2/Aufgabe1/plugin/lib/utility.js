
/*
Will count all equal array entries and list them in a javascript object such
that there is a object property for each unique array entry. The value of that
property equals the number of occurences. The order of the properties is sorted
according to the number of occurences. With the most occurences first.

You can use this construct

	for(var key in obj) {
		console.log(obj[key]);
	}

to iterate over all items in sorted order.
*/
function countElements(array) {
	var tmp = {};
	var result = {};
	var helpArray = [];
	for(var i=0; i<array.length; i++) {
		var item = array[i];
		if(!tmp.hasOwnProperty( item )) {
			tmp[item] = 1;
		} else {
			tmp[item] += 1;
		}
	}
	for(var key in tmp) {
		helpArray.push({key:key, value:tmp[key]});
	}
	helpArray.sort(comparePairs);
	for(var i=0; i<helpArray.length; i++) {
		result[helpArray[i].key] = helpArray[i].value;
	}
	return result;
};

/*Helperfunction for countElements*/
function comparePairs(a,b) {
	return b.value - a.value;
}

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

/*
Create an array of chars from a given text.
*/
function toCharArray(text) {
	var result = [];
	for(var i=0; i<text.length; i++) {
		result.push(text[i]);
	}
	return result;
}


/*
Create an array of charpairs from a given text.
*/
function toCharPairs(text) {
	var result = [];
	if (text.length > 1) {
		for(var i=1; i<text.length; i++) {
			result.push(text[i-1]+text[i]);
		}
	}
	return result;
}

exports.countElements = countElements;
exports.tokenize = tokenize;
exports.toCharArray = toCharArray;
exports.toCharPairs = toCharPairs;
