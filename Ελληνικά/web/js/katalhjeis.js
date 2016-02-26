var mtl = "ουσιαστικό";
var katalhjeis = null; // dialekto:kathgoria:katalhjeis
var istoria = null;
var dialektoi = null;

// ΜΟΔΕ
function EN_APXH() {
	neos();
	loadDialektous();
	loadKatalhjeis();
}

function eyresi(fora) {
	text = $F("εύρεση");
	notfound = true;
	if (fora == "e") {
		start = $("κκατηγορίες").selectedIndex +1;
		for (n = start; n < $("κκατηγορίες").length; n++) {
			if ($("κκατηγορίες")[n].value.search(text) != -1) {
				$("κκατηγορίες").selectedIndex = n;
				notfound = false;
				break
			}
		}
		if (notfound) {
			for (n = 0; n < $("κκατηγορίες").length; n++) {
				if ($("κκατηγορίες")[n].value.search(text) != -1) {
					$("κκατηγορίες").selectedIndex = n;
					break
				}
			}
		}
	} else {
		start = $("κκατηγορίες").selectedIndex;
		if(start>0) { start -= 1;}
		for (n = start-1; n > -1; n--) {
			if ($("κκατηγορίες")[n].value.search(text) != -1) {
				$("κκατηγορίες").selectedIndex = n;
				notfound = false;
				break
			}
		}
		if (notfound) {
			for (n = $("κκατηγορίες").length-1; n > -1; n--) {
				if ($("κκατηγορίες")[n].value.search(text) != -1) {
					$("κκατηγορίες").selectedIndex = n;
					break
				}
			}
		}
	}
}

function loadDialektous() {
	request = "dump/διάλεκτοι";
	var xmlhttp = new Ajax.Request(request,
			{
				method : 'post',
				onSuccess : function(transport) {
					var result = eval(transport.responseText);
					dialektoi = result[0];
					removeOptionsAlternate($("διάλεκτος"));
					var dias = Object.keys(dialektoi);
					var counter = 0;
					for (d = 0; d < dias.length; d++) {
						if (dialektoi[dias[d]]["εικονική"].length == 0) {
							$("διάλεκτος")[counter] = new Option(dias[d]
									.toLowerCase());
							counter += 1;
						}
					}
				},
				onFailure : function() {
					alert('Something went wrong in loadDialektous.');
				}
			});
}

function updateKatalhjeis() {
	if (katalhjeis == null) {
		return;
	}
	removeOptionsAlternate($("κκατηγορίες"));
	if (mtl == "ουσιαστικό" || mtl == "επίθετο") {
		var elm = katalhjeis[mtl][$F("διάλεκτος")];
		for (k = 0; k < elm.length; k++) {
			b = elm[k]["ΑΑ"] + " (" + elm[k]["καταλήξεις"] + ") ";
			$("κκατηγορίες")[k] = new Option(b);
		}
	} else if (mtl == "ρήμα" || mtl == "μετοχή") {
		var elm = katalhjeis[mtl][$F("διάλεκτος")][$F("χρόνος")];
		var counter = 0;
		for (k = 0; k < elm.length; k++) {
			if (elm[k]["ΑΑ"] != undefined) {
				b = elm[k]["ΑΑ"] + " (" + elm[k]["καταλήξεις"] + ") ";
				$("κκατηγορίες")[counter] = new Option(b);
				counter += 1;
			}
		}
	}
}

function updateKatalhjeis2() {
	if (katalhjeis == null) {
		return;
	}
	removeOptionsAlternate($("κκατηγορίες"));

	if (mtl == "ουσιαστικό" || mtl == "επίθετο") {
		var elm = katalhjeis[mtl][$F("διάλεκτος")];
		for (k = 0; k < elm.length; k++) {
			b = elm[k]["ΑΑ"] + " (" + elm[k]["καταλήξεις"] + ") ";
			$("κκατηγορίες")[k] = new Option(b);
		}
	} else if (mtl == "ρήμα" || mtl == "μετοχή") {
		var elm = katalhjeis[mtl][$F("διάλεκτος")][$F("χρόνος")];
		for (k = 0; k < elm.length; k++) {
			b = elm[k]["ΑΑ"] + " (" + elm[k]["καταλήξεις"] + ") ";
			$("κκατηγορίες")[k] = new Option(b);
		}
	}
}

