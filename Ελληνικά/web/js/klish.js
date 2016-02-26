var dialektoi = null;
var metadedomena = {};
var klimakes = {};

var arxika = {};// arxika:lexeis
var katali3is = {}; // dialekto:kathgoria
var tonismoi = {}; // dialekto:kathgoria:tonoi
var katigoriesRhma = {};
var istoria = null;

var tonoi_kathgories = {};
var trexon_kathgories = {};

var epitheta = {};
var ousiastika = {};
var rhmata = {};
var meros = []
var mtl = "ρήμα";

// ΜΟΔΕ
function EN_APXH() {
	nea();
	loadDialektous();
	allagiMTL('ρήμα');
	loadMetaKlima();
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

function allagiMTL(val) {
	meden();
	$(val).style.backgroundColor = "lightgray";
	mtl = val;
	if (val == "ουσιαστικό") {
		$("ε_γένος").show();
		$("γένος").show();
		$("τονισμοί").show();
		$("ονόματα").show();
		$("κΚλίσηΌνομα").show();
		$("κΚλίσηΡήμα").hide();
		$("αυξήσεις").hide();
		$("ενεστωτική").hide();
		$("ε_ενεστωτική").hide();
		$("ρήμα1").hide();
		$("ρήμα2").hide();
		$("ρήμα3").hide();
		$("ρήμα4").hide();
		$("ρήμα5").hide();
		$("ρήμα6").hide();
		$("ρήμα7").hide();
		$("ρήμα8").hide();
	} else if (mtl == "επίθετο") {
		$("αυξήσεις").hide();
		$("ενεστωτική").hide();
		$("ε_ενεστωτική").hide();
		$("ε_γένος").hide();
		$("γένος").hide();
		$("ρήμα1").hide();
		$("ρήμα2").hide();
		$("ρήμα3").hide();
		$("ρήμα4").hide();
		$("ρήμα5").hide();
		$("ρήμα6").hide();
		$("ρήμα7").hide();
		$("ρήμα8").hide();
		$("κΚλίσηΡήμα").hide();

		$("κΚλίσηΌνομα").show();
		$("τονισμοί").show();
		$("ονόματα").show();
	} else if (mtl == "ρήμα") {
		$("αυξήσεις").show();
		$("ενεστωτική").show();
		$("ε_ενεστωτική").show();
		$("ρήμα1").show();
		$("ρήμα2").show();
		$("ρήμα3").show();
		$("ρήμα4").show();
		$("ρήμα5").show();
		$("ρήμα6").show();
		$("ρήμα7").show();
		$("ρήμα8").show();
		$("κΚλίσηΌνομα").hide();
		$("κΚλίσηΡήμα").show();
		$("ονόματα").hide();
	}
	loadMTL();
}

function meden() {
	$("ουσιαστικό").style.backgroundColor = "";
	$('επίθετο').style.backgroundColor = "";
	$('ρήμα').style.backgroundColor = "";
}

function loadMTL() {
	request = "dump/" + mtl;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			// alert(transport.responseText);
			var result = eval(transport.responseText);
			// var result = transport.responseText.evalJSON(true);
			removeOptionsAlternate($("κκατηγορίες"));
			meros = result[0];

			if (mtl == "ρήμα") {
				katali3is = result[1];
				tonoi_kathgories = result[2];
			} else {
				katali3is = result[1];
				tonismoi = result[2];
				tonoi_kathgories = result[3];
			}
			updateKatalhjeis();
		},
		onFailure : function() {
			alert('Something went wrong in loadMTL.');
		}
	});
}

