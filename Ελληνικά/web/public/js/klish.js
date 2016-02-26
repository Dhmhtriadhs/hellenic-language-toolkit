var dialektoi = null;
var arthra = null;
var antonimies = null;
var epitheta = null;
var ousiastika = null;
var metoxes = null;
var rhmata = null;
var aklhto = null;

function EN_APXH(mtl) {
	loadDialektous();
	loadArthra(mtl);
}

function loadArthra(mtl) {
	request = "dump/" + mtl;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			if (mtl == "άρθρο") {
				arthra = result[0];
			} else if (mtl == "αντωνυμία") {
				antonimies = result[0];
			} else if (mtl == "μόριο" || mtl == "επίρρημα" || mtl == "πρόθεση"
					|| mtl == "σύνδεσμος" || mtl == "επιφώνημα") {
				aklhto = result[0];
			} else if (mtl == "ουσιαστικό") {
				ousiastika = result[0];
			} else if (mtl == "επίθετο") {
				epitheta = result[0];
			} else if (mtl == "ρήμα") {
				rhmata = result[0];
			} else if (mtl == "μετοχή") {
				metoxes = result[0];
			}

			removeOptionsAlternate($("λέξεις"));
			var dias = Object.keys(result[0][$F("διάλεκτος")]);
			for (d = 0; d < dias.length; d++) {
				$("λέξεις")[d] = new Option(dias[d].toLowerCase());
			}
		},
		onFailure : function() {
			alert('Something went wrong in loadArthra.');
		}
	});
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

function updateArthra() {
	removeOptionsAlternate($("λέξεις"));
	$("αποτελέσματα").innerHTML = "";
	if ($F("διάλεκτος") in arthra) {
		var dias = arthra[$F("διάλεκτος")];
		for (d = 0; d < dias.length; d++) {
			$("λέξεις")[d] = new Option(
					dias[d]["καταλήξεις"]["αρσενικό"]["καταλήξεις"][0]);
			$("λέξεις")[d].value = d;
		}
		if (dias.length > 0) {
			$("λέξεις").selectedIndex = 0;
			showArthra();
		}
	}
}

function updateOysiastika() {
	$("αποτελέσματα").innerHTML = "";
	removeOptionsAlternate($("λέξεις"));
	var meros = [];
	if ($("τύπος").innerHTML == "ουσιαστικό") {
		meros = ousiastika;
	} else if ($("τύπος").innerHTML == "μετοχή") {
		meros = metoxes;
	} else if ($("τύπος").innerHTML == "ρήμα") {
		meros = rhmata;
	} else if ($("τύπος").innerHTML == "επίθετο") {
		meros = epitheta;
	}
	for (a2 = 0; a2 < meros[$F("διάλεκτος")].length; a2++) {
		$("λέξεις")[a2] = new Option(meros[$F("διάλεκτος")][a2]);
	}
}

function showRhma(result) {
	$("αποτελέσματα").innerHTML = "";

	table = document.createElement("table");
	tbody = document.createElement("tbody");

	xronoi = Object.keys(result);
	for (x = 0; x < xronoi.length; x++) {
		xronos = xronoi[x];
		tr = document.createElement("tr");
		th = document.createElement("th");
		text = document.createTextNode(xronos);
		h4 = document.createElement("h4");
		h4.style.textAlign = "center";
		h4.appendChild(text);
		th.appendChild(h4);
		th.colSpan = 10;
		th.style.backgroundColor = "lightgrey";
		tr.appendChild(th);
		tbody.appendChild(tr);
		fones = Object.keys(result[xronos]);
		for (f = 0; f < fones.length; f++) {
			foni = fones[f];
			tr = document.createElement("tr");
			th = document.createElement("th");
			text = document.createTextNode(foni);
			h5 = document.createElement("h5");
			h5.style.textAlign = "center";
			h5.appendChild(text);
			th.appendChild(h5);
			th.colSpan = 10;
			tr.appendChild(th);
			tbody.appendChild(tr);
			egliseis = Object.keys(result[xronos][foni]);

			for (e = 0; e < egliseis.length; e++) {
				var tr = document.createElement("tr");
				eglish = egliseis[e];
				th = document.createElement("th");
				text = document.createTextNode(eglish);
				th.appendChild(text);
				tr.appendChild(th);
				klimena = result[xronos][foni][eglish];
				for (k = 0; k < klimena.length; k++) {
					td = document.createElement("td");
					text = document.createTextNode(klimena[k]);
					td.appendChild(text);
					tr.appendChild(td);
				}
				tbody.appendChild(tr);
			}

			// table = fillArthra(pack, false);
			// td = document.createElement("td");
			// h5 = document.createElement("h5");
			// text = document.createTextNode(xronos+" "+foni);
			// h5.style.textAlign = "center";
			// h5.appendChild(text);
			// td.appendChild(h5);
			// td.appendChild(table);
			// td.style.align = "center";
			// tr.appendChild(td);
		}
	}
	// table = document.createElement("table");
	// tbody = document.createElement("tbody");
	// tbody.appendChild(tr);
	// table.appendChild(tbody);
	table.appendChild(tbody);
	$("αποτελέσματα").appendChild(table);
}

