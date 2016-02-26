var dialektoi = null;
var istoria = null;

// ΜΟΔΕ
function EN_APXH() {
	nea(true);
	loadDialektous();
}

function boh_theia() {
	keimeno = "Ἐτικέτες: δείκτες για την κατάσταση της διαλέκτου, π.χ. για έλεγχο ποιότητας.\n";
	keimeno += "Η διαγραφή και η αποθήκευση είναι «εικονική» για να διορθώνονται τα σφάλματα της βάσης δεδομένων εύκολα.\n";
	keimeno += "Εικονική Διάλεκτος: Η διάλεκτος κληρονομεί τις κατηγορίες του «Εικονική».\n";
	keimeno += "   Χρησιμοποιείται για να ξεχωρίσουν οι ξένες λέξεις,\n";
	keimeno += "   π.χ. Ελληνέζικα: μπαρόβιος, «Εικονική»: Δημοτική.\n";
	keimeno += "Πτώσεις: ρυθμίζει τις κλίσεις-αναγνωρίσεις για τα ονόματα, για λόγο απόδοσης.\n";
	keimeno += "Διάλεκτοι: επεκτάσεις,  αν η λέξη δεν υπάρχει στην βασική διάλεκτο, γίνεται αναγνώριση-κλίση στις άλλες, κατά σειρά προτεραιότητας.\n";
	keimeno += "Δυϊκός: τα ρήματα θα έχουν δυϊκός ρυθμό;\n";
	keimeno += "Χρόνοι: ρυθμίζει τις κλίσεις-αναγνωρίσεις για τα ρήματα, για λόγο απόδοσης.\n";
	alert(keimeno);
}

function nea(hid) {
	$("τίτλος").value = "";
	$("Ἡμερομηνία").innerHTML = "";
	$("τίτλος").focus();	
	removeOptionsAlternate("δΔιάλεκτοι");
	while ($("εΔιάλεκτοι").options.length>0) { $("εΔιάλεκτοι").remove(0);};
	if(hid) {
		removeOptionsAlternate("πΔιαλέκτων");
		while ($("πΙστορίας").options.length>0) { $("πΙστορίας").remove(0);};}
	
	$("ἐτικέτες").value = "τρέχον, ";
	$("Παρατηρήσεις").value = "";
	for(row=2;row<7;row++) {
		for(cell=1;cell<4;cell++) {
			var onoma = $("ονόματα").tBodies[0].rows[row].cells[cell].firstChild;
			if(onoma.tagName=="INPUT") {
				onoma.checked = false;}
		}
	}
	for(row=3;row<45;row++) {
		for(cell=1;cell<4;cell++) {
			var xronoi = null;
			
			if((row-3)%6==0) {
				xronoi = $("χρόνοι").tBodies[0].rows[row].cells[cell+3];
			} else {
				xronoi = $("χρόνοι").tBodies[0].rows[row].cells[cell];
			}
			
			if(xronoi.firstChild.tagName=="INPUT") {
				xronoi.firstChild.checked = false;}
		}
	}
	$("Δυϊκός").checked = false;
	$("Δοτική").checked = false;
	$("εικονική")[0] = new Option("");
	if (dialektoi) {
		var counter = 0;
		dia = Object.keys(dialektoi);
		
		for (d = 0; d < dia.length; d++) {
			$("δΔιάλεκτοι")[counter] = new Option(dia[d]);
			$("εικονική")[counter+1] = new Option(dia[d]);
			counter += 1;
		}
	}
}

function loadIstoria(aa) {
	if ($("πΔιαλέκτων").selectedIndex != -1) {
		request = "develop/ιστορικό_διαλέκτου/" + Object.toJSON(aa);
		var xmlhttp = new Ajax.Request(request, {
			method : 'post',
			onSuccess : function(transport) {
				var result = eval(transport.responseText);
				istoria = result;
				removeOptionsAlternate("πΙστορίας");
				var counter = 0;
				var maxdate = 0;
				var maxd_pos = -1;
				var trex = -1;
				for (k = 0; k < istoria.length; k++) {
					b = istoria[k]["Ἡμερομηνία"] + " " + istoria[k]['ἐτικέτες'];
					$("πΙστορίας")[counter] = new Option(b);
					
					if (istoria[k]['ἐτικέτες'].match("τρέχον")) {
						$("πΙστορίας")[counter].selected;
						trex=k;}
					
					if (maxdate<istoria[k]["Ἡμερομηνία"]) {
						maxd_pos = k;
						maxdate=istoria[k]["Ἡμερομηνία"];}
					
					counter += 1;
				}
				if (trex==-1) { trex=maxd_pos;}
				showDialekto(istoria[trex]);
			},
			onFailure : function() {
				alert('Something went wrong in loadIstoria.');
			}
		});
	}
}