function neos() {
	removeOptionsAlternate("κκατηγορίες");
	removeOptionsAlternate("ιστορία");
	$("ουσιαστικό").style.backgroundColor = "lightgray";
	$('επίθετο').style.backgroundColor = "";
	$('ρήμα').style.backgroundColor = "";
	$('μετοχή').style.backgroundColor = "";
	mtl = "ουσιαστικό";
}

function loadIstoria() {
	if ($("κκατηγορίες").selectedIndex != -1) {
		while ($("ιστορία").length > 0) {
			$("ιστορία").remove(0);
		}

		parts = $F("κκατηγορίες").split(" ");
		kat = parseInt(parts[0]);
		var message = {};
		if (mtl == "ρήμα" || mtl == "μετοχή") {
			message = katalhjeis[mtl][$F("διάλεκτος")][$F("χρόνος")][kat];
		} else {
			message = katalhjeis[mtl][$F("διάλεκτος")][kat];
		}
		request = "develop/ιστορικό_καταλήξεων/" + Object.toJSON(message);
		var xmlhttp = new Ajax.Request(request,
				{
					method : 'post',
					onSuccess : function(transport) {
						var result = eval(transport.responseText);
						istoria = result;
						removeOptionsAlternate("ιστορία");
						var counter = 0;
						for (k = 0; k < istoria.length; k++) {
							b = istoria[k]["Ἡμερομηνία"] + ' '
									+ istoria[k]["ἐτικέτες"];
							$("ιστορία")[counter] = new Option(b);
							counter += 1;
							// if (istoria[k]['ἐτικέτες'].match("τρέχον")) {
							// $("πΙστορίας")[counter].selected;
							// trex=k;}

							// if (maxdate<istoria[k]["Ἡμερομηνία"]) {
							// maxd_pos = k;
							// maxdate=istoria[k]["Ἡμερομηνία"];}
						}
						$("ιστορία").selectedIndex = 0;
						epilogiIstorias();
						// if (trex==-1) { trex=maxd_pos;}
						// showDialekto(istoria[trex]);
					},
					onFailure : function() {
						alert('Something went wrong in loadIstoria.');
					}
				});
	}
}

function allagiMTL(val) {
	if (val == "ουσιαστικό") {
		$("ουσιαστικό").style.backgroundColor = "lightgray";
		$('επίθετο').style.backgroundColor = "";
		$('ρήμα').style.backgroundColor = "";
		$('μετοχή').style.backgroundColor = "";
		$("χρόνος").disabled = true;
	} else if (val == 'επίθετο') {
		$("ουσιαστικό").style.backgroundColor = "";
		$('επίθετο').style.backgroundColor = "lightgray";
		$('ρήμα').style.backgroundColor = "";
		$('μετοχή').style.backgroundColor = "";
		$("χρόνος").disabled = true;
	} else if (val == 'ρήμα') {
		$("ουσιαστικό").style.backgroundColor = "";
		$('επίθετο').style.backgroundColor = "";
		$('ρήμα').style.backgroundColor = "lightgray";
		$('μετοχή').style.backgroundColor = "";
		$("χρόνος").disabled = false;
	} else if (val == 'μετοχή') {
		$("ουσιαστικό").style.backgroundColor = "";
		$('επίθετο').style.backgroundColor = "";
		$('ρήμα').style.backgroundColor = "";
		$('μετοχή').style.backgroundColor = "lightgray";
		$("χρόνος").disabled = false;
	}
	mtl = val;
	updateKatalhjeis();
}

