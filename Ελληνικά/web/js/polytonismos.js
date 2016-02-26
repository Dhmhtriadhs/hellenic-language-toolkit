var active = true;
var IMEoffset = 0;
var maxCandidates = 0;
var candidates = [];
var counter = 0;

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

function tonismos() {
	// τονίζει το κείμενο από το textarea id="κείμενο"
	// και το εμφανίζει στο textarea id="αποτέλεσμα"
	var dialektos = "δημοτική";
	if ($("κοινή").style.backgroundColor != "") {
		dialektos = "κοινή";
	}
	request = "πολυτονισμός/" + dialektos + "/" + $F("κείμενο");
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			$("αποτέλεσμα").value = transport.responseText;
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function poly(child) {
	requestURL = 'πολυτονισμός/δημοτική/' + child.textContent;
	// alert(requestURL);
	var xmlhttp = new Ajax.Request(requestURL, {
		method : 'post',
		onSuccess : function(transport) {
			child.textContent = transport.responseText;
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		},
		asynchronous : false
	});
}

function poly2(child) {
	requestURL = 'πολυτονισμός/δημοτική/' + child.textContent;
	var request = new XMLHttpRequest();
	request.open('POST', requestURL, true);
	request.onreadystatechange = function() {
		if (request.readyState == 4) {
			child.textContent = request.responseText;
		}
	}
	request.send(null);
}

function htmlTree(obj) {
	// alert(obj);
	// var obj = obj || document.getElementsByTagName('body')[0];
	if (obj.hasChildNodes()) {
		var child = obj.firstChild;
		while (child) {
			if (child.nodeType === 1) {
				htmlTree(child);
			}
			if (child.nodeType === 3) {
				if (child.textContent.length > 1) {
					poly2(child);
				}
			}
			child = child.nextSibling;
		}
	}
}
function iframeRef(frameRef) {
	return frameRef.contentWindow ? frameRef.contentWindow.document
			: frameRef.contentDocument
}

function potonismos() {
	var inside = iframeRef(document.getElementById('one'))
	htmlTree(inside);
}

function updateCandidates(value) {
	var dialektos = "δημοτική";
	if ($("κοινή").style.backgroundColor != "") {
		dialektos = "κοινή";
	}
	request = "IME/" + dialektos + "/" + value;
	//alert(request);
	var xmlhttp = new Ajax.Request(request, {
		method : 'post',
		onSuccess : function(transport) {
			//alert(transport.responseText);
			candidates = eval(transport.responseText);
			IMEoffset = 0;
			updateTable();
		},
		onFailure : function() {
			alert('Something went wrong in kathgories.');
		}
	});
}

function IME(event) {
	request = $F("κείμενο");
	var acc = "";
	start = request.length;
	alert(start);
	for(n=start;n>-1;--n) {
		var letter = request[n];
		if (request.charCodeAt(n) > 64 && request.charCodeAt(n) < 123) {
			//String.fromCharCode(event.keyCode);
			acc = request[n]+;			
		} else {
			break;
		}
	}
	alert(acc);
	updateCandidates(acc);
	switch (event.keyCode) {
	case Event.KEY_ESC:
		if (active) {
			$("αποτελέσματα").hide();
			active = false;
			Event.stop(event);
		} else {
			$("αποτελέσματα").show();
			active = true;
			Event.stop(event);
		}
		return;
	case Event.KEY_TAB:
	case 32:
		Event.stop(event);
		commit(true);
		return;
	case Event.KEY_RETURN:
		Event.stop(event);
		commit(false);
		return;
	case Event.KEY_UP:
		IMEoffset -= 1;
		if (IMEoffset <= 0) {
			IMEoffset = 0;
		}
		Event.stop(event);
		updateTable();
		return;
	case Event.KEY_DOWN:
		Event.stop(event);
		IMEoffset += 1;
		if (IMEoffset >= maxCandidates) {
			IMEoffset = maxCandidates - 1;
		}
		updateTable();
		return;
	}
}

function commit(bypass) {
	if (bypass) {
		by = $("κείμενο").value.length;
		var neo = "";
		last = $("κείμενο").value[by - 1];
		for (b = 0; b < by - 1; b++) {
			neo += $("κείμενο").value[b];
		}
		$("κείμενο").value = neo + candidates[IMEoffset] + last;
	} else {
		$("κείμενο").value += candidates[IMEoffset];
	}
	resetTable();
}

function resetTable() {
	for (ai = 0; ai < 10; ai++) {
		row = parseInt(ai / 5);
		column = ai - row * 5;
		$("αποτελέσματα").tBodies[0].rows[row].cells[column].innerHTML = "";
		$("αποτελέσματα").tBodies[0].rows[row].cells[column].style.backgroundColor = "#FFFFFF";
	}
}

function updateTable() {

	var countTo = 10;
	if (candidates.length < 10) {
		maxCandidates = candidates.length;
	}

	for (ai = 0; ai < maxCandidates; ai++) {
		row = parseInt(ai / 5);
		column = ai - row * 5;
		$("αποτελέσματα").tBodies[0].rows[row].cells[column].innerHTML = ai
				.toString()
				+ ": " + candidates[ai];
		$("αποτελέσματα").tBodies[0].rows[row].cells[column].style.backgroundColor = "#FFFFFF";
		if (ai == IMEoffset) {
			$("αποτελέσματα").tBodies[0].rows[row].cells[column].style.backgroundColor = "#00FF00";
		}
	}
}
