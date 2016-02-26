var mlt = "άρθρο";
var anomala = null; // dialekto:kathgoria:anomala
var dialektoi = null;
var istoria = null;
var metadedomena = {};
// var klimakes = {};
var temp = null;

// ΜΟΔΕ
function EN_APXH() {
	neos();
	loadDialektous();
	loadKatalhjeis();
	loadMetaKlima();
}

function reload() {
	removeOptionsAlternate("κκατηγορίες");
	removeOptionsAlternate("ιστορία");
	loadKatalhjeis();
	loadMetaKlima();
}

function loadMetaKlima() {
	// Φορτώνει τα μεταδεδομένα, τις κλίμακες και τις τιμές τους
	request = "dump/μεταδεδομένα_κλίμακες";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			// var result = transport.responseText.evalJSON(true);
			metadedomena = result[0];
			$("μκ_συμπλήρωση").innerHTML = "";
			keys = Object.keys(metadedomena);
			for (m = 0; m < keys.length; m++) {
				$("μκ_συμπλήρωση").appendChild(new Option(keys[m]));
			}
		},
		onFailure : function() {
			alert('Something went wrong in loadMeta.');
		}
	});
}

function metaValues() {
	key = $F("μκόνομα");
	if (key in metadedomena) {
		$("μκ_τιμή_συμπλήρωση").innerHTML = "";
		for (k = 0; k < metadedomena[key].length; k++) {
			$("μκ_τιμή_συμπλήρωση").appendChild(
					new Option(metadedomena[key][k]));
		}
	}
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
			for (d = 0; d < dias.length; d++) {
				$("διάλεκτος")[d] = new Option(dias[d].toLowerCase());
			}
		},
		onFailure : function() {
			alert('Something went wrong in loadDialektous.');
		}
	});
}

function updateKatalhjeis() {
	if (anomala == null) {
		return;
	}
	removeOptionsAlternate($("κκατηγορίες"));
	var elm = anomala[mtl][$F("διάλεκτος")];
	if (mtl == "ουσιαστικό") {
		for (k = 0; k < elm.length; k++) {
			if ("καταλήξεις" in elm[k]) {
				b = elm[k]["ΑΑ"] + " (" + elm[k]["καταλήξεις"]["καταλήξεις"]
						+ ") ";
				$("κκατηγορίες")[k] = new Option(b);
			} else if ("λήμμα" in elm[k]) {
				b = elm[k]["ΑΑ"] + " (" + elm[k]["λήμμα"] + ") ";
				$("κκατηγορίες")[k] = new Option(b);
			}
		}
	} else if (mtl == "επίρρημα" || mtl == "πρόθεση" || mtl == "επιφώνημα"
			|| mtl == "μόριο" || mtl == "σύνδεσμος") {
		for (k = 0; k < elm.length; k++) {
			b = elm[k]["ΑΑ"] + " (" + elm[k]["λήμμα"] + ") ";
			$("κκατηγορίες")[k] = new Option(b);
		}
	} else if (mtl == "αντωνυμία") {
		for (k = 0; k < elm.length; k++) {
			var b = "";
			if ("κατάληξη" in elm[k]) {
				b = elm[k]["ΑΑ"] + " (" + elm[k]["κατάληξη"] + ") ";
			} else if ("α" in elm[k]["καταλήξεις"]) {
				b = elm[k]["ΑΑ"] + " ("
						+ elm[k]["καταλήξεις"]["α"]["αρσενικό"]["καταλήξεις"]
						+ ") ";
			} else {
				b = elm[k]["ΑΑ"] + " ("
						+ elm[k]["καταλήξεις"]["αρσενικό"]["καταλήξεις"] + ") ";
			}
			$("κκατηγορίες")[k] = new Option(b);
		}
	} else if (mtl == "επίθετο" || mtl == "άρθρο") {
		for (k = 0; k < elm.length; k++) {
			if ("αρσενικό" in elm[k]["καταλήξεις"]) {
				b = elm[k]["ΑΑ"] + " ("
						+ elm[k]["καταλήξεις"]["αρσενικό"]["καταλήξεις"] + ") ";
				$("κκατηγορίες")[k] = new Option(b);
			}
		}
	} else if (mtl == "ρήμα") {
		var counter = 0;
		for (k = 0; k < elm.length; k++) {
			if (elm[k]["ΑΑ"] != undefined) {
				xronos = Object.keys(elm[k]["καταλήξεις"]["ρήμα"])[0];
				foni = Object.keys(elm[k]["καταλήξεις"]["ρήμα"][xronos])[0];
				eglisi = Object
						.keys(elm[k]["καταλήξεις"]["ρήμα"][xronos][foni])[0];
				b = elm[k]["ΑΑ"]
						+ " ("
						+ elm[k]["καταλήξεις"]["ρήμα"][xronos][foni][eglisi]["καταλήξεις"]
						+ ") ";
				$("κκατηγορίες")[counter] = new Option(b);
				counter += 1;
			}
		}
	}
}

