var ortho = null;

// ΜΟΔΕ
function EN_APXH() {
	nea();
	loadOrthogafia();
}

function boh_theia() {
	keimeno = "";
	alert(keimeno);
}

function nea() {
	$("όνομα").value = "";
	$("γράμμα").value = "";
	$("αντιστοιχίες").value = "";
	$("αποτέλεσμα").value = "";
	$("όνομα").focus();
	
	$("κεφαλαία").checked = false;
	$("πνεύματα").checked = false;
	$("τόνοι").checked = false;
	$("εμπρός").checked = false;
	$("πίσω").checked = false;
	
	removeOptionsAlternate($("οαρχή"));
	removeOptionsAlternate($("ομέση"));
	removeOptionsAlternate($("οτέλος"));
}

function loadOrthogafia() {
	request = "dump/ορθογραφία";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			ortho = result[0];
			removeOptionsAlternate($("ορθογραφίες"));
			or = Object.keys(ortho);
			for(i=0;i<or.length;i++) {
				$("ορθογραφίες")[i] = new Option(or[i]);
			}
			updateOrthografia();
		},
		onFailure : function() {
			alert('Something went wrong in loadDialektous.');
		}
	});
}

function dokimh() {
	var message = {"αρχή":{}, "μέση":{}, "τέλος":{},
			"λέξη":$F("δοκιμή"), "κεφαλαία":0, 
			"πνεύματα":0, "τόνοι":0};
	for(i=0;i<$("οαρχή").length;i++) {
		meri = $("οαρχή")[i].value.split(": ");
		message["αρχή"][meri[0]] = meri[1].split(",");
	}
	for(i=0;i<$("ομέση").length;i++) {
		meri = $("ομέση")[i].value.split(": ");
		message["μέση"][meri[0]] = meri[1].split(",");
	}
	for(i=0;i<$("οτέλος").length;i++) {
		meri = $("οτέλος")[i].value.split(": ");
		message["τέλος"][meri[0]] = meri[1].split(",");
	}
	if ($("κεφαλαία").checked) {
		message["κεφαλαία"] = 1;
	}
	if ($("πνεύματα").checked) {
		message["πνεύματα"] = 1;
	}
	if ($("τόνοι").checked) {
		message["τόνοι"] = 1;
	}
	request = "develop/ορθογραφία_δοκιμή/"+Object.toJSON(message);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			$("αποτέλεσμα").value = "";
			for(i=0;i<result[0].length;i++) {
				$("αποτέλεσμα").value += result[0][i]+"\n";
			}
		},
		onFailure : function() {
			alert('Something went wrong in dokimh.');
		}
	});
}

function zero() {
	$("γράμμα").value = "";
	$("αντιστοιχίες").value = "";
}

function add() {
	var thesi = null;
	if ($F("γράμμα").length == 0) {
		return;
	}
	paketo = $F("γράμμα") + ": " + $F("αντιστοιχίες");
	if ($("αρχή").checked) {
		thesi = "οαρχή";
	} else if ($("μέση").checked) {
		thesi = "ομέση";
	} else if ($("τέλος").checked) {
		thesi = "οτέλος";
	} else {
		return;
	}
	pos = $(thesi).length;
	for (i = 0; i < $(thesi).length; i++) {
		if ($(thesi)[i].value.split(": ")[0] == $F("γράμμα")) {
			pos = i;
			break;
		}
	}
	$(thesi)[pos] = new Option(paketo);
}