function updateKatalhjeis() {
	var dialektos = $F("διάλεκτος");
	removeOptionsAlternate($("αρχικά"));
	removeOptionsAlternate($("λέξεις"));
	if (dialektos in dialektoi) {
		var counter = 0;
		keys = Object.keys(meros[dialektos]);
		keys.sort();
		for (d = 0; d < keys.length; d++) {
			$("αρχικά")[counter] = new Option(keys[d]);
			counter += 1;
		}
		if (dialektoi[dialektos]["εικονική"].length > 0) {
			dialektos = dialektoi[dialektos]["εικονική"];
		}
		var keys = [];
		keys = katali3is[dialektos];// Object.keys(tonoi_kathgories[dialektos]);
		if (mtl == "επίθετο") {
			keys = Object.keys(tonoi_kathgories[dialektos]);
			keys.sort();
		}
		if (mtl == "ρήμα") {
			keys = Object.keys(tonoi_kathgories[dialektos]);
			keys.sort();
			for (d = 0; d < keys.length; d++) {
				$("καταλήξεις_ρημάτων")[d] = new Option(keys[d]);
			}
			if ("ρήμα" in katali3is[dialektos]) {
				kat = katali3is[dialektos]["ρήμα"];
				removeOptionsAlternate($("ρενεστώτας"));
				removeOptionsAlternate($("ρπαρατατικός"));
				removeOptionsAlternate($("ραόριστος"));
				removeOptionsAlternate($("ρπαρακείμενος"));
				removeOptionsAlternate($("ρυπερσυντέλικος"));
				removeOptionsAlternate($("ρμέλλοντας"));
				removeOptionsAlternate($("ρσμέλλοντας"));
				$("ρενεστώτας")[0] = new Option(0);
				$("ρπαρατατικός")[0] = new Option(0);
				$("ραόριστος")[0] = new Option(0);
				$("ρπαρακείμενος")[0] = new Option(0);
				$("ρυπερσυντέλικος")[0] = new Option(0);
				$("ρμέλλοντας")[0] = new Option(0);
				$("ρσμέλλοντας")[0] = new Option(0);
				if ("ενεστώτας" in kat) {
					for (d = 0; d < kat["ενεστώτας"].length; d++) {
						$("ρενεστώτας")[d] = new Option(kat["ενεστώτας"][d]);
					}
				}
				if ("παρατατικός" in kat) {
					for (d = 0; d < kat["παρατατικός"].length; d++) {
						$("ρπαρατατικός")[d] = new Option(kat["παρατατικός"][d]);
					}
				}
				if ("αόριστος" in kat) {
					for (d = 0; d < kat["αόριστος"].length; d++) {
						$("ραόριστος")[d] = new Option(kat["αόριστος"][d]);
					}
				}
				if ("παρακείμενος" in kat) {
					for (d = 0; d < kat["παρακείμενος"].length; d++) {
						$("ρπαρακείμενος")[d] = new Option(
								kat["παρακείμενος"][d]);
					}
				}
				if ("υπερσυντέλικος" in kat) {
					for (d = 0; d < kat["υπερσυντέλικος"].length; d++) {
						$("ρυπερσυντέλικος")[d] = new Option(
								kat["υπερσυντέλικος"][d]);
					}
				}
				if ("μέλλοντας" in kat) {
					for (d = 0; d < kat["μέλλοντας"].length; d++) {
						$("ρμέλλοντας")[d] = new Option(kat["μέλλοντας"][d]);
					}
				}
				if ("συντελεσμένος μέλλοντας" in kat) {
					for (d = 0; d < kat["συντελεσμένος μέλλοντας"].length; d++) {
						$("ρσμέλλοντας")[d] = new Option(
								kat["συντελεσμένος μέλλοντας"][d]);
					}
				}
			}
			if ("μετοχή" in katali3is[dialektos]) {
				kat = katali3is[dialektos]["μετοχή"];
				removeOptionsAlternate($("μενεστώτας"));
				removeOptionsAlternate($("μαόριστος"));
				removeOptionsAlternate($("μπαρακείμενος"));
				removeOptionsAlternate($("μμέλλοντας"));
				removeOptionsAlternate($("μσμέλλοντας"));
				$("μενεστώτας")[0] = new Option(0);
				$("μαόριστος")[0] = new Option(0);
				$("μπαρακείμενος")[0] = new Option(0);
				$("μμέλλοντας")[0] = new Option(0);
				$("μσμέλλοντας")[0] = new Option(0);
				if ("ενεστώτας" in kat) {
					for (d = 0; d < kat["ενεστώτας"].length; d++) {
						$("μενεστώτας")[d] = new Option(kat["ενεστώτας"][d]);
					}
				}
				if ("αόριστος" in kat) {
					for (d = 0; d < kat["αόριστος"].length; d++) {
						$("μαόριστος")[d] = new Option(kat["αόριστος"][d]);
					}
				}
				if ("παρακείμενος" in kat) {
					for (d = 0; d < kat["παρακείμενος"].length; d++) {
						$("μπαρακείμενος")[d] = new Option(
								kat["παρακείμενος"][d]);
					}
				}
				if ("μέλλοντας" in kat) {
					for (d = 0; d < kat["μέλλοντας"].length; d++) {
						$("μμέλλοντας")[d] = new Option(kat["μέλλοντας"][d]);
					}
				}
				if ("συντελεσμένος μέλλοντας" in kat) {
					for (d = 0; d < kat["συντελεσμένος μέλλοντας"].length; d++) {
						$("μσμέλλοντας")[d] = new Option(
								kat["συντελεσμένος μέλλοντας"][d]);
					}
				}
			}
		} else {
			for (d = 0; d < keys.length; d++) {
				txt = keys[d]+"";
				if (txt.search(" ")!=-1) {
					txt = keys[d].replace(" ","");
					txt = txt.replace(" ","");
					txt = txt.replace(" ","");} else {
						txt = keys[d];
					}
				$("καταλήξεις")[d] = new Option(txt);
			}
		}
	}
}

function tonoiKathgorias() {
	dial = $F("διάλεκτος");
	τόνοι = [ "ετονισμόςα", "ετονισμόςθ", "ετονισμόςο", "μτονισμόςα",
			"μτονισμόςθ", "μτονισμόςο", "πτονισμόςα", "πτονισμόςθ",
			"πτονισμόςο" ];
	alert(dialektoi[dial]["εικονική"]);
	for (t = 0; t < 9; t++) {
		τόνος = τόνοι[t];
		removeOptionsAlternate($(τόνος));

		$(τόνος)[0] = new Option("Τονισμός");
		for (n = 0; n < tonoi_kathgories[dial]; n++) {
			$(τόνος)[n + 1] = new Option(n);
		}
	}
}

function epilogiKathgorias() {
	parts = $F("κκατηγορίες").split(": ");
	dialekt = parts[0];
	parts = parts[1].split("_");
	kat = parts[0];
	xro = parts[1].split(" (")[0];
	message = Object.toJSON({
		"διάλεκτος" : dialekt,
		"κατηγορία" : kat,
		"χρόνος" : xro,
		"μέρος του λόγου" : "μετοχή"
	});
	request = "develop/κατηγορία/" + message;
	var xmlhttp = new Ajax.Request(
			request,
			{
				method : 'post',
				onSuccess : function(transport) {
					var result = eval(transport.responseText);
					// var result = transport.responseText.evalJSON(true);
					trexon_kathgories = result;
					selectValue("διάλεκτος", result[0]["διάλεκτος"]);
					selectValue("χρόνος", result[0]["χρόνος"]);
					τόνοι = [ "ετονισμόςα", "ετονισμόςθ", "ετονισμόςο",
							"μτονισμόςα", "μτονισμόςθ", "μτονισμόςο",
							"πτονισμόςα", "πτονισμόςθ", "πτονισμόςο" ];
					for (t = 0; t < 9; t++) {
						selectValue(τόνοι[t], result[0]["τονισμοί"][t]);
					}
					tmhmata = [ "Ενεργητική_αρσενικό", "Ενεργητική_θηλυκό",
							"Ενεργητική_ουδέτερο", "Μέση_αρσενικό",
							"Μέση_θηλυκό", "Μέση_ουδέτερο",
							"Παθητική_αρσενικό", "Παθητική_θηλυκό",
							"Παθητική_ουδέτερο", ];
					for (t = 0; t < 9; t++) {
						nodes = $(tmhmata[t]).childNodes;
						tdn = 0;
						for (n = 0; n < nodes.length; n++) {
							if (nodes[n].nodeName == "TD") {
								if (tdn != 0 && tdn != 17
										&& nodes[n].hasChildNodes()) {
									nodes2 = nodes[n].childNodes;
									for (n2 = 0; n2 < nodes2.length; n2++) {
										if (nodes2[n2].nodeName == "INPUT") {
											if (result[0]["καταλήξεις"][t].length > (tdn - 1)) {
												nodes2[n2].value = result[0]["καταλήξεις"][t][tdn - 1];
											} else {
												nodes2[n2].value = "";
											}
										}
									}
								}
								tdn += 1;
							}
						}
					}
				},
				onFailure : function() {
					alert('Something went wrong in kathgories.');
				}
			});
}