function loadKatalhjeis() {
	request = "dump/καταλήξεις";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			// alert(transport.responseText);
			var result = eval(transport.responseText);
			katalhjeis = result[0];
			updateKatalhjeis();
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function epilogiKathgorias(dedomena, leji) {
	var ton = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ];
	if (dedomena != false) {
		parts = $F("κκατηγορίες").split(" ");
		kat = dedomena["ΑΑ"];
		for (i = 0; i < dedomena["καταλήξεις"].length; i++) {
			ton[i] = leji + dedomena["καταλήξεις"][i];
		}
	}
	var countTo = 0;
	var sz = [];

	if (mtl == "ουσιαστικό" || mtl == "επίθετο" || mtl == "μετοχή") {
		countTo = 5;
		pinakas = [
				[ [ 'Ενικός' ] ],
				[ [ 'Ονομαστική' ], [ 'Γενική' ], [ 'Δοτική' ],
						[ 'Αιτιατική' ], [ 'Κλητική' ] ],
				[ ton[0], ton[1], ton[2], ton[3], ton[4] ],
				[ [ 'Δυϊκός' ] ],
				[ [ 'Ονομαστική' ], [ 'Γενική' ], [ 'Δοτική' ],
						[ 'Αιτιατική' ], [ 'Κλητική' ] ],
				[ ton[5], ton[6], ton[7], ton[8], ton[9] ],
				[ [ 'Πληθυντικός' ] ],
				[ [ 'Ονομαστική' ], [ 'Γενική' ], [ 'Δοτική' ],
						[ 'Αιτιατική' ], [ 'Κλητική' ] ],
				[ ton[10], ton[11], ton[12], ton[13], ton[14] ] ];
		if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0
				|| dialektoi[$F("διάλεκτος")]["δυϊκός"] == "0") {
			pinakas.splice(3, 3);
		}
		if (dialektoi[$F("διάλεκτος")]["δοτική"] == 0
				|| dialektoi[$F("διάλεκτος")]["δοτική"] == "0") {
			for (z = 0; z < pinakas.length; z++) {
				if (z % 3 != 0) {
					pinakas[z].splice(2, 1);
				}
			}
			countTo -= 1;
		}
		sz = [ 10, 10, 10, 10, 10 ];
	} else if (mtl == "ρήμα") {
		countTo = 3;
		pinakas = [ [ [ 'Ενικός' ] ], [ [ 'α' ], [ 'β' ], [ 'γ' ] ],
				[ ton[0], ton[1], ton[2] ], [ [ 'Δυϊκός' ] ],
				[ [ 'α' ], [ 'β' ], [ 'γ' ] ], [ ton[3], ton[4], ton[5] ],
				[ [ 'Πληθυντικός' ] ], [ [ 'α' ], [ 'β' ], [ 'γ' ] ],
				[ ton[6], ton[7], ton[8] ] ];
		if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0
				|| dialektoi[$F("διάλεκτος")]["δυϊκός"] == "0") {
			pinakas.splice(3, 3);
		}
		sz = [ 10, 10, 10 ];
	}
	for (r = 0; r < pinakas.length; r++) {
		if (r % 3 == 2 || r % 3 == 1) {
			for (p = 0; p < countTo; p++) {
				ltxt = ("" + pinakas[r][p]).length;
				if (ltxt > sz[p]) {
					sz[p] = ltxt;
				}
			}
		}
	}

	txt = "";
	for (r = 0; r < pinakas.length; r++) {
		stxt = "";
		if (r % 3 == 2 || r % 3 == 1) {
			stxt = "|";
			for (p = 0; p < countTo; p++) {
				half = Math.abs(sz[p] / 2)
						- Math.abs(("" + pinakas[r][p]).length / 2);
				zero = "";
				for (z = 0; z < half; z++) {
					zero += " ";
				}
				ttext = zero + pinakas[r][p];
				while (ttext.length < sz[p]) {
					ttext += " ";
				}
				stxt += ttext + "|";
			}
			stxt += "\n";
		} else {
			sum = 0;
			for (p = 0; p < countTo; p++) {
				sum += sz[p];
			}
			half = Math.ceil(sum / 2) - Math.ceil(("" + pinakas[r]).length / 2);
			zero = "";
			for (z = 0; z < half; z++) {
				zero += " ";
			}
			stxt = zero + pinakas[r] + zero + "\n";
		}
		txt += stxt;
	}
	$("είσοδος").value = txt;
	if (dedomena == false) {
		$("ἐτικέτες").value = "τρέχον, ";
		$("Παρατηρήσεις").value = "";
	} else {
		$("ἐτικέτες").value = dedomena["ἐτικέτες"];
		$("Παρατηρήσεις").value = dedomena["Παρατηρήσεις"];
	}
}

