var mlt = "ουσιαστικό";
var tonismoi = null; // dialekto:kathgoria:tonoi
var istoria = null; // [ΑΑ, Διάλεκτος, Ημερομηνία, Συγγραφέας, Flags, τονισμοί,
					// Παρατηρήσεις]

// ΜΟΔΕ
function EN_APXH() {
	neos();
	loadDialektous();
	loadTonismous();
}

function loadDialektous() {
	request = "dump/διάλεκτοι";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			dialektoi = result[0];
			removeOptionsAlternate($("διάλεκτος"));
			var dias = Object.keys(dialektoi);
			var counter = 0;
			for (d = 0; d < dias.length; d++) {
				if (dialektoi[dias[d]]["εικονική"].length==0) {
					$("διάλεκτος")[counter] = new Option(dias[d].toLowerCase());
					counter += 1;}
			}
		},
		onFailure : function() {
			alert('Something went wrong in loadDialektous.');
		}
	});
}

function updateTonismous() {
	if (tonismoi == null) {
		return;
	}
	removeOptionsAlternate($("κκατηγορίες"));

	var elm = tonismoi[mtl][$F("διάλεκτος")];
	for (k = 0; k < elm.length; k++) {
		b = elm[k]["ΑΑ"] + " (" + elm[k]["τονισμοί"] + ") ";
		$("κκατηγορίες")[k] = new Option(b);
	}
}

function updateTonismous2() {
	if (tonismoi == null) {
		return;
	}
	removeOptionsAlternate($("κκατηγορίες"));
	var elm = tonismoi[mtl][$F("διάλεκτος")];
	for (k = 0; k < elm.length; k++) {
		b = elm[k]["ΑΑ"] + " (" + elm[k]["τονισμοί"] + ") ";
		$("κκατηγορίες")[k] = new Option(b);
	}
}

function neos() {
	removeOptionsAlternate("κκατηγορίες");
	removeOptionsAlternate("ιστορία");
	$("ουσιαστικό").style.backgroundColor = "lightgray";
	$('επίθετο').style.backgroundColor = "";
	$('ρήμα').style.backgroundColor = "";
	mtl = "ουσιαστικό";
}

function loadIstoria() {
	if ($("κκατηγορίες").selectedIndex != -1) {
		while ($("ιστορία").length>0) {$("ιστορία").remove(0);};
		parts = $F("κκατηγορίες").split(" ");
		kat = parseInt(parts[0]);
		message = tonismoi[mtl][$F("διάλεκτος")][kat];
		//alert(Object.toJSON(message));
		//message["τονισμοί"] = [];
		request = "develop/ιστορικό_τονισμού/" + Object.toJSON(message);
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
							//if (istoria[k]['ἐτικέτες'].match("τρέχον")) {
								//$("πΙστορίας")[counter].selected;
								//trex=k;}
							
							//if (maxdate<istoria[k]["Ἡμερομηνία"]) {
								//maxd_pos = k;
								//maxdate=istoria[k]["Ἡμερομηνία"];}
						}
						$("ιστορία").selectedIndex = 0;
						epilogiIstorias();
						//if (trex==-1) { trex=maxd_pos;}
						//showDialekto(istoria[trex]);
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
	} else if (val == 'επίθετο') {
		$("ουσιαστικό").style.backgroundColor = "";
		$('επίθετο').style.backgroundColor = "lightgray";
		$('ρήμα').style.backgroundColor = "";
	} else if (val == 'ρήμα') {
		$("ουσιαστικό").style.backgroundColor = "";
		$('επίθετο').style.backgroundColor = "";
		$('ρήμα').style.backgroundColor = "lightgray";
	}
	mtl = val;
	updateTonismous();
}