function nea_kathgoria() {
	$("κκατηγορίες").selectedIndex = -1;

	$("δκείμενο").value = "";
	τόνοι = [ "ετονισμόςα", "ετονισμόςθ", "ετονισμόςο", "μτονισμόςα",
			"μτονισμόςθ", "μτονισμόςο", "πτονισμόςα", "πτονισμόςθ",
			"πτονισμόςο" ];
	tmhmata = [ "Ενεργητική_αρσενικό", "Ενεργητική_θηλυκό",
			"Ενεργητική_ουδέτερο", "Μέση_αρσενικό", "Μέση_θηλυκό",
			"Μέση_ουδέτερο", "Παθητική_αρσενικό", "Παθητική_θηλυκό",
			"Παθητική_ουδέτερο", ];
	for (t = 0; t < 9; t++) {
		selectValue(τόνοι[t], [ "Τονισμός" ]);
		nodes = $(tmhmata[t]).childNodes;
		tdn = 0;
		for (n = 0; n < nodes.length; n++) {
			if (nodes[n].nodeName == "TD") {
				if (tdn != 0 && tdn != 17 && nodes[n].hasChildNodes()) {
					nodes2 = nodes[n].childNodes;
					for (n2 = 0; n2 < nodes2.length; n2++) {
						if (nodes2[n2].nodeName == "INPUT") {
							nodes2[n2].value = "";
						}
					}
				}
				tdn += 1;
			}
		}
	}
}

function dedomenaKathgorias() {
	message = {
		"διάλεκτος" : $F("διάλεκτος"),
		"θέμα" : $F("δκείμενο"),
		"χρόνος" : $F("χρόνος"),
		"μέρος του λόγου" : "μετοχή",
		"τονισμοί" : [],
		"καταλήξεις" : []
	};
	τόνοι = [ "ετονισμόςα", "ετονισμόςθ", "ετονισμόςο", "μτονισμόςα",
			"μτονισμόςθ", "μτονισμόςο", "πτονισμόςα", "πτονισμόςθ",
			"πτονισμόςο" ];
	tmhmata = [ "Ενεργητική_αρσενικό", "Ενεργητική_θηλυκό",
			"Ενεργητική_ουδέτερο", "Μέση_αρσενικό", "Μέση_θηλυκό",
			"Μέση_ουδέτερο", "Παθητική_αρσενικό", "Παθητική_θηλυκό",
			"Παθητική_ουδέτερο", ];
	for (t = 0; t < 9; t++) {
		timh = $F(τόνοι[t]);
		if (timh == "Τονισμός") {
			timh = 0;
		}
		message["τονισμοί"].push(parseInt(timh));
		nodes = $(tmhmata[t]).childNodes;
		tdn = 0;
		katal = [];
		for (n = 0; n < nodes.length; n++) {
			if (nodes[n].nodeName == "TD") {
				if (tdn != 0 && tdn != 17 && nodes[n].hasChildNodes()) {
					nodes2 = nodes[n].childNodes;
					for (n2 = 0; n2 < nodes2.length; n2++) {
						if (nodes2[n2].nodeName == "INPUT") {
							if (nodes2[n2].value.length > 0) {
								katal.push(nodes2[n2].value.split(", "));
							} else {
								katal.push([]);
							}
						}
					}
				}
				tdn += 1;
			}
		}
		message["καταλήξεις"].push(katal);
	}
	return message
}

function dokimh() {
	message = Object.toJSON(dedomenaKathgorias());
	request = "develop/δοκιμή/" + message;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var mresult = eval(transport.responseText);
			// var result = transport.responseText.evalJSON(true);
			showRhma({}, mresult[0])
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function apoKathgoria() {
	message = dedomenaKathgorias();
	if ($("κκατηγορίες").selectedIndex != -1) {
		parts = $F("κκατηγορίες").split(": ");
		dialekt = parts[0];
		parts = parts[1].split("_");
		kat = parts[0];
		xro = parts[1].split(" (")[0];

		message["διάλεκτος"] = dialekt;
		message["χρόνος"] = xro;
		message["κατηγορία"] = kat;
	}
	message = Object.toJSON(dedomenaKathgorias());
	request = "develop/αποθήκευση_κατηγορίας/" + message;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Αποθηκεύτικε!");
			}
			loadKathgories();
			allagiMTL();
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function diaKathgoria() {
	parts = $F("κκατηγορίες").split(": ");
	dialekt = parts[0];
	parts = parts[1].split("_");
	kat = parts[0];
	xro = parts[1].split(" (")[0];
	message = Object.toJSON({
		"διάλεκτος" : dialekt,
		"ΑΑ" : parseInt(kat),
		"χρόνος" : xro,
		"μέρος του λόγου" : "μετοχή"
	});
	request = "develop/διαγραφή_κατηγορίας/" + message;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Διαγράφηκε!");
			}
			loadKathgories();
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

// ΜΕΤΑΔΕΔΟΜΕΝΑ - ΚΛΙΜΑΚΕΣ
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
			alert('Something went wrong in loadMetaKlima.');
		}
	});
}