function updateOrthografia() {
	if (ortho == null) {
		return;
	}
	$("όνομα").value = $F("ορθογραφίες");
	or = ortho[$F("ορθογραφίες")];
	if (or["κεφαλαία"]==1) {
		$("κεφαλαία").checked = true;
	} else {
		$("κεφαλαία").checked = false;
	}
	if (or["πνεύματα"]==1) {
		$("πνεύματα").checked = true;
	} else {
		$("πνεύματα").checked = false;
	}
	if (or["τόνοι"]==1) {
		$("τόνοι").checked = true;
	} else {
		$("τόνοι").checked = false;
	}
	if (or["εμπρός"]==1) {
		$("εμπρός").checked = true;
	} else {
		$("εμπρός").checked = false;
	}
	if (or["πίσω"]==1) {
		$("πίσω").checked = true;
	} else {
		$("πίσω").checked = false;
	}
	removeOptionsAlternate($("οαρχή"));
	dia = Object.keys(or["αρχή"]);
	for (d = 0; d < dia.length; d++) {
		$("οαρχή")[d] = new Option(dia[d]+": "+or["αρχή"][dia[d]]);
	}
	removeOptionsAlternate($("ομέση"));
	dia = Object.keys(or["μέση"]);
	for (d = 0; d < dia.length; d++) {
		$("ομέση")[d] = new Option(dia[d]+": "+or["μέση"][dia[d]]);
	}
	removeOptionsAlternate($("οτέλος"));
	dia = Object.keys(or["τέλος"]);
	for (d = 0; d < dia.length; d++) {
		$("οτέλος")[d] = new Option(dia[d]+": "+or["τέλος"][dia[d]]);
	}
}

function apothikeusi() {
	var message = {
		"όνομα":$F("όνομα"),
		"αρχή":{}, "μέση":{}, "τέλος":{},
		"λέξη":$F("δοκιμή"), "κεφαλαία":0, 
		"πνεύματα":0, "τόνοι":0,
		"εμπρός":0, "πίσω":0};
	for(i=0;i<$("οαρχή").length;i++) {
		meri = $("οαρχή")[i].value.split(": ");
		message["αρχή"][meri[0]] = meri[1].split(",");}
	for(i=0;i<$("ομέση").length;i++) {
		meri = $("ομέση")[i].value.split(": ");
		message["μέση"][meri[0]] = meri[1].split(",");}
	for(i=0;i<$("οτέλος").length;i++) {
		meri = $("οτέλος")[i].value.split(": ");
		message["τέλος"][meri[0]] = meri[1].split(",");}
	if ($("κεφαλαία").checked) {
		message["κεφαλαία"] = 1;}
	if ($("πνεύματα").checked) {
		message["πνεύματα"] = 1;}
	if ($("τόνοι").checked) {
		message["τόνοι"] = 1;}
	if ($("εμπρός").checked) {
		message["εμπρός"] = 1;}
	if ($("πίσω").checked) {
		message["πίσω"] = 1;}
	index = $("ορθογραφίες").selectedIndex;
	if (index!=-1) {
		message["Κλειδί"] = ortho[$F("ορθογραφίες")]["Κλειδί"];
	}
	request = "develop/ορθογραφία_αποθήκευση/" + Object.toJSON(message);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Αποθηκεύτικε!");
				loadOrthogafia();
			} else {
				alert("Αποτυχία: " + transport.responseText);
			}
		},
		onFailure : function() {
			alert('Something went wrong in apothikeusi.');
		}
	});
}

function diagrafi() {
	if ($("ορθογραφίες").selectedIndex != -1) {
		message = ortho[$F("ορθογραφίες")];
		request = "develop/ορθογραφία_διαγραφή/" + Object.toJSON(message);
		var xmlhttp = new Ajax.Request(request, {
			method : 'post',
			onSuccess : function(transport) {
				if (transport.responseText == "OK") {
					alert("Διαγράφηκε!");
					EN_APXH();
				}
			},
			onFailure : function() {
				alert('Something went wrong in diagrafi.');
			}
		});
	}
}

function edit(name) {
	if (name=="οαρχή") {
		$("αρχή").checked = true;
		$('ομέση').selectedIndex=-1;
		$('οτέλος').selectedIndex=-1;
	} else if (name=='ομέση') {
		$("μέση").checked = true;
		$("οαρχή").selectedIndex=-1;
		$('οτέλος').selectedIndex=-1;
	} else if (name=='οτέλος') {
		$("τέλος").checked = true;
		$('ομέση').selectedIndex=-1;
		$("οαρχή").selectedIndex=-1;
	}
	
	if ($(name).selectedIndex != -1) {
		meri = $F(name).split(": ");
		$("γράμμα").value = meri[0]
		$("αντιστοιχίες").value = meri[1]
	}
}