function fillMetoxh(result) {

	$("αποτελέσματα").innerHTML = "";
	xronoi = Object.keys(result);
	tr = document.createElement("tr");
	for (x = 0; x < xronoi.length; x++) {
		xronos = xronoi[x];
		fones = Object.keys(result[xronos]);

		for (f = 0; f < fones.length; f++) {
			foni = fones[f];

			var pack = [// [αριθμός-πτώση, [αρχαία,δημοτική]]
					[ [ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ] ], // αρσενικά
					[ [ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ] ], // θηλυκό
					[ [ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ],
							[ [], [] ], [ [], [] ], [ [], [] ] ] ]; // ουδέτερο
			genoi = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];
			for (g = 0; g < 3; g++) {
				genos = genoi[g];
				a4 = result[xronos][foni][genos];
				for (aa = 0; aa < a4.length; aa++) {
					pack[g][aa][0] = a4[aa];
				}
			}
			table = fillArthra(pack, false);
			td = document.createElement("td");
			h5 = document.createElement("h5");
			text = document.createTextNode(xronos + " " + foni);
			h5.style.textAlign = "center";
			h5.appendChild(text);
			td.appendChild(h5);
			td.appendChild(table);
			td.style.align = "center";
			tr.appendChild(td);
		}
	}
	table = document.createElement("table");
	tbody = document.createElement("tbody");
	tbody.appendChild(tr);
	table.appendChild(tbody);
	$("αποτελέσματα").appendChild(table);
}

function klineOusiastiko() {
	request = "κλίση_web/" + $("τύπος").innerHTML + "/" + $F("διάλεκτος") + "/"
			+ $F("λέξεις");
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			if ($("τύπος").innerHTML == "ουσιαστικό") {
				fillOusiastiko(result[0]);
			} else if ($("τύπος").innerHTML == "επίθετο") {
				fillEpitheto(result[0]);
			} else if ($("τύπος").innerHTML == "ρήμα") {
				showRhma(result[0]);
			} else if ($("τύπος").innerHTML == "μετοχή") {
				fillMetoxh(result[0]);
			}
		},
		onFailure : function() {
			alert('Something went wrong in klineOusiastiko.');
		}
	});
}

function fillOusiastiko(result) {
	$("αποτελέσματα").innerHTML = "";
	table = document.createElement("table");
	// HEAD
	thead = document.createElement("thead");
	var tr = document.createElement("tr");
	th = document.createElement("th");
	tr.appendChild(th);
	ari8moi = [ "Ενικός", "Δυϊκός", "Πληθυντικός" ];
	for (g = 0; g < 3; g++) {
		th = document.createElement("th");
		text = document.createTextNode(ari8moi[g]);
		th.appendChild(text);
		if (g != 1) {
			th.style.backgroundColor = "lightgray";
		}
		tr.appendChild(th);
	}
	thead.appendChild(tr);
	table.appendChild(thead);
	// BODY
	tbody = document.createElement("tbody");
	ptoseis = [ "Ονομαστική", "Γενική", "Δοτική", "Αιτιατική", "Κλητική" ];
	for (a = 0; a < ptoseis.length; a++) {
		tr = document.createElement("tr");
		th = document.createElement("th");

		text = document.createTextNode(ptoseis[a]);
		th.appendChild(text);
		tr.appendChild(th);

		for (p = 0; p < 3; p++) {
			th = document.createElement("th");
			text = document.createTextNode(result[p * 5 + a]);
			th.appendChild(text);
			tr.appendChild(th);
		}
		tbody.appendChild(tr);
	}
	table.appendChild(tbody);
	$("αποτελέσματα").appendChild(table);
}

