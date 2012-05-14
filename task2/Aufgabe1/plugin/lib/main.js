var widgets = require("widget");
var pageMod = require("page-mod");
var student = require("student");
var data = require("self").data;

var workers = new Array();
var mod = null;

exports.main = function(options, callback) {
	mod = pageMod.PageMod(
		{
			include: "*",
			contentScriptWhen:"ready",
			contentScriptFile: data.url("./contentScripts/keworker.js"),
			onAttach: function onAttach(worker) {
				worker.on('message', handleMessage);
				workers.push(worker);
			}
		}
	);

	var widget = widgets.Widget(
		{
		  id: "ke",
		  label: "Knowledge Engineering",
		  contentURL: data.url("keicon.png")
		}
	);

	function handleMessage(message) {
		var lang = require("language");
		if(message.length > 0) {
			//TODO: Iconswitch
			var language = student.student(message);
			console.log(language);
			switch(language) {
				case lang.german: 
					widget.contentURL = data.url("./flag/de.png");
					break;
				case lang.spanish: 
					widget.contentURL = data.url("./flag/es.png");
					break;
				case lang.english: 
					widget.contentURL = data.url("./flag/en.png");
					break;
				case lang.french: 
					widget.contentURL = data.url("./flag/fr.png");
					break;
				default:
					widget.contentURL = data.url("./keicon.png");
					
			}
			//TODO: response
		}
	}

	console.log("The add-on is running.");
}

exports.onUnload = function(reason) {
	if(mod != null) {mod.destroy();}
	for(var i=0; i<workers.length; i++) {
		workers[i].destroy();
	}
}
