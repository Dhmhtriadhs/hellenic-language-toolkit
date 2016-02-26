var mlt = "ρήμα";
var katalhjeis = null; // dialekto:kathgoria:katalhjeis
var istoria = null;
var dialektoi = null;
var katon = null;
var katon2 = null;
var tonoi = null;

// ΜΟΔΕ
function EN_APXH() {
	$("είσοδος").value = "";
	loadDialektous();
	neos();
	loadKaton();
	allagiMTL('ρήμα');
	// loadKat
	// loadTon
	// loadKatalhjeis();
}

function loadKaton() {
	request = "dump/κατηγοροτονισμοί";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			// alert(transport.responseText);
			var result = eval(transport.responseText);
			katon = result[0];
			katon2 = result[1];
			tonoi = result[2];
			updateKaton();
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function loadDialektous() {
	request = "dump/διάλεκτοι";
	var xmlhttp = new Ajax.Request(request,
			{
				method : 'post',
				onSuccess : function(transport) {
					// alert(transport.responseText);
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
					updateXronoi();
				},
				onFailure : function() {
					alert('Something went wrong in loadDialektous.');
				}
			});
}

function updateKaton() {
	removeOptionsAlternate($("κκατηγορίες"));
	if ((mtl == "ρήμα" || mtl == "μετοχή")
			&& katon[mtl][$F("διάλεκτος")] != undefined) {
		var elm = katon[mtl][$F("διάλεκτος")][$F("χρόνος")];
		var counter = 0;
		for (k = 0; k < elm.length; k++) {
			if (elm[k]["ΑΑ"] != undefined) {
				b = elm[k]["ΑΑ"] + " (" + elm[k]["καταλήξεις"] + ", "
						+ elm[k]["τονισμοί"] + ") ";
				$("κκατηγορίες")[counter] = new Option(b);
				counter += 1;
			}
		}
	}
	$("κκατηγορίες").selectedIndex = 0;
	loadIstoria();
}

function updateXronoi() {
	if (dialektoi == null) {
		return;
	}
	removeOptionsAlternate($("χρόνος"));
	removeOptionsAlternate($("κκατηγορίες"));

	if (mtl == "ρήμα" || mtl == "μετοχή") {
		elm = dialektoi[$F("διάλεκτος")][mtl];
		keys = Object.keys(elm);
		keys.sort()
		var counter = 0;
		for (k = 0; k < keys.length; k++) {
			if (elm[keys[k]].length > 0) {
				$("χρόνος")[counter] = new Option(keys[k]);
				counter += 1;
			}
		}
	}
	$("χρόνος").selectedIndex = 0;
	listXrono();
	updateKaton();
}

function neos() {
	removeOptionsAlternate("κκατηγορίες");
	removeOptionsAlternate("ιστορία");
	$('ρήμα').style.backgroundColor = "lightgray";
	$('μετοχή').style.backgroundColor = "";
	mtl = "ρήμα";
}

function loadIstoria() {
	if ($("κκατηγορίες").selectedIndex != -1) {
		while ($("ιστορία").length > 0) {
			$("ιστορία").remove(0);
		}

		parts = $F("κκατηγορίες").split(" ");
		kat = parseInt(parts[0]);
		var message = {
			"μέρος του λόγου" : mtl,
			"διάλεκτος" : $F("διάλεκτος"),
			"χρόνος" : $F("χρόνος"),
			"ΑΑ" : kat
		};

		request = "develop/ιστορικό_κατηγοροτονισμῶν/" + Object.toJSON(message);
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
	if (val == 'ρήμα') {
		$('ρήμα').style.backgroundColor = "lightgray";
		$('μετοχή').style.backgroundColor = "";
		$('εγκλίσεις').show();
		$('a4').show();
		$('b4').show();
		$('c4').show();
		$('a5').show();
		$('b5').show();
		$('c5').show();
		$('γένη').hide();
	} else if (val == 'μετοχή') {
		$('ρήμα').style.backgroundColor = "";
		$('μετοχή').style.backgroundColor = "lightgray";
		$('εγκλίσεις').hide();
		$('γένη').show();
		$('a4').hide();
		$('b4').hide();
		$('c4').hide();
		$('a5').hide();
		$('b5').hide();
		$('c5').hide();
	}
	mtl = val;
	updateXronoi();
}

function listXrono() {
	removeOptionsAlternate($("κκατηγορίες"));

	if (mtl == "ρήμα" || mtl == "μετοχή") {
		st = {
			"ρήμα" : [ "a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4",
					"b5", "c1", "c2", "c3", "c4", "c5" ],
			"μετοχή" : [ "a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3" ]
		};
		st2 = {
			"ρήμα" : [ "d1", "d2", "d3", "d4", "d5" ],
			"μετοχή" : [ "e1", "e2", "e3" ]
		};
		st3 = [ "f0", "f1", "f2" ];
		for (k = 0; k < st3.length; k++) {
			$(st3[k]).hide();
		}
		for (k = 0; k < st[mtl].length; k++) {
			$(st[mtl][k]).hide();
		}
		for (k = 0; k < st2[mtl].length; k++) {
			$(st2[mtl][k]).hide();
		}
		elm = dialektoi[$F("διάλεκτος")][mtl][$F("χρόνος")];

		var elm2 = {};
		if (katon2[mtl][$F("διάλεκτος")] != undefined) {
			elm2 = katon2[mtl][$F("διάλεκτος")][$F("χρόνος")];
		}
		kkeys = Object.keys(elm2);
		if (mtl == "μετοχή") {
			metx = [ "ek0", "ek1", "ek2", "ek5", "ek6", "ek7", "ek10", "ek11",
					"ek12" ];
			for (ma = 0; ma < metx.length; ma++) {
				removeOptionsAlternate($(metx[ma]));
				for (k2 = 0; k2 < kkeys.length; k2++) {
					$(metx[ma])[k2] = new Option(kkeys[k2]);
				}
			}
		}
		for (k = 0; k < elm.length; k++) {

			if (mtl == "ρήμα") {
				$("d" + (elm[k] % 5 + 1)).show();
				$("f" + parseInt(elm[k] / 5)).show();
			} else if (mtl == "μετοχή") {
				$("e" + (elm[k] % 3 + 1)).show();
				$("f" + parseInt(elm[k] / 3)).show();
			}

			if (mtl == "ρήμα") {
				removeOptionsAlternate($("ek" + elm[k]));
				for (k2 = 0; k2 < kkeys.length; k2++) {
					$("ek" + elm[k])[k2] = new Option(kkeys[k2]);
				}
			}
			$(st[mtl][elm[k]]).show();
		}
	}
}

function tonousola() {
	k = [ "ek0", "ek1", "ek2", "ek3", "ek4", "ek5", "ek6", "ek7", "ek8", "ek9",
			"ek10", "ek11", "ek12", "ek13", "ek14" ];
	for (kk = 0; kk < k.length; kk++) {
		tonous(k[kk]);
	}
}

function tonous(id) {
	if ((mtl == "ρήμα" && $F("εόλα") != null)
			|| (mtl == "μετοχή" && $F("γόλα") != null) 
			|| ((mtl == "ρήμα" || mtl == "μετοχή") && 
					katon2[mtl][$F("διάλεκτος")][$F("χρόνος")][$F(id)].length==0)) {
		id = id.replace("k", "t");
		removeOptionsAlternate($(id));
		for (k2 = 0; k2 < tonoi[mtl].length; k2++) {
			$(id)[k2] = new Option(tonoi[mtl][k2]);
		}
	} else {
		elm2 = katon2[mtl][$F("διάλεκτος")][$F("χρόνος")][$F(id)];
		id = id.replace("k", "t");
		removeOptionsAlternate($(id));
		if (elm2 != undefined) {
			for (k2 = 0; k2 < elm2.length; k2++) {
				$(id)[k2] = new Option(elm2[k2]);
			}
		}
	}
}

function sxediash(pinakas, countTo) {
	var sz = [ 10, 10, 5, 10, 10, 5, 5, 4, 5, 5, 10, 10, 5, 10, 10 ];
	if (pinakas.length == 3) {
		sz = [ 10, 10, 10, 5, 5, 5, 10, 10, 15, 5, 10, 10, 5, 10, 10 ];
	}
	// εύρεση μέγιστου κάθε στήλης: sz
	for (r = 0; r < pinakas.length; r++) {
		for (p = 0; p < countTo; p++) {
			ltxt = ("" + pinakas[r][p]).length;
			if (ltxt > sz[p]) {
				sz[p] = ltxt;
			}
		}
	}

	txt = "";
	for (r = 0; r < pinakas.length; r++) {
		stxt = "";
		if (r % 3 == 2 || r % 3 == 1 || r % 3 == 0) {
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
	return txt;
}

function epilogiKathgorias(dedomena) {
	var ton = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ];
	var countTo = 0;
	var sz = [];
	$("είσοδος").value = "";
	fones = [ "ενεργητική", "μέση", "παθητική" ];
	if (mtl == "μετοχή") {
		geni = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];

		var txt = "";
		$("είσοδος").value = "";
		// alert(Object.toJSON(dedomena));
		for (f = 0; f < 3; f++) {
			foni = fones[f];
			if (foni in dedomena) {
			} else {
				continue;
			}
			$("είσοδος").value += foni + "\n";
			for (g = 0; g < 3; g++) {
				var ton = [ [], [], [], [], [], [], [], [], [], [], [], [], [],
						[], [] ];
				genos = geni[g];
				dat = dedomena[foni][genos];
				for (d = 0; d < dat.length; d++) {
					ton[d] = dat[d];
				}
				countTo = 4;
				pinakas = [
						[ [ genos ], [ 'Ενικός' ], [ 'Δυϊκός' ],
								[ 'Πληθυντικός' ] ],
						[ [ 'Ονομαστική' ], ton[0], ton[5], ton[10] ],
						[ [ 'Γενική' ], ton[1], ton[6], ton[11] ],
						[ [ 'Δοτική' ], ton[2], ton[7], ton[12] ],
						[ [ 'Αιτιατική' ], ton[3], ton[8], ton[13] ],
						[ [ 'Κλητική' ], ton[4], ton[9], ton[14] ] ];
				if (dialektoi[$F("διάλεκτος")]["δοτική"] == 0) {
					pinakas.splice(3, 1);
				}
				if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0) {
					for (z = 0; z < pinakas.length; z++) {
						pinakas[z].splice(2, 1);
					}
					countTo -= 1;
				}
				$("είσοδος").value += sxediash(pinakas, countTo) + "\n";
			}
		}
		// $("είσοδος").value = txt;
	} else if (mtl == "ρήμα") {
		var txt = "";
		for (f = 0; f < 3; f++) {
			foni = fones[f];
			if (foni in dedomena) {
			} else {
				continue;
			}
			pinakas = [ [ [ '' ], [ '' ], [ 'Ενικός' ], [ '' ], [ '' ],
					[ 'Δυϊκός' ], [ '' ], [ '' ], [ 'Πληθυντικός' ], [ '' ] ] ];
			countTo = 10;
			egliseis = [ "οριστική", "υποτακτική", "ευκτική", "προστακτική",
					"απαρέμφατο" ]
			pinakas.push([ [ foni.toUpperCase() ], [ 'α' ], [ 'β' ], [ 'γ' ],
					[ 'α' ], [ 'β' ], [ 'γ' ], [ 'α' ], [ 'β' ], [ 'γ' ] ]);
			for (e = 0; e < egliseis.length; e++) {
				eglish = egliseis[e];
				if (eglish in dedomena[foni]) {
				} else {
					continue;
				}
				var ton = [ [], [], [], [], [], [], [], [], [] ];
				for (s = 0; s < dedomena[foni][eglish].length; s++) {
					ton[s] = dedomena[foni][eglish][s];
				}
				pinakas.push([ eglish, ton[0], ton[1], ton[2], ton[3], ton[4],
						ton[5], ton[6], ton[7], ton[8] ]);
			}
			if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0) {
				for (z = 0; z < pinakas.length; z++) {
					pinakas[z].splice(4, 3);
				}
				countTo -= 3;
			}
			txt += sxediash(pinakas, countTo) + "\n";

		}
		$("είσοδος").value += txt;
	}
}