function fillEpitheto(result) {
	$("αποτελέσματα").innerHTML = "";
	var pack = [// [αριθμός-πτώση, [αρχαία,δημοτική]]
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ], // αρσενικά
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ], // θηλυκό
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ] ]; // ουδέτερο
	genoi = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];

	for (g = 0; g < 3; g++) {
		a4 = result[g];
		for (aa = 0; aa < a4.length; aa++) {
			pack[g][aa] = a4[aa];
		}
	}
	table = fillArthra(pack);
	$("αποτελέσματα").appendChild(table);
}

function updateEpitheta(dialektoi) {
	var counter = 0;

	removeOptionsAlternate($("λέξεις"));

	dkeys = Object.keys(dialektoi);
	var showD = false;
	if (dkeys.length == 2) {
		showD = true;
	}
	for (d = 0; d < dkeys.length; d++) {
		for (a = 0; a < epitheta.length; a++) {
			if (epitheta[a][0] == dialektoi[d]) {
				for (a2 = 0; a2 < epitheta[a][1].length; a2++) {
					typos = epitheta[a][1][a2];
					if (showD) {
						$("λέξεις")[counter] = new Option(typos + ": "
								+ dialektoi[d]);
					} else {
						$("λέξεις")[counter] = new Option(typos);
					}
					counter += 1;
				}
			}
		}
	}
}

function loadAntonimies() {
	// αναλύει το κείμενο από το textarea id="κείμενο"
	// και συμπληρώνει τον πίνακα id="αποτέλεσμα"
	request = "dump/" + Object.toJSON([ "κοινή", "δημοτική" ]) + "/"
			+ $("τύπος").innerHTML;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			// var result = transport.responseText.evalJSON(true);
			antonimies = result;
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
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

function updateAntonimies() {
	removeOptionsAlternate($("τύπος_αντωνυμίες"));
	removeOptionsAlternate($("λέξεις"));
	removeOptionsAlternate($("άλλα"));
	if ($F("διάλεκτος") in antonimies) {
		dkeys = Object.keys(antonimies[$F("διάλεκτος")]);
		for (a = 0; a < dkeys.length; a++) {
			$("τύπος_αντωνυμίες")[a] = new Option(dkeys[a]);
		}
		$("τύπος_αντωνυμίες").selectedIndex = 0;
		loadLexeis();
	}
}

function loadLexeis() {
	removeOptionsAlternate($("λέξεις"));
	lexeis = antonimies[$F("διάλεκτος")][$F("τύπος_αντωνυμίες")];
	for (counter = 0; counter < lexeis.length; counter++) {
		lexi = lexeis[counter];
		var lex = "";
		if ("κατάληξη" in lexi) {
			lex = lexi["κατάληξη"];
		} else if ("αρσενικό" in lexi["καταλήξεις"]) {
			var anto = lexi["καταλήξεις"]["αρσενικό"]["καταλήξεις"];
			for (op = 0; op < anto.length; op++) {
				lex = anto[op];
				if (lex.length > 0) {
					break;
				}
			}
		} else {
			var anto = lexi["καταλήξεις"]["α"]["αρσενικό"]["καταλήξεις"];
			for (op = 0; op < anto.length; op++) {
				lex = anto[op];
				if (lex.length > 0) {
					break;
				}
			}
		}
		$("λέξεις")[counter] = new Option(lex);
	}
	$("λέξεις").selectedIndex = 0;
	showAntonimies();
}

function showAntonimies() {
	$("Τίτλος").innerHTML = "";
	$("αποτελέσματα").innerHTML = "";
	$("αποτελέσματα2").innerHTML = "";
	$("αποτελέσματα3").innerHTML = "";

	var pack = [// [αριθμός-πτώση, [αρχαία,δημοτική]]
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ], // αρσενικά
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ], // θηλυκό
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ] ]; // ουδέτερο

	genoi = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];
	var lexi = antonimies[$F("διάλεκτος")][$F("τύπος_αντωνυμίες")][$("λέξεις").selectedIndex];

	if ("κατάληξη" in lexi) {
		$("αποτελέσματα").innerHTML += "Άκλητο: " + lexi["κατάληξη"];
	} else if ("αρσενικό" in lexi["καταλήξεις"]) {
		for (g = 0; g < 3; g++) {
			a4 = lexi["καταλήξεις"][genoi[g]]["καταλήξεις"];
			for (aa = 0; aa < a4.length; aa++) {
				pack[g][aa] = a4[aa];
			}
		}
		table = fillArthra(pack);
		$("αποτελέσματα").appendChild(table);
	} else if ("α" in lexi["καταλήξεις"]) {
		prosopa = [ "α", "β", "γ" ];
		for (pp = 0; pp < 3; pp++) {
			pack = [// [αριθμός-πτώση, [αρχαία,δημοτική]]
			[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ], // αρσενικά
			[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ], // θηλυκό
			[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ] ]; // ουδέτερο
			genoi = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];
			for (g = 0; g < 3; g++) {
				a4 = lexi["καταλήξεις"][prosopa[pp]][genoi[g]]["καταλήξεις"]
				for (aa = 0; aa < a4.length; aa++) {
					pack[g][aa] = a4[aa];
				}
			}
			table = fillArthra(pack);
			if (pp == 0) {
				$("αποτελέσματα").innerHTML += "<h5> Πρόσωπο: " + prosopa[pp]
						+ "</h5>";
				$("αποτελέσματα").appendChild(table);
			} else if (pp == 1) {
				$("αποτελέσματα2").innerHTML += "<h5>Πρόσωπο: " + prosopa[pp]
						+ "</h5>";
				$("αποτελέσματα2").appendChild(table);
			} else if (pp == 2) {
				$("αποτελέσματα3").innerHTML += "<h5>Πρόσωπο: " + prosopa[pp]
						+ "</h5>";
				$("αποτελέσματα3").appendChild(table);
			}
		}
	}
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