function επιλογή_μκ() {
	var index = $("μετα_κλίμακες").selectedIndex;
	if (index > -1) {
		parts = $("μετα_κλίμακες")[index].value.split(": ");
		if (parts[0] == "Κλίμακες") {
			$("μετα_κλίμα").selectedIndex = 1;
		} else {
			$("μετα_κλίμα").selectedIndex = 0;
		}
		$("μκόνομα").value = parts[1];
		$("μκτιμή").value = parts[2];
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

function trexon() {
	index = $("ιστορία").selectedIndex;
	if (index != -1) {
		message = istoria[index];
		request = "develop/τρέχον_λημμάτων/" + Object.toJSON(message);
		var xmlhttp = new Ajax.Request(request, {
			method : 'post',
			onSuccess : function(transport) {
				nea();
				allagiMTL(mtl);
			},
			onFailure : function() {
				alert('Something went wrong in trexon.');
			}
		});
	}
}

function updateLexeis() {
	removeOptionsAlternate($("αρχικά"));
	removeOptionsAlternate($("λέξεις"));

	var meros = [];
	if ($F("τύπος") == "ουσιαστικό") {
		meros = ousiastika;
	} else if ($F("τύπος") == "επίθετο") {
		meros = epitheta;
	} else if ($F("τύπος") == "ρήμα") {
		meros = rhmata;
	}
	if (dialektos in meros) {
		arxika = {};
		for (a = 0; a < meros[dialektos].length; a++) {
			typos = meros[dialektos][a];
			if (typos[0] in arxika) {
				arxika[typos[0]].push(typos);
			} else {
				arxika[typos[0]] = [ typos ]
			}
		}
		arxk = Object.keys(arxika);
		arxk.sort();
		for (a = 0; a < arxk.length; a++) {
			$("αρχικά")[a] = new Option(arxk[a]);
		}
	}
}

function fillLexeis() {
	removeOptionsAlternate($("λέξεις"));
	arxiko = $F("αρχικά");
	dialektos = $F("διάλεκτος");
	lexeis = Object.keys(meros[dialektos][arxiko]);
	lexeis.sort();
	for (a = 0; a < lexeis.length; a++) {
		$("λέξεις")[a] = new Option(lexeis[a]);
		$("λέξεις")[a].value = meros[dialektos][arxiko][lexeis[a]];
	}
}

function updateKatigories() {
	removeOptionsAlternate($("καταλήξεις"));
	removeOptionsAlternate($("τονισμοί"));
	$("καταλήξεις")[0] = new Option("καταλήξεις");
	if (dialektoi[dialektos]["εικονική"].length > 0) {
		dialektos = dialektoi[dialektos]["εικονική"];
	}
	if ($F("τύπος") == "ουσιαστικό" || $F("τύπος") == "επίθετο") {
		for (k = 0; k < katali3is[dialektos].length; k++) {
			txt = katali3is[dialektos][k].replace(" ","");
			txt = txt.replace(" ","");
			txt = txt.replace(" ","");
			$("καταλήξεις")[k + 1] = new Option(txt);
		}
	}
}

function updateTonous() {
	removeOptionsAlternate($("τονισμοί"));
	var dialektos = $F("διάλεκτος")
	if (dialektoi[dialektos]["εικονική"].length > 0) {
		dialektos = dialektoi[dialektos]["εικονική"];
	}
	if (mtl == "ουσιαστικό" || mtl == "επίθετο") {
		if ($F("όλα") == null) {
			ton = tonoi_kathgories[dialektos];
			value = $F("καταλήξεις");
			tonKeys = Object.keys(ton);
			for(tk=0;tk<tonKeys.length;tk++) {
				thekey = tonKeys[tk].replace(" ","");
				thekey = thekey.replace(" ","");
				thekey = thekey.replace(" ","");
				if (thekey!=value) {continue;}
				ton_value = ton[tonKeys[tk]];
				for (t = 0; t < ton_value.length; t++) {
					$("τονισμοί")[t] = new Option(ton_value[t]);
				}
				break;
			}
		} else {
			ton = tonismoi[dialektos];
			var counter = 0;
			for (t = 0; t < ton.length; t++) {
				$("τονισμοί")[counter] = new Option(ton[t]);
				counter += 1;
			}
		}
	}
}

// ΛΕΞΕΙΣ
function nea() {
	istoria = null;
	removeOptionsAlternate($("ιστορία"));
	$("συνθετικό").value = "";
	$("λήμμα").value = "";
	$("αύξηση").value = "";
	$("παρακείμενου").value = "";
	$("ενεστωτική").value = "";

	$("μκόνομα").value = "";
	$("μκτιμή").value = "";
	$("ἐτικέτες").value = "τρέχον, ";
	$("Παρατηρήσεις").value = "";
	removeOptionsAlternate($("μετα_κλίμακες"));
	$("αποτελέσματα").innerHTML = "";
}

function istoriko() {
	timh = $F("λέξεις");
	while ($("ιστορία").length > 0) {
		$("ιστορία").remove(0);
	}
	message = Object.toJSON({
		"μέρος του λόγου" : mtl,
		"θέση" : timh
	});
	request = "develop/ιστορικό_λημμάτων/" + message;
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			istoria = result;
			var counter = 0;
			for (k = 0; k < istoria.length; k++) {
				b = istoria[k]["Ἡμερομηνία"] + ' ' + istoria[k]["ἐτικέτες"];
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
			alert('Something went wrong in istoriko.');
		}
	});
}