function showDialekto(data) {
	if ($("πΔιαλέκτων").selectedIndex != -1) {
		$("τίτλος").value = data["όνομα"];
		while ($("εΔιάλεκτοι").length > 0) {
			$("εΔιάλεκτοι").remove(0);
		}
		;
		$("ἐτικέτες").value = data["ἐτικέτες"];
		$("Ἡμερομηνία").innerHTML = data["Ἡμερομηνία"];
		$("Παρατηρήσεις").value = data["Παρατηρήσεις"];

		if (data["δυϊκός"] == 1) {
			$("Δυϊκός").checked = true;
		} else {
			$("Δυϊκός").checked = false;
		}

		if (data["δοτική"] == 1) {
			$("Δοτική").checked = true;
		} else {
			$("Δοτική").checked = false;
		}

		for (p = 0; p < data["πτώσεις"].length; p++) {
			cell = parseInt(data["πτώσεις"][p] / 5) + 1;
			row = data["πτώσεις"][p] % 5 + 2;
			onoma = $("ονόματα").tBodies[0].rows[row].cells[cell].firstChild;
			if (onoma.tagName == "INPUT") {
				onoma.checked = true;
			}
		}
		epektaseis = data["επεκτάσεις"];
		for (e = 0; e < epektaseis.length; e++) {
			$("εΔιάλεκτοι")[e] = new Option(epektaseis[e]);
			removeValue("δΔιάλεκτοι", epektaseis[e]);
		}

		xronoi = Object.keys(data["ρήμα"]);
		xr_p = {
			"ενεστώτας" : 4,
			"παρατατικός" : 10,
			"αόριστος" : 16,
			"παρακείμενος" : 22,
			"υπερσυντέλικος" : 28,
			"μέλλοντας" : 34,
			"συντελεσμένος μέλλοντας" : 40
		};
		for (x = 0; x < xronoi.length; x++) {
			xronos = xronoi[x];
			times = data["ρήμα"][xronos];
			for (t = 0; t < times.length; t++) {
				row = (times[t] % 5) + xr_p[xronos];
				col = parseInt(times[t] / 5) + 1;
				onoma = $("χρόνοι").tBodies[0].rows[row].cells[col];
				if (onoma.firstChild.tagName == "INPUT") {
					onoma.firstChild.checked = true;
				}
			}
		}
		xronoi = Object.keys(data["μετοχή"]);
		for (x = 0; x < xronoi.length; x++) {
			xronos = xronoi[x];
			times = data["μετοχή"][xronos];
			for (t = 0; t < times.length; t++) {
				row = xr_p[xronos] - 1;
				col = parseInt(times[t] / 3) + 4;
				onoma = $("χρόνοι").tBodies[0].rows[row].cells[col];
				if (onoma.firstChild.tagName == "INPUT") {
					onoma.firstChild.checked = true;
				}
			}
		}
		selectValue("εικονική", data["εικονική"]);
	}
}

function prosthiki() {
	if ($("δΔιάλεκτοι").selectedIndex != -1) {
		n = $("εΔιάλεκτοι").length;
		$("εΔιάλεκτοι")[n] = new Option($F("δΔιάλεκτοι"));
		$("δΔιάλεκτοι").remove($("δΔιάλεκτοι").selectedIndex);
	}
}

function afairesh() {
	if ($("εΔιάλεκτοι").selectedIndex != -1) {
		n = $("δΔιάλεκτοι").length;
		$("δΔιάλεκτοι")[n] = new Option($F("εΔιάλεκτοι"));
		$("εΔιάλεκτοι").remove($("εΔιάλεκτοι").selectedIndex);
	}
}

// ΒΟΗΘΗΤΙΚΑ
function selectValue(elm, val) {
	for (n = 0; n < $(elm).length; n++) {
		if ($(elm)[n].value == val) {
			$(elm).selectedIndex = n;
			n = $(elm).length;
		}
	}
}

function removeValue(elm, val) {
	n = 0;
	while ($(elm).options.length > n) {
		if ($(elm)[n].value == val) {
			$(elm).remove(n);
			break;
		}
		n += 1;
	}
}

function include(arr, obj) {
	result = true;
	for (x = 0; x < arr.length; x++) {
		if (arr[x] == obj) {
			result = false;
		}
	}
	return result;
}

function removeOptionsAlternate(obj) {
	if (obj == null)
		return;
	if (obj.options == null)
		return;
	while (obj.length > 0) {
		obj.remove(0);
	}
}
