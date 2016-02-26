function toggl() {
	if ($("κοινή").style.backgroundColor == "") {
		$("κοινή").style.backgroundColor = "#000000";
		$("κοινή").style.color = "lightgray";
		$("δημοτική").style.backgroundColor = "";
		$("δημοτική").style.color = "";
	} else {
		$("κοινή").style.backgroundColor = "";
		$("κοινή").style.color = "";
		$("δημοτική").style.backgroundColor = "#000000";
		$("δημοτική").style.color = "lightgray";
	}
}

function analysi() {
	// αναλύει το κείμενο από το textarea id="κείμενο"
	// και συμπληρώνει τον πίνακα id="αποτέλεσμα"
	var dialektos="δημοτική";
	if ($("κοινή").style.backgroundColor != "") {dialektos="κοινή";}
	request = "ανάλυση/"+dialektos+"/" + $F("κείμενο");
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText); // plain text version
			//var result = transport.responseText.evalJSON(true); // json version
			fillTable(result);
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function anagnvrish() {
	// αναλύει το κείμενο από το textarea id="κείμενο"
	// και συμπληρώνει τον πίνακα id="αποτέλεσμα"
	var dialektos="δημοτική";
	if ($("κοινή").style.backgroundColor != "") {dialektos="κοινή";}
	request = "αναγνώριση/"+dialektos+"/" + $F("κείμενο");
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			var result = eval(transport.responseText);
			//var result = transport.responseText.evalJSON(true);
			fillTables(result);
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function fillTables(result) {
	$("αποτέλεσμα").innerHTML = "";
	for (i = 0; i < result.length; i++) {
		tbl     = document.createElement("table");
		tbody = document.createElement('tbody');
		row = document.createElement("tr");
		cellText = document.createTextNode(result[i][0]);
		cell = document.createElement("td");
		cell.appendChild(cellText);
		cell.colSpan = "4";
		cell.style.fontSize="larger"; 
		row.appendChild(cell);
		tbody.appendChild(row);
		for (z=0; z<result[i][1].length; z++) {
			row = document.createElement("tr");
			mtl = result[i][1][z]["μέρος του λόγου"]
			cellText = document.createTextNode(mtl);
			cell = document.createElement("td");
			cell.appendChild(cellText);
			cell.colSpan = "4";
			cell.align = "center";
			cell.style.fontWeight="bold"; 
			row.appendChild(cell);
			tbody.appendChild(row);
			
			var el = [['διάλεκτος', 'λήμμα'], ['μεταδεδομένα']];
			var style = "thick solid #000000";
			if (mtl=="επίθετο" || mtl=="ουσιαστικό" || mtl=="άρθρο") {
				el = [['λήμμα', 'κατάληξη'], ['διάλεκτος', 'γένος'], 
				      ['αριθμός', 'πτώση']];
				style = "thick solid #00FF00";
			} else if (mtl=="αντωνυμία") {
				el = [['κατάληξη', 'διάλεκτος'],['πρόσωπο', 'μεταδεδομένα'],
				      ['αριθμός', 'πτώση']];
				style = "thick solid #FF0000";
			} else if (mtl=="ρήμα" || mtl=="μετοχή"){
				el = [['θέμα', 'κατάληξη'], ['διάλεκτος', 'χρόνος'], 
						['φωνή', 'έγκλιση'], ['αριθμός', 'πρόσωπο']];
				style = "thick solid #0000FF";
				if (mtl=="μετοχή") { el[3][1]="πτώση";}
			}
			for (x=0;x<el.length;x++) {
				row = document.createElement("tr");
				for(y=0;y<el[x].length;y++) {
					var cellText1 = document.createTextNode(el[x][y]);
					var cellText2 = document.createTextNode(result[i][1][z][el[x][y]]);
					if (el[x][y]=='μεταδεδομένα' && mtl=="αντωνυμία") {
						cellText1 = document.createTextNode('τύπος αντωνυμίας');
						cellText2 = document.createTextNode(result[i][1][z]['μεταδεδομένα']['τύπος αντωνυμίας']);
					} else if (el[x][y]=='μεταδεδομένα') {
						cellText1 = document.createTextNode('ιδιότητες');
						cellText2 = document.createTextNode(result[i][1][z]['μεταδεδομένα']['ιδιότητες']);
					}
					
					cell = document.createElement("td");
					cell.appendChild(cellText1);
					row.appendChild(cell);
					
					cell = document.createElement("td");
					cell.appendChild(cellText2);
					row.appendChild(cell);
				}
				tbody.appendChild(row);
			}
		}
		tbl.appendChild(tbody);
		tbl.style.outline = style;
		$("αποτέλεσμα").appendChild(tbl);
		br = document.createElement("br");
		$("αποτέλεσμα").appendChild(br);
	}
}

function fillTable(result) {
	// συμπληρώνει τον πίνακα id="αποτέλεσμα" με το json του result

	// μηδενισμός πίνακα
	$("αποτέλεσμα").innerHTML = "";
	
	// δημιουργία επικεφαλίδων
	thead = document.createElement('thead');
	thead.innerHTML = "<tr><th><h2>Λέξη</h2></th><th>ΜτΛόγου</th><th>ανάλυση</th></tr>";
	$("αποτέλεσμα").appendChild(thead);
	
	// συμπλήρωση περιεχομένου
	tbody = document.createElement('tbody');
	$("αποτέλεσμα").appendChild(tbody);
	for (i = 0; i < result.length; i++) {
		// αν "στίξη" χρεισιμοποιούμε το αποτέλεσμα «χύμα»
		if (result[i][1]=="στίξη") {
			var row = document.createElement("tr");
			for (x=0; x<result[i].length; x++) {
				var cell = document.createElement("td");
				cellText = document.createTextNode(result[i][x]);
				cell.appendChild(cellText);
				row.appendChild(cell);
			}
			$("αποτέλεσμα").tBodies[0].appendChild(row);
		} else {
			// αν «μέρος του λόγου» εξηδικευμένη συμπλήρωση
			for (z=0; z<result[i][1].length; z++) {
				var row = document.createElement("tr");
				
				for (x=0; x<result[i].length; x++) {
					//alert(result[i][x]);
					var cell = document.createElement("td");
					// αν είναι το πρώτο αποτέλεσμα συμπληρώνουμε την λέξη που αναλύθηκε
					if (z==0 && x==0) {
						cellText = document.createTextNode(result[i][0]);
						cell.appendChild(cellText);
					} else if (x==0) {
						// αν δεν είναι το πρώτο αποτέλεσμα δεν συμπληρώνουμε την λέξη που αναλύθηκε
						cellText = document.createTextNode("");
						cell.appendChild(cellText);
					} else if (x==2 && (result[i][1][z]=="ρήμα" || result[i][1][z]=="μετοχή")) {
						tbl     = document.createElement("table");
						tb = document.createElement('tbody');
						el = [['θέμα', 'κατάληξη'], ['διάλεκτος', 'χρόνος'], 
							['φωνή', 'έγκλιση'], ['αριθμός', 'πρόσωπο']];
						if (result[i][1][z]=="μετοχή") { el[3][1]="πτώση";}
						for (rn=0;rn<4;rn++) {
							rw = document.createElement("tr");
							for (cn=0;cn<2;cn++) {
								cll = document.createElement("td");
								cllText = document.createTextNode(el[rn][cn]);
								cll.appendChild(cllText);
								rw.appendChild(cll);
								
								cll = document.createElement("td");
								cllText = document.createTextNode(result[i][2][z][el[rn][cn]]);
								cll.appendChild(cllText);
								rw.appendChild(cll);
								}
							tb.appendChild(rw);}
						tbl.appendChild(tb);
						tbl.style.outline = "thick solid #0000FF";
						cellText = document.importNode(tbl, true);
						cell.appendChild(cellText);
					} else if (x==2 && (result[i][1][z]=="επίθετο" || result[i][1][z]=="ουσιαστικό" || result[i][1][z]=="άρθρο")) {
						tbl     = document.createElement("table");
						tb = document.createElement('tbody');
						el = [['λήμμα', 'κατάληξη'], ['διάλεκτος', 'γένος'], 
							['αριθμός', 'πτώση']];
						for (rn=0;rn<3;rn++) {
							rw = document.createElement("tr");
							for (cn=0;cn<2;cn++) {
								cll = document.createElement("td");
								cllText = document.createTextNode(el[rn][cn]);
								cll.appendChild(cllText);
								rw.appendChild(cll);
								
								cll = document.createElement("td");
								cllText = document.createTextNode(result[i][2][z][el[rn][cn]]);
								cll.appendChild(cllText);
								rw.appendChild(cll);
								}
							tb.appendChild(rw);}
						tbl.appendChild(tb);
						tbl.style.outline = "thick solid #00FF00";
						cellText = document.importNode(tbl, true);
						cell.appendChild(cellText);
					} else if (x==2 && result[i][1][z]=="αντωνυμία") {
						tbl     = document.createElement("table");
						tb = document.createElement('tbody');
						el = [['κατάληξη', 'διάλεκτος'],
						      ['πρόσωπο', 'μεταδεδομένα'],
						      ['αριθμός', 'πτώση']];
						for (rn=0;rn<el.length;rn++) {
							rw = document.createElement("tr");
							for (cn=0;cn<2;cn++) {
								cll = document.createElement("td");
								if (el[rn][cn]=='μεταδεδομένα') {
									cllText = document.createTextNode('τύπος αντωνυμίας');}
								else {
									cllText = document.createTextNode(el[rn][cn]);
								}
								cll.appendChild(cllText);
								rw.appendChild(cll);
								
								cll = document.createElement("td");
								if (el[rn][cn]=='μεταδεδομένα') {
									cllText = document.createTextNode(result[i][2][z]['μεταδεδομένα']['τύπος αντωνυμίας']);
								} else {
									cllText = document.createTextNode(result[i][2][z][el[rn][cn]]);}
								cll.appendChild(cllText);
								rw.appendChild(cll);
								}
							tb.appendChild(rw);}
						tbl.appendChild(tb);
						tbl.style.outline = "thick solid #FF0000";
						cellText = document.importNode(tbl, true);
						cell.appendChild(cellText);
					} else if (x==2)  {
						// προσθήκη των υπόλοιπων, κανονικά
						tbl     = document.createElement("table");
						tb = document.createElement('tbody');
						el = [['διάλεκτος', 'λήμμα'],
						      ['μεταδεδομένα']];
						
						for (rn=0;rn<el.length;rn++) {
							rw = document.createElement("tr");
							for (cn=0;cn<el[rn].length;cn++) {
								cll = document.createElement("td");
								if (el[rn][cn]=='μεταδεδομένα') {
									cllText = document.createTextNode('ιδιότητες');}
								else {
									cllText = document.createTextNode(el[rn][cn]);}	
								cll.appendChild(cllText);
								rw.appendChild(cll);
								
								cll = document.createElement("td");
								if (el[rn][cn]=='μεταδεδομένα') {
									cllText = document.createTextNode(result[i][2][z]['μεταδεδομένα']['ιδιότητες']);
								} else {
									cllText = document.createTextNode(result[i][2][z][el[rn][cn]]);}
								
								cll.appendChild(cllText);
								rw.appendChild(cll);}
							tb.appendChild(rw);}
						tbl.appendChild(tb);
						tbl.style.outline = "thick solid #000000";
						cellText = document.importNode(tbl, true);
						cell.appendChild(cellText);
					} else {
						cellText = document.createTextNode(result[i][x][z]);
						cell.appendChild(cellText);
					}
					row.appendChild(cell);
				}
				$("αποτέλεσμα").tBodies[0].appendChild(row);
			}
		}
	}
}