function epilogiIstorias() {
	if ($("ιστορία").selectedIndex != -1) {
		ist = istoria[$("ιστορία").selectedIndex];
		$("συνθετικό").value = ist["συνθετικό"];
		$("λήμμα").value = ist["λήμμα"];
		$("ἐτικέτες").value = ist["ἐτικέτες"];
		$("Παρατηρήσεις").value = ist["Παρατηρήσεις"];
		changeMeta();

		if (mtl == "ουσιαστικό") {
			selectValue("γένος", ist["γένος"]);
			selectValue("καταλήξεις", ist["κατηγορία"]);
			selectValue("τονισμοί", ist["τονισμός"]);
			updateTonous();
			kline();
		} else if (mtl == "επίθετο") {
			selectValue("καταλήξεις", Object.toJSON(ist["κατηγορίες"]));
			updateTonous();
			kline();
		} else if (mtl == "ρήμα") {
			$("αύξηση").value = ist["αύξηση"];
			$("ενεστωτική").value = ist["ενεστωτική αύξηση"];
			$("παρακείμενου").value = ist["αύξηση παρακείμενου"];

			selectValue("καταλήξεις_ρημάτων", "[" + ist["ρήμα"] + ", "
					+ ist["μετοχή"] + "]");
			xronoiRhma();
			klineRhma();
		}
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

function anagnorish() {
	met = [ "μενεστώτας", "μαόριστος", "μπαρακείμενος", "μμέλλοντας",
			"μσμέλλοντας" ];
	for (zx = 0; zx < 5; zx++) {
		met[zx].selectedIndex = 0;
	}
	var synolo = {
		"διάλεκτος" : dialektos,
		"μέρος του λόγου" : $F("τύπος"),
		"λέξη" : $F("λέξεις")
	};
	request = "develop/αναγνώριση/" + Object.toJSON(synolo);
	var xmlhttp = new Ajax.Request(
			request,
			{
				method : 'post',
				onSuccess : function(transport) {
					var result = eval(transport.responseText);
					// var result = transport.responseText.evalJSON(true);
					nea(false);
					for (r = 0; r < result.length; r++) {
						if ($F("τύπος") == "ουσιαστικό") {
							gen = {
								"αρσενικό" : 0,
								"θηλυκό" : 1,
								"ουδέτερο" : 2
							};
							$("γένος").selectedIndex = gen[result[r]["γένος"]];
							fillOusiastiko(result[r]["κλίσεις"]);
						} else if ($F("τύπος") == "επίθετο") {
							fillEpitheto(result[r]["κλίσεις"]);
						} else if ($F("τύπος") == "ρήμα") {
							showRhma(result[r]['κλίσεις ρήμα'],
									result[r]['κλίσεις μετοχή']);
						}

						if ("λήμμα" in result[r]) {
							$("λήμμα").value = result[r]["λήμμα"];
						}
						if ("θέμα" in result[r]) {
							$("λήμμα").value = result[r]["θέμα"];
						}
						if ("αύξηση" in result[r]) {
							$("αύξηση").value = result[r]["αύξηση"];
						}
						if ("ενεστωτική αύξηση" in result[r]) {
							$("ενεστωτική").value = result[r]["ενεστωτική αύξηση"];
						}

						if ("αύξηση παρακείμενου" in result[r]) {
							$("παρακείμενου").value = result[r]["αύξηση παρακείμενου"];
						}
						$("συνθετικό").value = "";
						if ("συνθετικό" in result[r]
								&& result[r]["συνθετικό"].length > 0) {
							$("συνθετικό").value = result[r]["συνθετικό"];
						}

						$("καταλήξεις").selectedIndex = 0;
						if ("κατηγορία" in result[r]) {
							for (ka = 0; ka < $("καταλήξεις").length; ka++) {
								if ($("καταλήξεις")[ka].value == result[r]["κατηγορία"]) {
									$("καταλήξεις").selectedIndex = ka;
									ka = $("καταλήξεις").length;
								}
							}
						} else if ("κατηγορίες" in result[r]) {
							for (k = 0; k < $("καταλήξεις").length; k++) {
								if ($("καταλήξεις")[k].value == result[r]["κατηγορίες"]) {
									$("καταλήξεις").selectedIndex = k;
									k = $("καταλήξεις").length;
								}
							}
						}

						if ($F("τύπος") == "ουσιαστικό"
								|| $F("τύπος") == "επίθετο") {
							updateTonous();
							$("τονισμοί").selectedIndex = 0;
							if ("τονισμός" in result[r]) {
								for (ka = 0; ka < $("τονισμοί").length; ka++) {
									if ($("τονισμοί")[ka].value == result[r]["τονισμός"]) {
										$("τονισμοί").selectedIndex = ka;
										ka = $("τονισμοί").length;
									}
								}
							} else if ("τονισμοί" in result[r]) {
								for (k = 0; k < $("τονισμοί").length; k++) {
									if ($("τονισμοί")[k].value == result[r]["τονισμοί"]) {
										$("τονισμοί").selectedIndex = k;
									}
								}
							}
						}

						if ("ρήμα_μετοχή" in result[r]) {
							selectValue("καταλήξεις_ρημάτων",
									result[r]["ρήμα_μετοχή"]);
							xronoiRhma();
						}

						if ("μεταδεδομένα" in result[r]) {
							ks = Object.keys(result[r]["μεταδεδομένα"]);
							for (k = 0; k < ks.length; k++) {
								$("μετα_κλίμακες")[k] = new Option(
										"μεταδεδομένα: "
												+ ks[k]
												+ ": "
												+ result[r]["μεταδεδομένα"][ks[k]]);
							}
						}
						if ("κλίμακες" in result[r]) {
							ks = Object.keys(result[r]["κλίμακες"]);
							for (k = 0; k < ks.length; k++) {
								$("μετα_κλίμακες")[k] = new Option("κλίμακες: "
										+ ks[k] + ": "
										+ result[r]["κλίμακες"][ks[k]]);
							}
						}
					}
				},
				onFailure : function() {
					alert('Something went wrong in kathgories.');
				}
			});
}

function kline() {
	if ($F("καταλήξεις") == "καταλήξεις" || $F("καταλήξεις") == "") {
		return;
	}
	if ($F("τονισμοί") == "τονισμοί") {
		return;
	}
	var kline_d = {
		"συνθετικό" : $F("συνθετικό"),
		"λήμμα" : $F("λήμμα"),
		"μέρος του λόγου" : mtl,
		"διάλεκτος" : $F("διάλεκτος")
	}

	if (mtl == "ουσιαστικό") {
		kline_d["κατηγορία"] = parseInt($F("καταλήξεις"));
		kline_d["τονισμός"] = parseInt($F("τονισμοί"));
		kline_d["γένος"] = $F("γένος");
	} else if (mtl == "επίθετο") {
		kline_d["κατηγορίες"] = eval($F("καταλήξεις"));
		kline_d["τονισμοί"] = eval($F("τονισμοί"));
	}
	request = "develop/κλίνε/" + Object.toJSON(kline_d);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			// var result = transport.responseText.evalJSON(true);
			if (mtl == "ουσιαστικό") {
				fillOusiastiko(result[0]);
			} else {
				fillEpitheto(result[0]);
			}
		},
		onFailure : function() {
			alert('Something went wrong in kline.');
		}
	});
}