function updateKatalhjeis2() {
	if (anomala == null) {
		return;
	}
	removeOptionsAlternate($("κκατηγορίες"));
	dial = $F("διάλεκτος");
	var elm = anomala[mtl][$F("διάλεκτος")];
	if (mtl == "ουσιαστικό") {
		for (k = 0; k < elm.length; k++) {
			if ("καταλήξεις" in elm[k]) {
				b = elm[k]["ΑΑ"] + " (" + elm[k]["καταλήξεις"]["καταλήξεις"]
						+ ") ";
				$("κκατηγορίες")[k] = new Option(b);
			} else if ("λήμμα" in elm[k]) {
				b = elm[k]["ΑΑ"] + " (" + elm[k]["λήμμα"] + ") ";
				$("κκατηγορίες")[k] = new Option(b);
			}
		}
	} else if (mtl == "επίρρημα" || mtl == "πρόθεση" || mtl == "επιφώνημα"
			|| mtl == "μόριο" || mtl == "σύνδεσμος") {
		for (k = 0; k < elm.length; k++) {
			b = elm[k]["ΑΑ"] + " (" + elm[k]["λήμμα"] + ") ";
			$("κκατηγορίες")[k] = new Option(b);
		}
	} else if (mtl == "αντωνυμία") {
		for (k = 0; k < elm.length; k++) {
			var b = "";
			if ("κατάληξη" in elm[k]) {
				b = elm[k]["ΑΑ"] + " (" + elm[k]["κατάληξη"] + ") ";
			} else if ("α" in elm[k]["καταλήξεις"]) {
				b = elm[k]["ΑΑ"] + " ("
						+ elm[k]["καταλήξεις"]["α"]["αρσενικό"]["καταλήξεις"]
						+ ") ";
			} else {
				b = elm[k]["ΑΑ"] + " ("
						+ elm[k]["καταλήξεις"]["αρσενικό"]["καταλήξεις"] + ") ";
			}
			$("κκατηγορίες")[k] = new Option(b);
		}
	} else if (mtl == "επίθετο" || mtl == "άρθρο") {
		for (k = 0; k < elm.length; k++) {
			b = elm[k]["ΑΑ"] + " ("
					+ elm[k]["καταλήξεις"]["αρσενικό"]["καταλήξεις"] + ") ";
			$("κκατηγορίες")[k] = new Option(b);
		}
	} else if (mtl == "ρήμα") {
		var counter = 0;
		for (k = 0; k < elm.length; k++) {
			if (elm[k]["ΑΑ"] != undefined) {
				xronos = Object.keys(elm[k]["καταλήξεις"]["ρήμα"])[0];
				foni = Object.keys(elm[k]["καταλήξεις"]["ρήμα"][xronos])[0];
				eglisi = Object
						.keys(elm[k]["καταλήξεις"]["ρήμα"][xronos][foni])[0];
				b = elm[k]["ΑΑ"]
						+ " ("
						+ elm[k]["καταλήξεις"]["ρήμα"][xronos][foni][eglisi]["καταλήξεις"]
						+ ") ";
				$("κκατηγορίες")[counter] = new Option(b);
				counter += 1;
			}
		}
	}
}

function meden() {
	$('άρθρο').style.backgroundColor = "";
	$("ουσιαστικό").style.backgroundColor = "";
	$('επίθετο').style.backgroundColor = "";
	$('αντωνυμία').style.backgroundColor = "";
	$('ρήμα').style.backgroundColor = "";

	$('επιφώνημα').style.backgroundColor = "";
	$('μόριο').style.backgroundColor = "";
	$('πρόθεση').style.backgroundColor = "";
	$('σύνδεσμος').style.backgroundColor = "";
	$('επίρρημα').style.backgroundColor = "";
}

function neos() {
	removeOptionsAlternate("κκατηγορίες");
	removeOptionsAlternate("ιστορία");
	meden();
	$('άρθρο').style.backgroundColor = "lightgray";
	mtl = "άρθρο";
}