function showDump() {
	result = aklhto[$F("διάλεκτος")];
	$("αποτελέσματα").innerHTML = "";
	table = document.createElement("table");
	// HEAD
	thead = document.createElement("thead");
	var tr = document.createElement("tr");
	th = document.createElement("th");
	text = document.createTextNode($F("διάλεκτος"))
	th.appendChild(text);
	th.colSpan = "2";
	tr.appendChild(th);
	thead.appendChild(tr);

	tr = document.createElement("tr");
	th = document.createElement("th");
	text = document.createTextNode("Λήμμα")
	th.appendChild(text);
	tr.appendChild(th);
	th = document.createElement("th");
	text = document.createTextNode("Τύπος")
	th.appendChild(text);

	tr.appendChild(th);
	thead.appendChild(tr);
	table.appendChild(thead);
	// BODY
	tbody = document.createElement("tbody");
	for (e = 0; e < result.length; e++) {
		tr = document.createElement("tr");
		td = document.createElement("td");
		text = document.createTextNode(result[e]['λήμμα']);
		td.appendChild(text);
		tr.appendChild(td);
		td = document.createElement("td");
		text = document.createTextNode(result[e]['Μεταδεδομένα']['ιδιότητες']);
		td.appendChild(text);
		tr.appendChild(td);
		table.appendChild(tr);
	}
	table.appendChild(tbody);
	$("αποτελέσματα").appendChild(table);
}

