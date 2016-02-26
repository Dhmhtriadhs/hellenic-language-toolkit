var dialektoi = null;
var timh = null;
var titlos = null;
var maximumtime = 0;
var timer = null;

function loadDialektous() {
	request = "dump/διάλεκτοι";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			dialektoi = result[0];
			var dias = Object.keys(dialektoi);
			var counter = 0;
			txt = "<table id='dia'><tr><td>";
			for (d = 0; d < dias.length; d++) {
				txt += '<input id="' + dias[d] + '" type="checkbox" value="'
						+ dias[d] + '">' + dias[d] + "</input></td>";
				if (d % 3 == 2) {
					txt += "</tr><tr>";
				}
				txt += "<td>";
			}
			txt += "</td></tr></table>";
			$("διάλεκτοι").innerHTML = txt;
		},
		onFailure : function() {
			alert('Something went wrong in loadDialektous.');
		}
	});
}

function loadEjagogi() {
	removeOptionsAlternate($("ετοιμα"));
	request = "dump/εξαγωγή";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			ethma = result[0];
			for (c = 0; c < ethma.length; c++) {
				$("ετοιμα")[c] = new Option(ethma[c]);
			}
		},
		onFailure : function() {
			alert('Something went wrong in loadDialektous.');
		}
	});
}

function diagrafh() {
	if ($("ετοιμα").selectedIndex == -1) { return;}
	request = "εξαγωγή/διαγραφή/"+ $F("ετοιμα");
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			//var result = eval(transport.responseText);
			loadEjagogi();
		},
		onFailure : function() {
			alert('Something went wrong in loadDialektous.');
		}
	});
}

function create() {
	$("ετοιμα").selectedIndex = -1;
	if ($F("γλώσσα").length == 0) {
		return;
	}
	var paketo = {
		"τύπος" : null,
		"διάλεκτοι" : [],
		"τίτλος" : $F("γλώσσα")
	};
	if ($("HLT").checked) {
		paketo["τύπος"] = "HLT";
	} else if ($("json").checked) {
		paketo["τύπος"] = "json";
	} else if ($("csv").checked) {
		paketo["τύπος"] = "csv";
	} else if ($("hunspell").checked) {
		paketo["τύπος"] = "hunspell";
	}
	var dias = Object.keys(dialektoi);
	for (d = 0; d < dias.length; d++) {
		if ($(dias[d]).checked) {
			paketo["διάλεκτοι"].push(dias[d]);
		}
	}

	request = "εξαγωγή/δημιουργία/" + Object.toJSON(paketo);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			timh = result[0];
			titlos = result[1];
			$("δημιουργία").disabled = true;
		},
		onFailure : function() {
			alert('Something went wrong in loadDialektous.');
		}
	});
	timer = setInterval("ping()", 1000);
}

function ping() {
	if (timh == null) {
		return;
	}
	var prog = 0;
	request = "εξαγωγή/πρόοδος/" + timh;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			prog = parseInt(transport.responseText);
			if (prog > 99) {
				clearInterval(timer);
				$("δημιουργία").disabled = false;
				loadEjagogi();
			}
			$("prog").value = prog;
		},
		onFailure : function() {
			clearInterval(timer);
			$("δημιουργία").disabled = true;
			alert('Something went wrong in ping.');
		}
	});

}

function download() {
	var request = null;
	if ($("ετοιμα").selectedIndex != -1) {
		request = "εξαγωγή/" + "αποτέλεσμα" + "/" + $F("ετοιμα");
	} else if (titlos != null) {
		request = "εξαγωγή/" + "αποτέλεσμα" + "/" + titlos;
	} else {
		return;
	}
	window.open(request);
}

function removeOptionsAlternate(obj) {
	if (obj == null)
		return;
	if (obj.options == null)
		return;
	while (obj.options.length > 0) {
		obj.remove(0);
	}
}