function apothikeusi() {
	dat = {
		"διάλεκτος" : $F("διάλεκτος"),
		"μέρος του λόγου" : mtl,
		"χρόνος" : $F("χρόνος"),
		"ἐτικέτες" : $("ἐτικέτες").value,
		"Παρατηρήσεις" : $("Παρατηρήσεις").value,
		"καταλήξεις" : [],
		"τονισμοί" : [],
		"λήμμα" : $F("δοκιμή")
	}
	if ($("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		temp = istoria[index];
		dat["ΑΑ"] = temp["ΑΑ"];
	}
	var metx1 = [ "ek0", "ek1", "ek2", "ek3", "ek4", "ek5", "ek6", "ek7",
			"ek8", "ek9", "ek10", "ek11", "ek12", "ek13", "ek14" ];
	var metx2 = [ "et0", "et1", "et2", "et3", "et4", "et5", "et6", "et7",
			"et8", "et9", "et10", "et11", "et12", "et13", "et14" ];
	if (mtl == "μετοχή") {
		metx1 = [ "ek0", "ek1", "ek2", "ek5", "ek6", "ek7", "ek10", "ek11",
				"ek12" ];
		metx2 = [ "et0", "et1", "et2", "et5", "et6", "et7", "et10", "et11",
				"et12" ];
	}
	for (ma = 0; ma < metx1.length; ma++) {
		dat["καταλήξεις"].push(parseInt($F(metx1[ma])));
		dat["τονισμοί"].push(parseInt($F(metx2[ma])));
	}
	message = Object.toJSON(dat);

	request = "develop/αποθήκευση_κατηγοροτονισμῶν/" + message;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Αποθηκεύτικε!");
				removeOptionsAlternate("κκατηγορίες");
				loadKaton();
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

		request = "develop/διαγραφή_κατηγοροτονισμῶν/" + Object.toJSON(message);
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
		$("ἐτικέτες").value = temp["ἐτικέτες"];
		$("Παρατηρήσεις").value = temp["Παρατηρήσεις"];
		// elm = dialektoi[$F("διάλεκτος")][mtl][$F("χρόνος")];
		if (mtl == "ρήμα") {
			for (k = 0; k < 15; k++) {
				id1 = "ek" + k;
				selectValue(id1, temp["καταλήξεις"][k]);
				tonous(id1);
				id2 = "et" + k;
				selectValue(id2, temp["τονισμοί"][k]);
			}
		} else if (mtl == "μετοχή") {
			for (k = 0; k < 9; k++) {
				var id1 = "ek" + k;
				var id2 = "et" + k;
				if (k > 5) {
					id1 = "ek" + (k + 4);
					id2 = "et" + (k + 4);
				} else if (k > 2) {
					id1 = "ek" + (k + 2);
					id2 = "et" + (k + 2);
				}
				selectValue(id1, temp["καταλήξεις"][k]);
				tonous(id1);
				selectValue(id2, temp["τονισμοί"][k]);
			}
		}
		dokimh();
	}
}