function loadDialektous() {
	request = "dump/διάλεκτοι";
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			dialektoi = result[0];
			updateDialektoi();
		},
		onFailure : function() {
			alert('Something went wrong in loadDialektous.');
		}
	});
}

function updateDialektoi() {
	if (dialektoi == null) {
		return;
	}
	var counter = 0;
	dia = Object.keys(dialektoi);
	$("εικονική")[0] = new Option("");
	for (d = 0; d < dia.length; d++) {
		aa = dialektoi[dia[d]]["ΑΑ"];
		$("πΔιαλέκτων")[counter] = new Option(aa+" "+dia[d]);
		$("δΔιάλεκτοι")[counter] = new Option(dia[d]);
		$("εικονική")[counter+1] = new Option(dia[d]);
		counter += 1;
	}
}

function dedomenaDialektou() {
	var dedomena = [];
	
	var dat = {
		"όνομα" : $F("τίτλος"),
		"ἐτικέτες" : $F("ἐτικέτες"),
		"Παρατηρήσεις" : $("Παρατηρήσεις").value,
		"εικονική": $F("εικονική"),
		"πτώσεις" : [],
		"ρήμα" : {}, // χρόνος:[φωνή-έγκλιση]
		"μετοχή" : {}, // χρόνος:[φωνή-γένος]
		"επεκτάσεις":[],
		"ΑΑ":0,
		"δυϊκός" : 0, // αριθμός-πρόσωπο
		"δοτική" : 0
		};
	if ($("πΔιαλέκτων").selectedIndex!=-1) {
		epilogi = $F("πΔιαλέκτων");
		epilogi = epilogi.split(" ")[1];
		dat["ΑΑ"] = dialektoi[epilogi]["ΑΑ"];
		dat["Κλειδί"] = dialektoi[epilogi]["Κλειδί"];
	}
	if ($("Δυϊκός").checked==true) {
		dat["δυϊκός"] = 1;
	}
	if ($("Δοτική").checked==true) {
		dat["δοτική"] = 1;
	}
	for(i=0;i<$("εΔιάλεκτοι").length;i++) {
		dat["επεκτάσεις"].push($("εΔιάλεκτοι")[i].value);
	};
	
	for(cell=1;cell<4;cell++) {
		for(row=2;row<7;row++) {
			var onoma = $("ονόματα").tBodies[0].rows[row].cells[cell].firstChild;
			if(onoma.tagName=="INPUT") { 
				if (onoma.checked==true) { dat["πτώσεις"].push(1);
					} else { dat["πτώσεις"].push(0);};
			}
		}
	}
	
	var xronos = "";
	for(row=3;row<45;row++) {
		var sylogi = [];
		for(cell=1;cell<4;cell++) {
			var xronoi = null;
			
			if((row-3)%6==0) {
				xronoi = $("χρόνοι").tBodies[0].rows[row].cells[cell+3];
				if(xronoi.firstChild.tagName=="INPUT") {
					if(xronoi.firstChild.checked == true) {
						sylogi.push(1);sylogi.push(1);sylogi.push(1);
					} else { sylogi.push(0);sylogi.push(0);sylogi.push(0); };
				}
			} else {
				xronoi = $("χρόνοι").tBodies[0].rows[row].cells[cell];
				if(xronoi.firstChild.tagName=="INPUT") {
					if (xronoi.firstChild.checked == true) {
						val = (row-3)%6-1+(cell-1)*5;
						dat["ρήμα"][xronos][val] = 1;
					};
				}
			}
		}
		
		if((row-3)%6==0) {
			xronos = $("χρόνοι").tBodies[0].rows[row].cells[0].firstChild.textContent;
			dat["ρήμα"][xronos] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
			dat["μετοχή"][xronos] = sylogi;
		}
	}
	
	return dat;
}