function dedomenaKathgorias() {
	var dedomena = [];
	parts = $("είσοδος").value.split("\n");
	var mxy = 9;
	if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0
			|| dialektoi[$F("διάλεκτος")]["δυϊκός"] == "0") {
		mxy = 6;
	}

	for (z = 2; z < mxy; z += 3) {
		// z=γραμμή = αριθμός
		subparts = parts[z].split("|");
		if (mtl == "ρήμα") {
			for (n = 1; n < 4; n++) {
				dedomena.push(subparts[n].split(","));
			}
		} else {
			for (n = 1; n < 6; n++) {
				dedomena.push(subparts[n].split(","));
			}
		}
	}
	if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0
			&& dialektoi[$F("διάλεκτος")]["δοτική"] == 0) {
		if (mtl == "ρήμα") {
			dedomena = dedomena.slice(0, 3).concat([ [], [], [] ]).concat(
					dedomena.slice(3, 6));
		} else {
			dedomena = dedomena.slice(0, 2).concat([ [] ]).concat(
					dedomena.slice(2, 4)).concat([ [], [], [], [], [] ])
					.concat(dedomena.slice(5, 7)).concat([ [] ]).concat(
							dedomena.slice(7, 9));
		}
	}
	dat = {
		"διάλεκτος" : $F("διάλεκτος"),
		"μέρος του λόγου" : mtl,
		"καταλήξεις" : dedomena,
		"ἐτικέτες" : $("ἐτικέτες").value,
		"Παρατηρήσεις" : $("Παρατηρήσεις").value
	}
	if (mtl == "ρήμα" || mtl == "μετοχή") {
		dat["χρόνος"] = $F("χρόνος");
	}
	return dat;
}

function apothikeusi() {
	message = dedomenaKathgorias();
	if ($("κκατηγορίες").selectedIndex != -1) {
		parts = $F("κκατηγορίες").split(" ");
		kat = parseInt(parts[0]);
		message["ΑΑ"] = kat;
	}
	message = Object.toJSON(message);

	request = "develop/αποθήκευση_καταλήξεων/" + message;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Αποθηκεύτικε!");
				removeOptionsAlternate("κκατηγορίες");
				loadKatalhjeis();
			} else {
				alert("Αποτυχία: " + transport.responseText);
			}
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function diagrafi() {
	if ($("κκατηγορίες").selectedIndex != -1
			&& $("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		message = istoria[index];

		request = "develop/διαγραφή_καταλήξεων/" + Object.toJSON(message);
		var xmlhttp = new Ajax.Request(request, {
			method : 'post',
			onSuccess : function(transport) {
				if (transport.responseText == "OK") {
					alert("Διαγράφηκε!");
					removeOptionsAlternate("κκατηγορίες");
					EN_APXH();
				}
			},
			onFailure : function() {
				alert('Something went wrong in kathgories.');
			}
		});
	}
}

function nea() {
	while ($("ιστορία").length > 0) {
		$("ιστορία").remove(0);
	}
	;
	$("κκατηγορίες").selectedIndex = -1;
	$("είσοδος").value = "";
	$("ἐτικέτες").value = "τρέχον, ";
	$("Παρατηρήσεις").value = "";

	epilogiKathgorias(false, "");
}

function epilogiIstorias() {
	if ($("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		// alert(Object.toJSON(istoria));
		temp = istoria[index];
		epilogiKathgorias(temp, "");
	}
}

function dokimh() {
	if ($("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		temp = istoria[index];
		epilogiKathgorias(temp, $F("δοκιμή"));
	}
}

function trexon() {
	if ($("κκατηγορίες").selectedIndex != -1
			&& $("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		message = istoria[index];
		request = "develop/τρέχον_καταλήξεις/" + Object.toJSON(message);
		var xmlhttp = new Ajax.Request(request, {
			method : 'post',
			onSuccess : function(transport) {
				index2 = $("κκατηγορίες").selectedIndex;
				loadIstoria();
				EN_APXH();
				$("κκατηγορίες").selectedIndex = index2;
			},
			onFailure : function() {
				alert('Something went wrong in kathgories.');
			}
		});
	}
}

function boh_theia() {
	text = "";
	alert(text);
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
	while (obj.options.length > 0) {
		obj.remove(0);
	}
}