function dokimh() {
	dat = {
		"διάλεκτος" : $F("διάλεκτος"),
		"μέρος του λόγου" : mtl,
		"χρόνος" : $F("χρόνος"),
		"ἐτικέτες" : $("ἐτικέτες").value,
		"Παρατηρήσεις" : $("Παρατηρήσεις").value,
		"καταλήξεις" : [],
		"τονισμοί" : [],
		"λήμμα" : $F("δοκιμή")
	}
	if ($("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		temp = istoria[index];
		dat["ΑΑ"] = temp["ΑΑ"];
	}
	var metx1 = [ "ek0", "ek1", "ek2", "ek3", "ek4", "ek5", "ek6", "ek7",
			"ek8", "ek9", "ek10", "ek11", "ek12", "ek13", "ek14" ];
	var metx2 = [ "et0", "et1", "et2", "et3", "et4", "et5", "et6", "et7",
			"et8", "et9", "et10", "et11", "et12", "et13", "et14" ];
	if (mtl == "μετοχή") {
		metx1 = [ "ek0", "ek1", "ek2", "ek5", "ek6", "ek7", "ek10", "ek11",
				"ek12" ];
		metx2 = [ "et0", "et1", "et2", "et5", "et6", "et7", "et10", "et11",
				"et12" ];
	}
	for (ma = 0; ma < metx1.length; ma++) {
		dat["καταλήξεις"].push(parseInt($F(metx1[ma])));
		dat["τονισμοί"].push(parseInt($F(metx2[ma])));
	}

	// alert(Object.toJSON(dat));
	request = "develop/δοκιμή_κατηγοριοτονισμού/" + Object.toJSON(dat);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			// alert(transport.responseText);
			var result = eval(transport.responseText);
			// alert(result[0]);
			epilogiKathgorias(result[0]);
		},
		onFailure : function() {
			alert('Something went wrong in dokimh.');
		}
	});
}

function trexon() {
	if ($("κκατηγορίες").selectedIndex != -1
			&& $("ιστορία").selectedIndex != -1) {
		index = $("ιστορία").selectedIndex;
		message = istoria[index];
		request = "develop/τρέχον_κατηγοροτονισμῶν/" + Object.toJSON(message);
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