function apothikeusi() {
	var kline_d = {
		"συνθετικό" : $F("συνθετικό"),
		"λήμμα" : $F("λήμμα"),
		"μέρος του λόγου" : mtl,
		"διάλεκτος" : $F("διάλεκτος"),
		"Μεταδεδομένα" : {},
		"Κλίμακες" : {},
		"ἐτικέτες" : $F("ἐτικέτες"),
		"Παρατηρήσεις" : $F("Παρατηρήσεις")
	};
	// if ($("λέξεις").selectedIndex != -1) {
	// lexi = $("λέξεις")[$("λέξεις").selectedIndex].value;
	// var r = confirm("Αλλαγή της λέξεως " + lexi + ";");
	// if (r == false) {
	// return;
	// }
	// kline_d["αρχικό"] = lexi;
	// }
	if (mtl == "ουσιαστικό") {
		kline_d["κατηγορία"] = parseInt($F("καταλήξεις"));
		kline_d["τονισμός"] = parseInt($F("τονισμοί"));
		kline_d["γένος"] = $F("γένος");

	} else if (mtl == "επίθετο") {
		kline_d["κατηγορίες"] = eval($F("καταλήξεις"));
		kline_d["τονισμοί"] = eval($F("τονισμοί"));
	} else if (mtl == "ρήμα") {
		kline_d["θέμα"] = $F("λήμμα");
		kline_d["αύξηση παρακείμενου"] = $F("παρακείμενου");
		kline_d["αύξηση"] = $F("αύξηση");
		kline_d["ενεστωτική αύξηση"] = $F("ενεστωτική");
		kline_d["ρήμα"] = {
			"ενεστώτας" : parseInt($F("ρενεστώτας")),
			"παρατατικός" : parseInt($F("ρπαρατατικός")),
			"αόριστος" : parseInt($F("ραόριστος")),
			"παρακείμενος" : parseInt($F("ρπαρακείμενος")),
			"υπερσυντέλικος" : parseInt($F("ρυπερσυντέλικος")),
			"μέλλοντας" : parseInt($F("ρμέλλοντας")),
			"συντελεσμένος μέλλοντας" : parseInt($F("ρσμέλλοντας"))
		}
		kline_d["μετοχή"] = {
			"ενεστώτας" : parseInt($F("μενεστώτας")),
			"παρατατικός" : 0,
			"αόριστος" : parseInt($F("μαόριστος")),
			"παρακείμενος" : parseInt($F("μπαρακείμενος")),
			"υπερσυντέλικος" : 0,
			"μέλλοντας" : parseInt($F("μμέλλοντας")),
			"συντελεσμένος μέλλοντας" : parseInt($F("μσμέλλοντας"))
		}
	}
	index = $("ιστορία").selectedIndex;
	if (index != -1) {
		kline_d["ΑΑ"] = istoria[index]["ΑΑ"];
	}
	for (m = 0; m < $("μετα_κλίμα").length; m++) {
		parts = $("μετα_κλίμα")[m].value.split(": ");
		if (parts.length == 3) {
			key = parts[1];
			val = parts[2].split(", ");
			if (parts[0] == "Μεταδεδομένα") {
				kline_d["Μεταδεδομένα"][key] = val;
			} else {
				kline_d["Κλίμακες"][key] = eval(val);
			}
		}
	}
	alert(Object.toJSON(kline_d));
	// return;
	request = "develop/αποθήκευση_λημμάτων/" + Object.toJSON(kline_d);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Αποθηκεύτικε!");
			}
			loadOnomata();
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function diagrafh() {
	index = $("ιστορία").selectedIndex;
	if (index != -1) {
		kline_d = istoria[index];
		request = "develop/διαγραφή_λημμάτων/" + Object.toJSON(kline_d);
		var xmlhttp = new Ajax.Request(request, {
			method : 'post',
			onSuccess : function(transport) {
				if (transport.responseText == "OK") {
					alert("Διαγράφηκε!");
					nea();
				}
				allagiMTL(mtl);
			},
			onFailure : function() {
				alert('Something went wrong in kathgories.');
			}
		});
	}
}