function fillArthra(pack) {
	table = document.createElement("table");
	// HEAD
	thead = document.createElement("thead");
	var tr = document.createElement("tr");
	th = document.createElement("th");
	tr.appendChild(th);
	genoi = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];
	for (g = 0; g < 3; g++) {
		th = document.createElement("th");
		text = document.createTextNode(genoi[g]);
		th.appendChild(text);
		th.colSpan = "2";
		if (g != 1) {
			th.style.backgroundColor = "lightgray";
		}
		tr.appendChild(th);
	}
	thead.appendChild(tr);
	table.appendChild(thead);

	// BODY
	tbody = document.createElement("tbody");
	ari8moi = [ "Ενικός", "Δυϊκός", "Πληθυντικός" ];
	ptoseis = [ "Ονομαστική", "Γενική", "Δοτική", "Αιτιατική", "Κλητική" ];
	genoi = [ "Αρσενικό", "Θηλυκό", "Ουδέτερο" ];

	for (a = 0; a < 3; a++) {
		tr = document.createElement("tr");
		th = document.createElement("th");
		tr.appendChild(th);
		th = document.createElement("th");
		th.colSpan = "6";
		text = document.createTextNode(ari8moi[a]);
		th.appendChild(text);
		tr.appendChild(th);
		table.appendChild(tr);
		for (p = 0; p < ptoseis.length; p++) {
			tr = document.createElement("tr");
			th = document.createElement("th");
			text = document.createTextNode(ptoseis[p]);
			th.appendChild(text);
			tr.appendChild(th);
			for (g = 0; g < 3; g++) {
				td = document.createElement("td");
				var txt = pack[g][a * 5 + p];

				text = document.createTextNode(txt);
				td.appendChild(text);
				td.colSpan = "2";
				if (g != 1) {
					td.style.backgroundColor = "lightgray";
				}
				tr.appendChild(td);
			}
			table.appendChild(tr);
		}
	}

	table.appendChild(tbody);
	return table;
}

function showArthra() {
	$("αποτελέσματα").innerHTML = "";
	var pack = [// [αριθμός-πτώση, []]
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ], // αρσενικά
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ], // θηλυκό
	[ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ] ]; // ουδέτερο
	result = arthra[$F("διάλεκτος")][$F("λέξεις")];

	genoi = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];
	for (g = 0; g < 3; g++) {
		lexeis = result["καταλήξεις"][genoi[g]]["καταλήξεις"];
		for (l = 0; l < lexeis.length; l++) {
			pack[g][l] = lexeis[l];
		}
	}

	$("αποτελέσματα").appendChild(fillArthra(pack));
}

