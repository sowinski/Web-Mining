const main = require("main");
const lang = require("language");
exports.test_test_run = function(test) {
  test.pass("Unit test running!");
};

exports.test_id = function(test) {
  test.assert(require("self").id.length > 0);
};

exports.test_url = function(test) {
  require("request").Request({
    url: "http://www.mozilla.org/",
    onComplete: function(response) {
      test.assertEqual(response.statusText, "OK");
      test.done();
    }
  }).get();
  test.waitUntilDone(20000);
};

exports.test_open_tab = function(test) {
  const tabs = require("tabs");
  tabs.open({
    url: "http://www.mozilla.org/",
    onReady: function(tab) {
      test.assertEqual(tab.url, "http://www.mozilla.org/");
      test.done();
    }
  });
  test.waitUntilDone(20000);
};

var errormessage = "";

exports.test_util_countElements = function(test) {
	const util = require("utility");
	test.assert(compareObjects(util.countElements(["du", "du", "hallo", "hallo", "du"]),{"hallo":2, "du":3}),errormessage);
};

exports.test_util_toCharArray = function(test) {
	const util = require("utility");
	test.assert(compareArrays(util.toCharArray("test"), ["t","e","s","t"]), errormessage);
};
 
exports.test_util_toCharPairs = function(test) {
	const util = require("utility");
	test.assert(compareArrays(util.toCharPairs("mainz"),["ma", "ai", "in", "nz"]), errormessage);
};

exports.test_util_tokenize = function(test) {
	const util = require("utility");
	test.assert(compareArrays(util.tokenize("Dem Igel geht's gut."),["dem","igel","gehts","gut"]), errormessage);
};

exports.test_student_student = function(test) {
	const student = require("student");
	var text = "blubber";
	test.assertEqual(student.student(text), lang.german, "Geht nicht weil.");
};

function compareObjects(a,b) {
	for(var key in a) {
		if( a[key] != b[key] ) {
			return false;
		}
	}
	return true;
};

function compareArrays(a,b) {
	if (a.length != b.length) {
		errormessage = "Arrays of unequal size";
		return false
	}
	for(var i=0; i<a.length; i++) {
		if (a[i] != b[i]) {
			errormessage = a[i] + " != " + b[i];
			return false;
		}
	}
	return true;
};