function klineRhma() {
	// if ($F("καταλήξεις")=="καταλήξεις" || $F("καταλήξεις")=="")
	var kline_d = {
		"συνθετικό" : $F("συνθετικό"),
		"λήμμα" : $F("λήμμα"),
		"αύξηση παρακείμενου" : $F("παρακείμενου"),
		"αύξηση" : $F("αύξηση"),
		"ενεστωτική αύξηση" : $F("ενεστωτική"),
		"μέρος του λόγου" : mtl,
		"ρήμα" : {
			"ενεστώτας" : parseInt($F("ρενεστώτας")),
			"παρατατικός" : parseInt($F("ρπαρατατικός")),
			"αόριστος" : parseInt($F("ραόριστος")),
			"παρακείμενος" : parseInt($F("ρπαρακείμενος")),
			"υπερσυντέλικος" : parseInt($F("ρυπερσυντέλικος")),
			"μέλλοντας" : parseInt($F("ρμέλλοντας")),
			"συντελεσμένος μέλλοντας" : parseInt($F("ρσμέλλοντας"))
		},
		"μετοχή" : {
			"ενεστώτας" : parseInt($F("μενεστώτας")),
			"αόριστος" : parseInt($F("μαόριστος")),
			"παρακείμενος" : parseInt($F("μπαρακείμενος")),
			"μέλλοντας" : parseInt($F("μμέλλοντας")),
			"συντελεσμένος μέλλοντας" : parseInt($F("μσμέλλοντας"))
		},
		"διάλεκτος" : $F("διάλεκτος")
	}
	request = "develop/κλίνε/" + Object.toJSON(kline_d);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			// var result = transport.responseText.evalJSON(true);
			for (r = 0; r < result.length; r++) {
				showRhma(result[0], result[1]);
			}
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function xronoiRhma() {
	if ($("καταλήξεις_ρημάτων").selectedIndex != -1) {
		times = tonoi_kathgories[$F("διάλεκτος")][$F("καταλήξεις_ρημάτων")];
		r = times["ρήμα"];
		m = times["μετοχή"];

		if (r) {
			if ("ενεστώτας" in r) {
				selectValue("ρενεστώτας", r["ενεστώτας"]["ΑΑ"]);
			} else {
				selectValue("ρενεστώτας", 0);
			}
			if ("παρατατικός" in r) {
				selectValue("ρπαρατατικός", r["παρατατικός"]["ΑΑ"]);
			} else {
				selectValue("ρπαρατατικός", 0);
			}
			if ("αόριστος" in r) {
				selectValue("ραόριστος", r["αόριστος"]["ΑΑ"]);
			} else {
				selectValue("ραόριστος", 0);
			}
			if ("παρακείμενος" in r) {
				selectValue("ρπαρακείμενος", r["παρακείμενος"]["ΑΑ"]);
			} else {
				selectValue("ρπαρακείμενος", 0);
			}
			if ("υπερσυντέλικος" in r) {
				selectValue("ρυπερσυντέλικος", r["υπερσυντέλικος"]["ΑΑ"]);
			} else {
				selectValue("ρυπερσυντέλικος", 0);
			}
			if ("μέλλοντας" in r) {
				selectValue("ρμέλλοντας", r["μέλλοντας"]["ΑΑ"]);
			} else {
				selectValue("ρμέλλοντας", 0);
			}
			if ("συντελεσμένος μέλλοντας" in r) {
				selectValue("ρσμέλλοντας", r["συντελεσμένος μέλλοντας"]["ΑΑ"]);
			} else {
				selectValue("ρσμέλλοντας", 0);
			}
		}
		if (m) {
			if ("ενεστώτας" in m) {
				selectValue("μενεστώτας", m["ενεστώτας"]["ΑΑ"]);
			} else {
				selectValue("μενεστώτας", 0);
			}
			if ("αόριστος" in m) {
				selectValue("μαόριστος", m["αόριστος"]["ΑΑ"]);
			} else {
				selectValue("μαόριστος", 0);
			}
			if ("παρακείμενος" in m) {
				selectValue("μπαρακείμενος", m["παρακείμενος"]["ΑΑ"]);
			} else {
				selectValue("μπαρακείμενος", 0);
			}
			if ("μέλλοντας" in m) {
				selectValue("μμέλλοντας", m["μέλλοντας"]["ΑΑ"]);
			} else {
				selectValue("μμέλλοντας", 0);
			}
			if ("συντελεσμένος μέλλοντας" in m) {
				selectValue("μσμέλλοντας", m["συντελεσμένος μέλλοντας"]["ΑΑ"]);
			} else {
				selectValue("μσμέλλοντας", 0);
			}
		}
	}
}

function showRhma(result, mresult) {
	$("αποτελέσματα").innerHTML = "";
	table = document.createElement("table");
	tbody = document.createElement("tbody");
	xronoi = [ "ενεστώτας", "παρατατικός", "αόριστος", "παρακείμενος",
			"υπερσυντέλικος", "μέλλοντας", "συντελεσμένος μέλλοντας" ];
	for (x = 0; x < xronoi.length; x++) {
		xronos = xronoi[x];
		if (xronos in result || xronos in mresult) {
			tr = document.createElement("tr");
			th = document.createElement("th");
			text = document.createTextNode(xronos);
			h4 = document.createElement("h4");
			h4.style.textAlign = "center";
			h4.appendChild(text);
			th.appendChild(h4);
			th.colSpan = 16;
			th.style.backgroundColor = "lightgrey";
			tr.appendChild(th);
			tbody.appendChild(tr);

			fones = [ "ενεργητική", "μέση", "παθητική" ];
			for (f = 0; f < fones.length; f++) {
				foni = fones[f];
				if ((xronos in result && foni in result[xronos])
						|| (xronos in mresult && foni in mresult[xronos])) {
					tr = document.createElement("tr");
					th = document.createElement("th");
					text = document.createTextNode(foni);
					h5 = document.createElement("h5");
					h5.style.textAlign = "center";
					h5.appendChild(text);
					th.appendChild(h5);
					th.colSpan = 16;
					tr.appendChild(th);
					tbody.appendChild(tr);
				}

				if (xronos in result && foni in result[xronos]) {
					egliseis = [ "οριστική", "υποτακτική", "ευκτική",
							"προστακτική", "απαρέμφατο" ];
					for (e = 0; e < egliseis.length; e++) {
						eglish = egliseis[e];
						if (eglish in result[xronos][foni]) {
							tr = document.createElement("tr");
							th = document.createElement("th");
							text = document.createTextNode(eglish);
							th.appendChild(text);
							tr.appendChild(th);
							tr.appendChild(document.createElement("td"));
							klimena = result[xronos][foni][eglish];
							for (k = 0; k < klimena.length; k++) {
								if (k / 3 == 1 || k / 3 == 2) {
									tr
											.appendChild(document
													.createElement("td"));
									tr
											.appendChild(document
													.createElement("td"));
								}
								td = document.createElement("td");
								text = document.createTextNode(klimena[k]);
								td.appendChild(text);
								if (parseInt(k / 3) == 1) {
									td.style.backgroundColor = "lightgray";
								}
								tr.appendChild(td);

							}
							tbody.appendChild(tr);
						}
					}
				}

				if (xronos in mresult && foni in mresult[xronos]) {
					gen2 = [ "αρσενικό", "θηλυκό", "ουδέτερο" ];
					for (g2 = 0; g2 < 3; g2++) {
						genos = gen2[g2];

						if (genos in mresult[xronos][foni]) {
							tr = document.createElement("tr");
							th = document.createElement("th");
							text = document.createTextNode(genos);
							th.appendChild(text);
							tr.appendChild(th);
							for (a = 0; a < 15; a++) {
								td = document.createElement("td");
								text = document
										.createTextNode(mresult[xronos][foni][genos][a]);
								td.appendChild(text);
								if (parseInt(a / 5) == 1) {
									td.style.backgroundColor = "lightgray";
								}
								tr.appendChild(td);
							}
							tbody.appendChild(tr);
						}
					}
				}
			}
		}
		table.appendChild(tbody);
		$("αποτελέσματα").appendChild(table);
	}
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
			th.style.backgroundColor = "grey";
		}
		th.colSpan = "5";
		tr.appendChild(th);
	}
	thead.appendChild(tr);
	tr = document.createElement("tr");
	th = document.createElement("th");
	tr.appendChild(th);
	ptoseis = [ "Ονομαστική", "Γενική", "Δοτική", "Αιτιατική", "Κλητική" ];
	for (g = 0; g < 3; g++) {
		for (a = 0; a < ptoseis.length; a++) {
			th = document.createElement("th");

			text = document.createTextNode(ptoseis[a]);
			th.appendChild(text);
			if ((g * 5 + a) % 2 == 1) {
				th.style.backgroundColor = "lightgray";
			}
			tr.appendChild(th);
		}
	}
	thead.appendChild(tr);

	table.appendChild(thead);
	tbody = document.createElement("tbody");
	tr = document.createElement("tr");
	th = document.createElement("th");
	text = document.createTextNode($F("γένος"));
	th.appendChild(text);
	tr.appendChild(th);
	for (a = 0; a < 15; a++) {
		td = document.createElement("td");
		text = document.createTextNode(result[a]);
		td.appendChild(text);
		if (a % 2 == 1) {
			td.style.backgroundColor = "lightgray";
		}
		tr.appendChild(td);
	}
	tbody.appendChild(tr);
	table.appendChild(tbody);
	$("αποτελέσματα").appendChild(table);
}