function klishArthra(dialektoi) {
	// αναλύει το κείμενο από το textarea id="κείμενο"
	// και συμπληρώνει τον πίνακα id="αποτέλεσμα"
	request = "κλίση/" + Object.toJSON(dialektoi) + "/το";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			// var result = transport.responseText.evalJSON(true);
			showArthra(result, dialektoi);
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function klish() {
	// αναλύει το κείμενο από το textarea id="κείμενο"
	// και συμπληρώνει τον πίνακα id="αποτέλεσμα"
	request = "κλίση/" + $F("διάλεκτος") + "/" + $F("λέξη");
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			// var result = transport.responseText.evalJSON(true);
			fillTable(result);
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function fillProsopo(result, tbody) {
	for (y = 0; y < result.length; y++) {
		prosopa = Object.keys(result[y]);
		for (p = 0; p < prosopa.length; p++) {
			prosopo = prosopa[p];

			row = document.createElement("tr");
			cellText = document.createTextNode(prosopo);
			cell = document.createElement("td");
			cell.appendChild(cellText);
			cell.colSpan = "4";
			cell.align = "center";
			row.appendChild(cell);
			tbody.appendChild(row);

			fillgeni(result[y][prosopo], tbody);
		}
	}
}

function fillOnoma(result, tbody) {
	for (y = 0; y < result.length; y++) {
		fillgeni(result[y], tbody);
	}
}

function fillRhma(result, tbody) {
	for (y = 0; y < result.length; y++) {
		xronoi = Object.keys(result[y]);
		for (x = 0; x < xronoi.length; x++) {
			xronos = xronoi[x];
			row = document.createElement("tr");
			cellText = document.createTextNode(xronos);
			cell = document.createElement("td");
			cell.appendChild(cellText);
			cell.colSpan = "10";
			cell.align = "center";
			cell.style.fontWeight = "bold";
			row.appendChild(cell);
			tbody.appendChild(row);

			fones = Object.keys(result[y][xronos]);
			for (f = 0; f < fones.length; f++) {
				foni = fones[f];
				row = document.createElement("tr");
				cellText = document.createTextNode(foni);
				cell = document.createElement("td");
				cell.appendChild(cellText);
				cell.colSpan = "10";
				cell.align = "center";
				row.appendChild(cell);
				tbody.appendChild(row);

				egliseis = Object.keys(result[y][xronos][foni]);
				for (e = 0; e < egliseis.length; e++) {
					eglisi = egliseis[e];
					row = document.createElement("tr");
					cellText = document.createTextNode(eglisi);
					cell = document.createElement("td");
					cell.style.fontWeight = "bold";
					cell.appendChild(cellText);
					row.appendChild(cell);

					times = result[y][xronos][foni][eglisi];
					for (t = 0; t < times.length; t++) {
						cellText = document.createTextNode(times[t]);
						cell = document.createElement("td");
						cell.appendChild(cellText);
						row.appendChild(cell);
					}

					tbody.appendChild(row);
				}
			}
		}
	}
}

function fillgeni(result, tbody) {
	genoi = Object.keys(result);
	for (g = 0; g < genoi.length; g++) {
		genos = genoi[g];
		row = document.createElement("tr");
		cellText = document.createTextNode(genos);
		cell = document.createElement("td");
		cell.appendChild(cellText);
		cell.colSpan = "4";
		cell.align = "center";
		row.appendChild(cell);
		tbody.appendChild(row);
		el = [ "ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική" ];
		for (z = 0; z < el.length; z++) {
			a1 = result[genos][z];
			a2 = result[genos][z + 5];
			a3 = result[genos][z + 10];

			row = document.createElement("tr");
			cellText = document.createTextNode(el[z]);
			cell = document.createElement("td");
			cell.appendChild(cellText);
			row.appendChild(cell);
			cellText = document.createTextNode(a1);
			cell = document.createElement("td");
			cell.appendChild(cellText);
			row.appendChild(cell);
			cellText = document.createTextNode(a2);
			cell = document.createElement("td");
			cell.appendChild(cellText);
			row.appendChild(cell);
			cellText = document.createTextNode(a3);
			cell = document.createElement("td");
			cell.appendChild(cellText);
			row.appendChild(cell);

			tbody.appendChild(row);
		}
	}
}

function fillTable(result) {
	$("αποτέλεσμα").innerHTML = "";
	// alert(Object.keys(result));
	for (i = 0; i < result.length; i++) {
		tbl = document.createElement("table");
		tbody = document.createElement('tbody');

		row = document.createElement("tr");
		cellText = document.createTextNode(result[i][0]);
		cell = document.createElement("td");
		cell.appendChild(cellText);
		row.appendChild(cell);
		tbody.appendChild(row);

		dial = Object.keys(result[i][1]);
		mtln = Object.keys(result[i][1][dial[0]]);
		for (m = 0; m < mtln.length; m++) {
			mtl = mtln[m];
			row = document.createElement("tr");
			cellText = document.createTextNode(mtl);
			cell = document.createElement("td");
			cell.appendChild(cellText);
			cell.colSpan = "4";
			cell.align = "center";
			row.appendChild(cell);
			tbody.appendChild(row);

			if (mtl == "άρθρο" || mtl == "ουσιαστικό" || mtl == "επίθετο"
					|| mtl == "μετοχή") {
				fillOnoma(result[i][1][dial[0]][mtl], tbody);
			} else if (mtl == "αντωνυμία") {
				fk = Object.keys(result[i][1][dial[0]][mtl][0])[0];
				if (fk == "α" || fk == "β" || fk == "γ") {
					fillProsopo(result[i][1][dial[0]][mtl], tbody);
				} else {
					fillOnoma(result[i][1][dial[0]][mtl], tbody);
				}
			} else if (mtl == "ρήμα") {
				fillRhma(result[i][1][dial[0]][mtl], tbody);
			} else {
				row = document.createElement("tr");
				cellText = document.createTextNode("Άκλητο");
				cell = document.createElement("td");
				cell.appendChild(cellText);
				cell.colSpan = "4";
				cell.align = "center";
				row.appendChild(cell);
				tbody.appendChild(row);
			}

		}
		tbl.appendChild(tbody);
		$("αποτέλεσμα").appendChild(tbl);
	}
}