function loadTonismous() {
	request = "dump/τονισμοί";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			// alert(transport.responseText);
			var result = eval(transport.responseText);
			tonismoi = result[0];
			updateTonismous();
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function epilogiTonismou(dedomena) {
	var ton = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ];
	if (dedomena != false) {
		parts = $F("κκατηγορίες").split(" ");
		kat = dedomena["ΑΑ"];
		ton = dedomena["τονισμοί"];
	}
	var countTo = 0;
	var sz = [];

	if (mtl == "ουσιαστικό" || mtl == "επίθετο") {
		countTo = 5;
		pinakas = [
				[ [ 'Ενικός' ] ],
				[ [ 'Ονομαστική' ], [ 'Γενική' ], [ 'Δοτική' ], [ 'Αιτιατική' ], [ 'Κλητική' ] ],
				[ ton[0], ton[1], ton[2], ton[3], ton[4] ],
				[ [ 'Δυϊκός' ] ],
				[ [ 'Ονομαστική' ], [ 'Γενική' ], [ 'Δοτική' ],	[ 'Αιτιατική' ], [ 'Κλητική' ] ],
				[ ton[5], ton[6], ton[7], ton[8], ton[9] ],
				[ [ 'Πληθυντικός' ] ],
				[ [ 'Ονομαστική' ], [ 'Γενική' ], [ 'Δοτική' ],	[ 'Αιτιατική' ], [ 'Κλητική' ] ],
				[ ton[10], ton[11], ton[12], ton[13], ton[14] ] ];
		if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0 || dialektoi[$F("διάλεκτος")]["δυϊκός"] == "0") {
			pinakas.splice(3, 3);
		}
		if (dialektoi[$F("διάλεκτος")]["δοτική"] == 0 || dialektoi[$F("διάλεκτος")]["δοτική"] == "0") {
			for(z=0;z<pinakas.length;z++) {
				if(z%3!=0){
				pinakas[z].splice(2, 1);}}
			countTo -= 1;
		}
		sz = [ 10, 10, 10, 10, 10 ];
	} else if (mtl == "ρήμα") {
		countTo = 3;
		pinakas = [ [ [ 'Ενικός' ] ], 
		            [ [ 'α' ], [ 'β' ], [ 'γ' ] ],
		            [ ton[0], ton[1], ton[2] ], 
		            [ [ 'Δυϊκός' ] ],
		            [ [ 'α' ], [ 'β' ], [ 'γ' ] ], 
		            [ ton[3], ton[4], ton[5] ],
		            [ [ 'Πληθυντικός' ] ], 
		            [ [ 'α' ], [ 'β' ], [ 'γ' ] ],
		            [ ton[6], ton[7], ton[8] ] ];
		if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0 || dialektoi[$F("διάλεκτος")]["δυϊκός"] == "0") {
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

function dedomenaTonismou() {
	var dedomena = [];
	parts = $("είσοδος").value.split("\n");
	var mxy = 9;
	if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0 || dialektoi[$F("διάλεκτος")]["δυϊκός"] == "0") {mxy = 6;}
	
	for (z = 2; z < mxy; z += 3) {
		subparts = parts[z].split("|");
		if (mtl=="ρήμα") {
			for (n = 1; n < 4; n++) {dedomena.push(subparts[n].split(","));}
		} else {
			for (n = 1; n < 6; n++) {dedomena.push(subparts[n].split(","));}
		}
	}
	
	if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0 && dialektoi[$F("διάλεκτος")]["δοτική"] == 0) {
		if (mtl=="ρήμα") {
			dedomena = dedomena.slice(0,3).concat([[],[],[]]).concat(dedomena.slice(3,6));
		} else {
			dedomena = dedomena.slice(0,2).concat([[]]).concat(dedomena.slice(2,4))
				.concat([[],[],[],[],[]]).concat(dedomena.slice(5,7))
				.concat([[]]).concat(dedomena.slice(7,9));
		}
	}
	
	dat = {
		"διάλεκτος" : $F("διάλεκτος"),
		"μέρος του λόγου" : mtl,
		"τονισμοί" : dedomena,
		"ἐτικέτες" : $("ἐτικέτες").value,
		"Παρατηρήσεις" : $("Παρατηρήσεις").value
	}
	return dat;
}

function apothikeusi() {
	message = dedomenaTonismou();
	if ($("κκατηγορίες").selectedIndex != -1) {
		parts = $F("κκατηγορίες").split(" ");
		kat = parseInt(parts[0]);
		message["ΑΑ"] = kat;
	}
	message = Object.toJSON(message);
	request = "develop/αποθήκευση_τονισμού/" + message;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Αποθηκεύτικε!");
				removeOptionsAlternate("κκατηγορίες");
				EN_APXH();
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
	if ($("κκατηγορίες").selectedIndex != -1 &&
		$("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		message = istoria[index];

		request = "develop/διαγραφή_τονισμού/" + Object.toJSON(message);
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
	while ($("ιστορία").length>0) {$("ιστορία").remove(0);};
	$("κκατηγορίες").selectedIndex = -1;
	$("είσοδος").value = "";
	$("ἐτικέτες").value = "default, ";
	$("Παρατηρήσεις").value = "";

	epilogiTonismou(false);
}

function epilogiIstorias() {
	if ($("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		// alert(Object.toJSON(istoria));
		temp = istoria[index];
		epilogiTonismou(temp);
	}
}

function trexon() {
	if ($("κκατηγορίες").selectedIndex != -1 &&
			$("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		message = istoria[index];
		request = "develop/τρέχον_τονισμός/" + Object.toJSON(message);
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