function fillEpitheto(result) {
	$("αποτελέσματα").innerHTML = "";
	table = document.createElement("table");
	// BODY
	tbody = document.createElement("tbody");
	var tr = document.createElement("tr");
	th = document.createElement("th");
	tr.appendChild(th);
	ari8moi = [ "Ενικός", "Δυϊκός", "Πληθυντικός" ];
	for (g = 0; g < 3; g++) {
		th = document.createElement("th");
		text = document.createTextNode(ari8moi[g]);
		th.appendChild(text);
		if (g != 1) {
			th.style.backgroundColor = "grey";
		}
		th.colSpan = "5";
		tr.appendChild(th);
	}
	tbody.appendChild(tr);
	tr = document.createElement("tr");
	th = document.createElement("th");
	tr.appendChild(th);
	ptoseis = [ "Ονομαστική", "Γενική", "Δοτική", "Αιτιατική", "Κλητική" ];
	for (g = 0; g < 3; g++) {
		for (a = 0; a < ptoseis.length; a++) {
			th = document.createElement("th");

			text = document.createTextNode(ptoseis[a]);
			th.appendChild(text);
			if ((g * 5 + a) % 2 == 1) {
				th.style.backgroundColor = "lightgray";
			}
			tr.appendChild(th);
		}
	}
	tbody.appendChild(tr);
	gen2 = [ "Αρσενικό", "Θηλυκό", "Ουδέτερο" ];
	for (g2 = 0; g2 < 3; g2++) {
		tr = document.createElement("tr");
		th = document.createElement("th");
		text = document.createTextNode(gen2[g2]);
		th.appendChild(text);
		tr.appendChild(th);
		for (a = 0; a < 15; a++) {
			td = document.createElement("td");
			text = document.createTextNode(result[g2][a]);// [a]
			td.appendChild(text);
			if (a % 2 == 1) {
				td.style.backgroundColor = "lightgray";
			}
			tr.appendChild(td);
		}
		tbody.appendChild(tr);
	}
	table.appendChild(tbody);
	$("αποτελέσματα").appendChild(table);
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