function apothikeusi() {
	message = dedomenaDialektou();
	request = "develop/αποθήκευση_διαλέκτου/" + Object.toJSON(message);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			if (transport.responseText == "OK") {
				alert("Αποθηκεύτικε!");
				EN_APXH();
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
	if ($("πΔιαλέκτων").selectedIndex != -1) {
		message = dedomenaDialektou();
		request = "develop/διαγραφή_διαλέκτου/" + Object.toJSON(message);
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

function epilogiDialektou() {
	nea(false);
	while ($("πΙστορίας").options.length>0) { $("πΙστορίας").remove(0);}
	if ($("πΔιαλέκτων").selectedIndex != -1) {
		aa=dialektoi[$F("πΔιαλέκτων").split(" ")[1]];
		loadIstoria(aa);
	}
}

function showDialekto(data) {
	if ($("πΔιαλέκτων").selectedIndex != -1) {
		$("τίτλος").value = data["όνομα"];
		while ($("εΔιάλεκτοι").length>0) { $("εΔιάλεκτοι").remove(0);};
		$("ἐτικέτες").value = data["ἐτικέτες"];
		$("Ἡμερομηνία").innerHTML = data["Ἡμερομηνία"];
		$("Παρατηρήσεις").value = data["Παρατηρήσεις"];
		
		if (data["δυϊκός"]==1) {
			$("Δυϊκός").checked = true; 
		} else {
			$("Δυϊκός").checked = false;
		}
		
		if (data["δοτική"]==1) {
			$("Δοτική").checked = true; 
		} else {
			$("Δοτική").checked = false;
		}
		
		for(p=0;p<data["πτώσεις"].length;p++) {
			cell = parseInt(data["πτώσεις"][p]/5) + 1;
			row  = data["πτώσεις"][p]%5 + 2;
			onoma = $("ονόματα").tBodies[0].rows[row].cells[cell].firstChild;
			if(onoma.tagName=="INPUT") { onoma.checked = true; }
		}
		epektaseis = data["επεκτάσεις"];
		for(e=0;e<epektaseis.length;e++) {
			$("εΔιάλεκτοι")[e] = new Option(epektaseis[e]);
			removeValue("δΔιάλεκτοι", epektaseis[e]);
		}
		
		xronoi = Object.keys(data["ρήμα"]);
		xr_p = {"ενεστώτας":4,"παρατατικός":10,"αόριστος":16,
				"παρακείμενος":22,"υπερσυντέλικος":28,
				"μέλλοντας":34, "συντελεσμένος μέλλοντας":40};
		for(x=0;x<xronoi.length;x++) {
			xronos = xronoi[x];
			times = data["ρήμα"][xronos];
			for(t=0;t<times.length;t++) {
				row = (times[t]%5)+xr_p[xronos];
				col = parseInt(times[t]/5)+1;
				onoma = $("χρόνοι").tBodies[0].rows[row].cells[col];
				if(onoma.firstChild.tagName=="INPUT") { onoma.firstChild.checked = true; }
			}
		}
		xronoi = Object.keys(data["μετοχή"]);
		for(x=0;x<xronoi.length;x++) {
			xronos = xronoi[x];
			times = data["μετοχή"][xronos];
			for(t=0;t<times.length;t++) {
				row = xr_p[xronos]-1;
				col = parseInt(times[t]/3)+4;
				onoma = $("χρόνοι").tBodies[0].rows[row].cells[col];
				if(onoma.firstChild.tagName=="INPUT") { onoma.firstChild.checked = true; }
			}
		}
		selectValue("εικονική", data["εικονική"]);
	}
}

function epilogiIstorias() {
	index = $("πΙστορίας").selectedIndex;
	if (index != -1) {
		showDialekto(istoria[index]);
	}
}

function trexon() {
	if ($("πΙστορίας").selectedIndex != -1) {
		message = istoria[$("πΙστορίας").selectedIndex];
		request = "develop/τρέχον_διάλεκτος/" + Object.toJSON(message);
		var xmlhttp = new Ajax.Request(request, {
			method : 'post',
			onSuccess : function(transport) {
				if (transport.responseText=="OK"){
					epilogiDialektou();
					loadIstoria();}
			},
			onFailure : function() {
				alert('Something went wrong in trexon.');
			}
		});
	}
}

function prosthiki() {
	if ($("δΔιάλεκτοι").selectedIndex!=-1) {
		n = $("εΔιάλεκτοι").length;
		$("εΔιάλεκτοι")[n] = new Option($F("δΔιάλεκτοι"));
		$("δΔιάλεκτοι").remove($("δΔιάλεκτοι").selectedIndex);
	}
}

function afairesh() {
	if ($("εΔιάλεκτοι").selectedIndex!=-1) {
		n=$("δΔιάλεκτοι").length;
		$("δΔιάλεκτοι")[n] = new Option($F("εΔιάλεκτοι"));
		$("εΔιάλεκτοι").remove($("εΔιάλεκτοι").selectedIndex);
	}
}

function pano() {
	index = $("εΔιάλεκτοι").selectedIndex;
	if (index>0 && index<$("εΔιάλεκτοι").length) {
		var opt = $("εΔιάλεκτοι")[index];
		$("εΔιάλεκτοι").removeChild(opt);
		$("εΔιάλεκτοι").insertBefore(opt, $("εΔιάλεκτοι")[index - 1]);
	}
}

function kato() {
	index = $("εΔιάλεκτοι").selectedIndex;
	if (index>-1 && index<$("εΔιάλεκτοι").length) {
		var opt = $("εΔιάλεκτοι")[index];
		$("εΔιάλεκτοι").removeChild(opt);
		$("εΔιάλεκτοι").insertBefore(opt, $("εΔιάλεκτοι")[index+1]);
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
	while (obj.options.length > 0) {
		obj.remove(0);
	}
}