function loadIstoria() {
	if ($("κκατηγορίες").selectedIndex != -1) {
		while ($("ιστορία").length > 0) {
			$("ιστορία").remove(0);
		}

		parts = $F("κκατηγορίες").split(" ");
		kat = parseInt(parts[0]);
		var message = anomala[mtl][$F("διάλεκτος")][kat];
		request = "develop/ιστορικό_ανώμαλων/" + Object.toJSON(message);
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
	meden();
	$(val).style.backgroundColor = "lightgray";
	mtl = val;
	updateKatalhjeis();
}

function loadKatalhjeis() {
	request = "dump/ανώμαλα";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			anomala = result[0];
			updateKatalhjeis();
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
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
	genoi = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];
	xronoi = [ "ενεστώτας", "παρατατικός", "αόριστος", "παρακείμενος",
			"υπερσυντέλικος", "μέλλοντας", "συντελεσμένος μέλλοντας" ];
	fones = [ "ενεργητική", "μέση", "παθητική" ];
	egliseis = [ "οριστική", "υποτακτική", "ευκτική", "προστακτική",
			"απαρέμφατο" ];
	prosopa = [ "α", "β", "γ" ];
	if (mtl == "ουσιαστικό") {
		genos = "";
		if (dedomena != false) {
			if ("καταλήξεις" in dedomena) {
				for (i = 0; i < dedomena["καταλήξεις"]["καταλήξεις"].length; i++) {
					ton[i] = dedomena["καταλήξεις"]["καταλήξεις"][i];
				}
			} else if ("λήμμα" in dedomena) {
				ton[0] = dedomena["λήμμα"];
			}
			genos = dedomena["γένος"];
		}
		countTo = 4;
		pinakas = [
				[ [ genos ], [ 'Ενικός' ], [ 'Δυϊκός' ], [ 'Πληθυντικός' ] ],
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
		$("είσοδος").value = sxediash(pinakas, countTo);
	} else if (mtl == "επίθετο" || mtl == "άρθρο") {
		txt = "";

		for (g = 0; g < genoi.length; g++) {
			genos = genoi[g];
			var ton = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [],
					[] ];
			if (dedomena != false) {
				for (i = 0; i < dedomena["καταλήξεις"][genos]["καταλήξεις"].length; i++) {
					ton[i] = dedomena["καταλήξεις"][genos]["καταλήξεις"][i];
				}
			}

			countTo = 4;
			pinakas = [
					[ [ genos ], [ 'Ενικός' ], [ 'Δυϊκός' ], [ 'Πληθυντικός' ] ],
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
			txt += sxediash(pinakas, countTo) + "\n";
		}
		$("είσοδος").value = txt;
	} else if (mtl == "ρήμα") {
		txt = "";

		for (x = 0; x < xronoi.length; x++) {
			xronos = xronoi[x];
			if (dialektoi[$F("διάλεκτος")]["ρήμα"][xronos].length == 0) {
				continue;
			}

			pinakas = [ [ [ xronos ], [ '' ], [ 'Ενικός' ], [ '' ], [ '' ],
					[ 'Δυϊκός' ], [ '' ], [ '' ], [ 'Πληθυντικός' ], [ '' ] ] ];
			countTo = 10;
			var thesi = -1;
			for (f = 0; f < fones.length; f++) {
				foni = fones[f];
				pinakas.push([ [ foni.toUpperCase() ], [ 'α' ], [ 'β' ],
						[ 'γ' ], [ 'α' ], [ 'β' ], [ 'γ' ], [ 'α' ], [ 'β' ],
						[ 'γ' ] ]);

				for (e = 0; e < egliseis.length; e++) {
					thesi += 1;
					if (dialektoi[$F("διάλεκτος")]["ρήμα"][xronos]
							.indexOf(thesi) == -1) {
						if (thesi % 5 == 0) {
							pinakas.pop();
						}
						continue;
					}
					eglish = egliseis[e];
					var ton = [ [], [], [], [], [], [], [], [], [], [], [], [],
							[], [], [] ];
					if (dedomena != false
							&& dedomena["καταλήξεις"]["ρήμα"][xronos] != undefined
							&& dedomena["καταλήξεις"]["ρήμα"][xronos][foni] != undefined
							&& dedomena["καταλήξεις"]["ρήμα"][xronos][foni][eglish] != undefined) {
						for (i = 0; i < dedomena["καταλήξεις"]["ρήμα"][xronos][foni][eglish]["καταλήξεις"].length; i++) {
							ton[i] = dedomena["καταλήξεις"]["ρήμα"][xronos][foni][eglish]["καταλήξεις"][i];
						}
					}
					pinakas.push([ eglish, ton[0], ton[1], ton[2], ton[3],
							ton[4], ton[5], ton[6], ton[7], ton[8] ]);
				}
			}
			if (dialektoi[$F("διάλεκτος")]["δυϊκός"] == 0) {
				for (z = 0; z < pinakas.length; z++) {
					pinakas[z].splice(4, 3);
				}
				countTo -= 3;
			}
			txt += sxediash(pinakas, countTo) + "\n";
		}
		for (x = 0; x < xronoi.length; x++) {
			xronos = xronoi[x];
			if (dialektoi[$F("διάλεκτος")]["μετοχή"][xronos] == undefined
					|| dialektoi[$F("διάλεκτος")]["μετοχή"][xronos].length == 0) {
				continue;
			}
			txt += xronos.toUpperCase() + "\n";
			// pinakas = [ [ [ xronos ], [ '' ], [ 'Ενικός' ], [ '' ], [ '' ],
			// [ 'Δυϊκός' ], [ '' ], [ '' ], [ 'Πληθυντικός' ], [ '' ] ] ];
			countTo = 10;
			var thesi = -1;
			for (f = 0; f < fones.length; f++) {
				foni = fones[f];
				txt += foni + "\n";
				for (g = 0; g < genoi.length; g++) {
					genos = genoi[g];
					var ton = [ [], [], [], [], [], [], [], [], [], [], [], [],
							[], [], [] ];
					if (dedomena != false
							&& dedomena["καταλήξεις"]["μετοχή"] != undefined
							&& dedomena["καταλήξεις"]["μετοχή"][xronos] != undefined
							&& dedomena["καταλήξεις"]["μετοχή"][xronos][foni] != undefined
							&& dedomena["καταλήξεις"]["μετοχή"][xronos][foni][genos] != undefined) {
						for (i = 0; i < dedomena["καταλήξεις"]["μετοχή"][xronos][foni][genos]["καταλήξεις"].length; i++) {
							ton[i] = dedomena["καταλήξεις"]["μετοχή"][xronos][foni][genos]["καταλήξεις"][i];
						}
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
					txt += sxediash(pinakas, countTo);
				}
			}
			txt += "\n";
		}
		$("είσοδος").value = txt;
	} else if (mtl == "επίρρημα" || mtl == "πρόθεση" || mtl == "επιφώνημα"
			|| mtl == "μόριο" || mtl == "σύνδεσμος") {
		txt = "λήμμα: " + dedomena["λήμμα"] + "\n";
		$("είσοδος").value = txt;
	} else if (mtl == "αντωνυμία") {
		txt = "";
		prosopa = [ "α", "β", "γ" ];
		for (pi = 0; pi < prosopa.length; pi++) {
			prosopo = prosopa[pi];
			txt += prosopo + "\n";
			for (g = 0; g < genoi.length; g++) {
				genos = genoi[g];
				var ton = [ [], [], [], [], [], [], [], [], [], [], [], [], [],
						[], [] ];
				if (dedomena != false) {
					if ("κατάληξη" in dedomena && dedomena != false) {
						if (genos == "αρσενικό" && prosopo == "α") {
							ton[0] = dedomena["κατάληξη"];
						}
					} else if ("αρσενικό" in dedomena["καταλήξεις"]) {
						if (pi == 0) {
							for (i = 0; i < dedomena["καταλήξεις"][genos]["καταλήξεις"].length; i++) {
								ton[i] = dedomena["καταλήξεις"][genos]["καταλήξεις"][i];
							}
						}
					} else {
						for (i = 0; i < dedomena["καταλήξεις"][prosopa[pi]][genos]["καταλήξεις"].length; i++) {
							ton[i] = dedomena["καταλήξεις"][prosopa[pi]][genos]["καταλήξεις"][i];
						}
					}
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
				txt += sxediash(pinakas, countTo) + "\n";
			}
		}
		$("είσοδος").value = txt;
	}

	if (dedomena == false) {
		$("ἐτικέτες").value = "τρέχον, ";
		$("Παρατηρήσεις").value = "";
	} else {
		$("ἐτικέτες").value = dedomena["ἐτικέτες"];
		$("Παρατηρήσεις").value = dedomena["Παρατηρήσεις"];
		changeMeta();
	}
}

function changeMeta() {
	removeOptionsAlternate($("μετα_κλίμακες"));
	index = $("ιστορία").selectedIndex;
	dedomena = istoria[index];
	var counter = 0;
	keys = Object.keys(dedomena["Μεταδεδομένα"]);
	for (k = 0; k < keys.length; k++) {
		$("μετα_κλίμακες")[counter] = new Option("Μεταδεδομένα: " + keys[k]
				+ ": " + dedomena["Μεταδεδομένα"][keys[k]]);
		counter += 1
	}
	keys = Object.keys(dedomena["Κλίμακες"]);
	for (k = 0; k < keys.length; k++) {
		$("μετα_κλίμακες")[counter] = new Option("Κλίμακες: " + keys[k] + ": "
				+ dedomena["Κλίμακες"][keys[k]]);
		counter += 1
	}
}

function επιλογή_μκ() {
	var index = $("μετα_κλίμακες").selectedIndex;
	if (index > -1) {
		parts = $("μετα_κλίμακες")[index].value.split(": ");
		if (parts[0] == "κλίμακες") {
			$("μετα_κλίμα").selectedIndex = 1;
		} else {
			$("μετα_κλίμα").selectedIndex = 0;
		}
		$("μκόνομα").value = parts[1];
		$("μκτιμή").value = parts[2];
	}
}

function metaklimatimes() {
	key = $F("μκόνομα");
	typos = $F("μετα_κλίμα");
	var dedomena = metadedomena;
	if (typos == "κλίμακες") {
		dedomena = klimakes;
	}
	if (key in dedomena) {
		$("μκ_τιμή_συμπλήρωση").innerHTML = "";
		for (m = 0; m < dedomena[key].length; m++) {
			$("μκ_τιμή_συμπλήρωση").appendChild(new Option(dedomena[key][m]));
		}
	}
}

function προσθήκη_μκ() {
	if ($("μκόνομα").value.length > 0 && $("μκτιμή").value.length > 0) {
		mx = $("μετα_κλίμακες").length;
		var offst = mx;
		for (z = 0; z < mx; z++) {
			pro = $("μετα_κλίμακες")[z].value.split(": ")[1];
			mk = $("μετα_κλίμακες")[z].value.split(": ")[0];
			if ($F("μετα_κλίμα") == mk && pro == $("μκόνομα").value) {
				offst = z;
			}
		}
		$("μετα_κλίμακες")[offst] = new Option($F("μετα_κλίμα") + ": "
				+ $("μκόνομα").value + ": " + $("μκτιμή").value);
	}
}

function αφαίρεση_μκ() {
	$("μετα_κλίμακες").remove($("μετα_κλίμακες").selectedIndex);
}

function zero_μκ() {
	$("μκόνομα").value = "";
	$("μκτιμή").value = "";
}

function dedomenaKathgorias() {
	var meta = {};
	var klima = {};
	mk = $("μετα_κλίμακες")
	for (m = 0; m < mk.length; m++) {
		val = mk[m].value.split(": ")
		if (val[0] == "Μεταδεδομένα") {
			meta[val[1]] = val[2];
		} else if (val[0] == "Κλίμακες") {
			klima[val[1]] = val[2];
		}
	}
	dat = {
		"διάλεκτος" : $F("διάλεκτος"),
		"μέρος του λόγου" : mtl,
		"ἐτικέτες" : $("ἐτικέτες").value,
		"Μεταδεδομένα" : meta,
		"Κλίμακες" : klima,
		"Παρατηρήσεις" : $("Παρατηρήσεις").value
	}
	if ($("κκατηγορίες").selectedIndex != -1) {
		parts = $F("κκατηγορίες").split(" ");
		kat = parseInt(parts[0]);
		dat["ΑΑ"] = kat;
	}

	lines = $("είσοδος").value.split("\n");
	if (mtl == "επίρρημα" || mtl == "πρόθεση" || mtl == "επιφώνημα"
			|| mtl == "μόριο" || mtl == "σύνδεσμος") {
		for (l = 0; l < lines.length; l++) {
			line = lines[l].split(":");
			if (line[0].search("λήμμα") != -1) {
				dat["λήμμα"] = line[1].split(",");
			}
		}
		if (!("λήμμα" in dat)) {
			return false;
		}
	} else if (mtl == "άρθρο" || mtl == "επίθετο") {
		var dedomena = {
			"αρσενικό" : [ [], [], [], [], [], [], [], [], [], [], [], [], [],
					[], [] ],
			"θηλυκό" : [ [], [], [], [], [], [], [], [], [], [], [], [], [],
					[], [] ],
			"ουδέτερο" : [ [], [], [], [], [], [], [], [], [], [], [], [], [],
					[], [] ]
		}
		var genos = null;
		for (l = 0; l < lines.length; l++) {
			line = lines[l].split("|");
			if (line.length > 4) {
				if (line[1].toLowerCase().search("ρσενικ") != -1) {
					genos = "αρσενικό";
					continue;
				} else if (line[1].toLowerCase().search("θηλυκ") != -1) {
					genos = "θηλυκό";
					continue;
				} else if (line[1].toLowerCase().search("τερο") != -1) {
					genos = "ουδέτερο";
					continue;
				} else if (genos == null) {
					continue;
				} else if (line[1].toLowerCase().search("νομαστικ") != -1) {
					if (line.length == 5) {
						dedomena[genos][0] = line[2].split(",");
						dedomena[genos][10] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[genos][0] = line[2].split(",");
						dedomena[genos][5] = line[3].split(",");
						dedomena[genos][10] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("ενικ") != -1) {
					if (line.length == 5) {
						dedomena[genos][1] = line[2].split(",");
						dedomena[genos][11] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[genos][1] = line[2].split(",");
						dedomena[genos][6] = line[3].split(",");
						dedomena[genos][11] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("οτικ") != -1) {
					if (line.length == 5) {
						dedomena[genos][2] = line[2].split(",");
						dedomena[genos][12] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[genos][2] = line[2].split(",");
						dedomena[genos][7] = line[3].split(",");
						dedomena[genos][12] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("τιατικ") != -1) {
					if (line.length == 5) {
						dedomena[genos][3] = line[2].split(",");
						dedomena[genos][13] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[genos][3] = line[2].split(",");
						dedomena[genos][8] = line[3].split(",");
						dedomena[genos][13] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("λητικ") != -1) {
					if (line.length == 5) {
						dedomena[genos][4] = line[2].split(",");
						dedomena[genos][14] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[genos][4] = line[2].split(",");
						dedomena[genos][9] = line[3].split(",");
						dedomena[genos][14] = line[4].split(",");
					}
				}
			}
		}
		dat["καταλήξεις"] = dedomena;
		if (!("καταλήξεις" in dat)) {
			return false;
		}
	} else if (mtl == "ουσιαστικό") {
		var dedomena = [ [], [], [], [], [], [], [], [], [], [], [], [], [],
				[], [] ];
		for (l = 0; l < lines.length; l++) {
			line = lines[l].split("|");
			if (line.length > 4) {
				if (line[1].toLowerCase().search("ρσενικ") != -1
						|| line[1].toLowerCase().search("θηλυκ") != -1
						|| line[1].toLowerCase().search("τερο") != -1) {
					dat["γένος"] = line[1];
				} else if (line[1].toLowerCase().search("νομαστικ") != -1) {
					if (line.length == 5) {
						dedomena[0] = line[2].split(",");
						dedomena[10] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[0] = line[2].split(",");
						dedomena[5] = line[3].split(",");
						dedomena[10] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("ενικ") != -1) {
					if (line.length == 5) {
						dedomena[1] = line[2].split(",");
						dedomena[11] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[1] = line[2].split(",");
						dedomena[6] = line[3].split(",");
						dedomena[11] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("οτικ") != -1) {
					if (line.length == 5) {
						dedomena[2] = line[2].split(",");
						dedomena[12] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[2] = line[2].split(",");
						dedomena[7] = line[3].split(",");
						dedomena[12] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("τιατικ") != -1) {
					if (line.length == 5) {
						dedomena[3] = line[2].split(",");
						dedomena[13] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[3] = line[2].split(",");
						dedomena[8] = line[3].split(",");
						dedomena[13] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("λητικ") != -1) {
					if (line.length == 5) {
						dedomena[4] = line[2].split(",");
						dedomena[14] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[4] = line[2].split(",");
						dedomena[9] = line[3].split(",");
						dedomena[14] = line[4].split(",");
					}
				}
			}
		}
		dat["καταλήξεις"] = dedomena;
		if (!("γένος" in dat) || !("καταλήξεις" in dat)) {
			return false;
		}
	} else if (mtl == "αντωνυμία") {
		var dedomena = {
			"α" : {
				"αρσενικό" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ],
				"θηλυκό" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ],
				"ουδέτερο" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ]
			},
			"β" : {
				"αρσενικό" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ],
				"θηλυκό" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ],
				"ουδέτερο" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ]
			},
			"γ" : {
				"αρσενικό" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ],
				"θηλυκό" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ],
				"ουδέτερο" : [ [], [], [], [], [], [], [], [], [], [], [], [],
						[], [], [] ]
			}
		}
		var genos = null;
		var prosopo = null;
		for (l = 0; l < lines.length; l++) {
			line = lines[l].split("|");
			if (line.length > 4 && prosopo != null) {
				if (line[1].toLowerCase().search("ρσενικ") != -1) {
					genos = "αρσενικό";
					continue;
				} else if (line[1].toLowerCase().search("θηλυκ") != -1) {
					genos = "θηλυκό";
					continue;
				} else if (line[1].toLowerCase().search("τερο") != -1) {
					genos = "ουδέτερο";
					continue;
				} else if (genos == null) {
					continue;
				} else if (line[1].toLowerCase().search("νομαστικ") != -1) {
					if (line.length == 5) {
						dedomena[prosopo][genos][0] = line[2].split(",");
						dedomena[prosopo][genos][10] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[prosopo][genos][0] = line[2].split(",");
						dedomena[prosopo][genos][5] = line[3].split(",");
						dedomena[prosopo][genos][10] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("ενικ") != -1) {
					if (line.length == 5) {
						dedomena[prosopo][genos][1] = line[2].split(",");
						dedomena[prosopo][genos][11] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[prosopo][genos][1] = line[2].split(",");
						dedomena[prosopo][genos][6] = line[3].split(",");
						dedomena[prosopo][genos][11] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("οτικ") != -1) {
					if (line.length == 5) {
						dedomena[prosopo][genos][2] = line[2].split(",");
						dedomena[prosopo][genos][12] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[prosopo][genos][2] = line[2].split(",");
						dedomena[prosopo][genos][7] = line[3].split(",");
						dedomena[prosopo][genos][12] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("τιατικ") != -1) {
					if (line.length == 5) {
						dedomena[prosopo][genos][3] = line[2].split(",");
						dedomena[prosopo][genos][13] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[prosopo][genos][3] = line[2].split(",");
						dedomena[prosopo][genos][8] = line[3].split(",");
						dedomena[prosopo][genos][13] = line[4].split(",");
					}
				} else if (line[1].toLowerCase().search("λητικ") != -1) {
					if (line.length == 5) {
						dedomena[prosopo][genos][4] = line[2].split(",");
						dedomena[prosopo][genos][14] = line[3].split(",");
					} else if (line.length == 6) {
						dedomena[prosopo][genos][4] = line[2].split(",");
						dedomena[prosopo][genos][9] = line[3].split(",");
						dedomena[prosopo][genos][14] = line[4].split(",");
					}
				}
			} else if (line.length == 1) {
				if (line[0].toLowerCase().search("α") != -1) {
					prosopo = "α";
					genos = null;
					continue;
				} else if (line[0].toLowerCase().search("β") != -1) {
					prosopo = "β";
					genos = null;
					continue;
				} else if (line[0].toLowerCase().search("γ") != -1) {
					prosopo = "γ";
					genos = null;
					continue;
				}
			}
		}
		dat["καταλήξεις"] = dedomena;
	} else if (mtl == "ρήμα") {
		var dedomena = {
			"ρήμα" : {},
			"μετοχή" : {}
		};
		var xronos = null;
		var foni = null;
		var genos = null;
		var meros = null;
		for (l = 0; l < lines.length; l++) {
			line = lines[l].split("|");
			if (line.length > 4) {
				if (line[1].toLowerCase().search("νεστ") != -1) {
					xronos = "ενεστώτας";
					meros = "ρήμα";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[1].toLowerCase().search("παρατατικ") != -1) {
					xronos = "παρατατικός";
					meros = "ρήμα";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[1].toLowerCase().search("ριστος") != -1) {
					xronos = "αόριστος";
					meros = "ρήμα";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[1].toLowerCase().search("παρακε") != -1) {
					xronos = "παρακείμενος";
					meros = "ρήμα";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[1].toLowerCase().search("περσυντ") != -1) {
					xronos = "υπερσυντέλικος";
					meros = "ρήμα";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[1].toLowerCase().search("συντελεσμ") != -1) {
					xronos = "συντελεσμένος μέλλοντας";
					meros = "ρήμα";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[1].toLowerCase().search("λλοντας") != -1) {
					xronos = "μέλλοντας";
					meros = "ρήμα";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[1].toLowerCase().search("νεργητικ") != -1) {
					foni = "ενεργητική";
					meros = "ρήμα";
					dedomena[meros][xronos][foni] = {};
					continue;
				} else if (line[1].toLowerCase().search("μέση") != -1) {
					foni = "μέση";
					meros = "ρήμα";
					dedomena[meros][xronos][foni] = {};
					continue;
				} else if (line[1].toLowerCase().search("παθητικ") != -1) {
					foni = "παθητική";
					meros = "ρήμα";
					dedomena[meros][xronos][foni] = {};
					continue;
				} else if (line[1].toLowerCase().search("οριστική") != -1) {
					if (line.length == 9) {
						dedomena[meros][xronos][foni]["οριστική"] = [
								line[2].split(","), line[3].split(","),
								line[4].split(","), [], [], [],
								line[5].split(","), line[6].split(","),
								line[7].split(",") ];
					} else if (line.length == 12) {
						dedomena[meros][xronos][foni]["οριστική"] = [
								line[2].split(","), line[3].split(","),
								line[4].split(","), line[5].split(","),
								line[6].split(","), line[7].split(","),
								line[8].split(","), line[9].split(","),
								line[10].split(",") ];
					}
					continue;
				} else if (line[1].toLowerCase().search("υποτακτική") != -1) {
					if (line.length == 9) {
						dedomena[meros][xronos][foni]["υποτακτική"] = [
								line[2].split(","), line[3].split(","),
								line[4].split(","), [], [], [],
								line[5].split(","), line[6].split(","),
								line[7].split(",") ];
					} else if (line.length == 12) {
						dedomena[meros][xronos][foni]["υποτακτική"] = [
								line[2].split(","), line[3].split(","),
								line[4].split(","), line[5].split(","),
								line[6].split(","), line[7].split(","),
								line[8].split(","), line[9].split(","),
								line[10].split(",") ];
					}
					continue;
				} else if (line[1].toLowerCase().search("ευκτική") != -1) {
					if (line.length == 9) {
						dedomena[meros][xronos][foni]["ευκτική"] = [
								line[2].split(","), line[3].split(","),
								line[4].split(","), [], [], [],
								line[5].split(","), line[6].split(","),
								line[7].split(",") ];
					} else if (line.length == 12) {
						dedomena[meros][xronos][foni]["ευκτική"] = [
								line[2].split(","), line[3].split(","),
								line[4].split(","), line[5].split(","),
								line[6].split(","), line[7].split(","),
								line[8].split(","), line[9].split(","),
								line[10].split(",") ];
					}
					continue;
				} else if (line[1].toLowerCase().search("προστακτική") != -1) {
					if (line.length == 9) {
						dedomena[meros][xronos][foni]["προστακτική"] = [
								line[2].split(","), line[3].split(","),
								line[4].split(","), [], [], [],
								line[5].split(","), line[6].split(","),
								line[7].split(",") ];
					} else if (line.length == 12) {
						dedomena[meros][xronos][foni]["προστακτική"] = [
								line[2].split(","), line[3].split(","),
								line[4].split(","), line[5].split(","),
								line[6].split(","), line[7].split(","),
								line[8].split(","), line[9].split(","),
								line[10].split(",") ];
					}
					continue;
				} else if (line[1].toLowerCase().search("απαρέμφατο") != -1) {
					dedomena[meros][xronos][foni]["απαρέμφατο"] = [ line[2]
							.split(",") ];
					continue;
				} else if (meros == "μετοχή"
						&& dedomena[meros][xronos] == undefined) {
					continue
				} else if (meros == "μετοχή"
						&& dedomena[meros][xronos][foni] == undefined) {
					continue
				} else if (meros == "ρήμα") {
					continue
				} else if (line[1].toLowerCase().search("ρσενικ") != -1) {
					genos = "αρσενικό";
					dedomena[meros][xronos][foni][genos] = [ [], [], [], [],
							[], [], [], [], [], [], [], [], [], [], [] ];
					continue;
				} else if (line[1].toLowerCase().search("θηλυκ") != -1) {
					genos = "θηλυκό";
					dedomena[meros][xronos][foni][genos] = [ [], [], [], [],
							[], [], [], [], [], [], [], [], [], [], [] ];
					continue;
				} else if (line[1].toLowerCase().search("τερο") != -1) {
					genos = "ουδέτερο";
					dedomena[meros][xronos][foni][genos] = [ [], [], [], [],
							[], [], [], [], [], [], [], [], [], [], [] ];
					continue;
				} else if (genos == null) {
					continue;
				} else if (line[1].toLowerCase().search("νομαστικ") != -1) {
					if (line.length == 5) {
						dedomena[meros][xronos][foni][genos][0] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][10] = line[3]
								.split(",");
					} else if (line.length == 6) {
						dedomena[meros][xronos][foni][genos][0] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][5] = line[3]
								.split(",");
						dedomena[meros][xronos][foni][genos][10] = line[4]
								.split(",");
					}
				} else if (line[1].toLowerCase().search("ενικ") != -1) {
					if (line.length == 5) {
						dedomena[meros][xronos][foni][genos][1] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][11] = line[3]
								.split(",");
					} else if (line.length == 6) {
						dedomena[meros][xronos][foni][genos][1] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][6] = line[3]
								.split(",");
						dedomena[meros][xronos][foni][genos][11] = line[4]
								.split(",");
					}
				} else if (line[1].toLowerCase().search("οτικ") != -1) {
					if (line.length == 5) {
						dedomena[meros][xronos][foni][genos][2] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][12] = line[3]
								.split(",");
					} else if (line.length == 6) {
						dedomena[meros][xronos][foni][genos][2] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][7] = line[3]
								.split(",");
						dedomena[meros][xronos][foni][genos][12] = line[4]
								.split(",");
					}
				} else if (line[1].toLowerCase().search("τιατικ") != -1) {
					if (line.length == 5) {
						dedomena[meros][xronos][foni][genos][3] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][13] = line[3]
								.split(",");
					} else if (line.length == 6) {
						dedomena[meros][xronos][foni][genos][3] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][8] = line[3]
								.split(",");
						dedomena[meros][xronos][foni][genos][13] = line[4]
								.split(",");
					}
				} else if (line[1].toLowerCase().search("λητικ") != -1) {
					if (line.length == 5) {
						dedomena[meros][xronos][foni][genos][4] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][14] = line[3]
								.split(",");
					} else if (line.length == 6) {
						dedomena[meros][xronos][foni][genos][4] = line[2]
								.split(",");
						dedomena[meros][xronos][foni][genos][9] = line[3]
								.split(",");
						dedomena[meros][xronos][foni][genos][14] = line[4]
								.split(",");
					}
				}

			} else if (line.length == 1) {
				if (line[0].toLowerCase().search("νεστ") != -1) {
					xronos = "ενεστώτας";
					meros = "μετοχή";
					foni = null;
					dedomena[meros][xronos] = {};
					continue;
				} else if (line[0].toLowerCase().search("παρατατικ") != -1) {
					xronos = "παρατατικός";
					meros = "μετοχή";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[0].toLowerCase().search("ριστος") != -1) {
					xronos = "αόριστος";
					meros = "μετοχή";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[0].toLowerCase().search("παρακε") != -1) {
					xronos = "παρακείμενος";
					meros = "μετοχή";
					dedomena[meros][xronos] = {};
					foni = null;
					continue;
				} else if (line[0].toLowerCase().search("περσυντ") != -1) {
					xronos = "υπερσυντέλικος";
					meros = "μετοχή";
					foni = null;
					dedomena[meros][xronos] = {};
					continue;
				} else if (line[0].toLowerCase().search("συντελεσμ") != -1) {
					xronos = "συντελεσμένος μέλλοντας";
					meros = "μετοχή";
					foni = null;
					dedomena[meros][xronos] = {};
					continue;
				} else if (line[0].toLowerCase().search("λλοντας") != -1) {
					xronos = "μέλλοντας";
					meros = "μετοχή";
					foni = null;
					dedomena[meros][xronos] = {};
					continue;
				} else if (line[0].toLowerCase().search("νεργητικ") != -1) {
					foni = "ενεργητική";
					meros = "μετοχή";
					dedomena[meros][xronos][foni] = {};
					continue;
				} else if (line[0].toLowerCase().search("μέση") != -1) {
					foni = "μέση";
					meros = "μετοχή";
					dedomena[meros][xronos][foni] = {};
					continue;
				} else if (line[0].toLowerCase().search("παθητικ") != -1) {
					foni = "παθητική";
					meros = "μετοχή";
					dedomena[meros][xronos][foni] = {};
					continue;
				}
			}
		}
		dat["καταλήξεις"] = dedomena;
	}
	return dat;
}

function apothikeusi() {
	message = Object.toJSON(dedomenaKathgorias());
	request = "develop/αποθήκευση_ανώμαλων/" + message;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Αποθηκεύτικε!");
				removeOptionsAlternate("κκατηγορίες");
				reload();
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

		request = "develop/διαγραφή_ανώμαλων/" + Object.toJSON(message);
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
	while ($("μετα_κλίμακες").length > 0) {
		$("μετα_κλίμακες").remove(0);
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
		request = "develop/τρέχον_ανώμαλων/" + Object.toJSON(message);
		var xmlhttp = new Ajax.Request(request, {
			method : 'post',
			onSuccess : function(transport) {
				index2 = $("κκατηγορίες").selectedIndex;
				loadIstoria();
				EN_APXH();
				$("κκατηγορίες").selectedIndex = index2;
			},
			onFailure : function() {
				alert('Something went wrong in trexon.');
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
