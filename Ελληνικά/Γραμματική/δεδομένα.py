#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, dimitriadis dimitris
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#	 * Redistributions of source code must retain the above copyright
#		notice, this list of conditions and the following disclaimer.
#	 * Redistributions in binary form must reproduce the above copyright
#		notice, this list of conditions and the following disclaimer in the
#		documentation and/or other materials provided with the distribution.
#	 * Neither the name of the dimitriadis dimitris nor the
#		names of its contributors may be used to endorse or promote products
#		derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL dimitriadis dimitris BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

τύπωσε = print
κείμενο = str
μήκος = len
εύρος = range
import os

if "Γραμματική" in os.getcwd():
	import δεδομένα_json, δοκιμές_json, δεδομένα_sql
else:
	import Ελληνικά.Γραμματική.JSON.json as δεδομένα_json
	import Ελληνικά.Γραμματική.JSON.δοκιμές as δοκιμές_json
	import Ελληνικά.Γραμματική.SQL.sql as δεδομένα_sql
	import Ελληνικά.Γραμματική.ευρετήρια as ευρετήρια

class Δεδομένα():
	def __init__(self, τονιστής, develop=None):
		self.json = δεδομένα_json.Δεδομένα(τονιστής)
		self.json_δοκιμές = δοκιμές_json.Δεδομένα()
		self.sql = δεδομένα_sql.Δεδομένα(τονιστής)
		self.τ = τονιστής
		
		self.__μεταβλητές()
		if develop:
			#self.json.φόρτωση_άκλητα()
			#self.κατηγορίες_αντωνυμιών = self.json.κατηγορίες_αντωνυμιών
			self.sql.επαναφόρτωση(self.δ)
		else:
			self.json.επαναφόρτωση()
			self.κατηγορίες = self.json.κατηγορίες
			self.θέματα = self.json.θέματα
			self.τονισμοί = self.json.τονισμοί
			self.ανώμαλα = self.json.ανώμαλα
			self.κατηγορίες_αντωνυμιών = self.json.κατηγορίες_αντωνυμιών
			self.μεταδεδομένα = self.json.μεταδεδομένα
			self.κλίμακες = self.json.κλίμακες
		
		self.json_δοκιμές.φόρτωση(self.κ)
		self._ευρετήρια = ευρετήρια.Ευρετήρια(self.τ, self.δ["διάλεκτοι"])
		self.α["ανώμαλων"], self.α["καταλήξεων"], self.κατηγορίες_αντωνυμιών = self._ευρετήρια.αναλύσεις(
			self.δ["ανώμαλα"], self.δ["καταλήξεις"])
		ακθ = self._ευρετήρια.ευρετήριο(self.α["ανώμαλων"], self.α["καταλήξεων"], self.δ["θέματα"], απλοποιητής=None)
		self.ε["βασικό"]["ανώμαλα"], self.ε["βασικό"]["καταλήξεις"], self.ε["βασικό"]["θέματα"] = ακθ
	
	def __μεταβλητές(self):
		# δεδομένα
		self.δ = {
			"διάλεκτοι":{}, "ανώμαλα":{}, "τονισμοί":{}, "καταλήξεις":{},
			"μεταδεδομένα":{}, "κλίμακες":{}, "θέματα":[], "ομάδες":{"ρήμα":{}, "μετοχή":{}},
			"κατηγοριοτονισμoί":{"ουσιαστικό":{}, "επίθετο":{}, "ρήμα":{}, "μετοχή":{}},
			"ορθογραφία":{}, "στίξη":{}
			}
		# ευρετήρια
		self.ε = {"βασικό":
						{"ανώμαλα":{}, "καταλήξεις":{}, "θέματα":{}}
					}
		# αναλύσεις
		self.α = {"ανώμαλων":[], "καταλήξεων":[]}
		# δοκιμές
		self.κ = {"ουσιαστικό":{}, "επίθετο":{}, "μετοχή":{}, "ρήμα":{}, "αντωνυμία":{}}
		
		self.κατηγορίες_αντωνυμιών = {}
		
		self.δ["στίξη"] = {
			' ': {"στίξη":" ", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["κενό"]}},
			',': {"στίξη":",", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["κόμμα"]}},
			"'": {"στίξη":"'", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["απόστροφος"]}},
			'.': {"στίξη":".", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["τελεία"]}},
			'·': {"στίξη":"·", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["τελεία", "άνω"]}},
			'(': {"στίξη":"(", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["παρένθεση", "ανοιχτή"]}},
			')': {"στίξη":")", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["παρένθεση", "κλειστή"]}},
			'«': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			'»': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			'[': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			']': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			'{': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			'}': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			'!': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			':': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			';': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			'-': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"'": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"+": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"/": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"\\": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"*": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"=": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"·": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῾": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"᾽": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"᾿": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῀": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"´": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"ι": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῁": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῍": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῎": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῏": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῝": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῞": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῟": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"῭": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"΅": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"`": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"<": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			">": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			'"': {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"@": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"#": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"%": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"^": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"|": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"$": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"&": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"_": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"'": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"?": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"`": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"~": {"στίξη":")", "μέρος του λόγου":"στίξη"},
			"0": {"στίξη":"0", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["μηδέν"]}},
			"1": {"στίξη":"1", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["ένα"]}},
			"2": {"στίξη":"2", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["δύο"]}},
			"3": {"στίξη":"3", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["τρία"]}},
			"4": {"στίξη":"4", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["τέσσερα"]}},
			"5": {"στίξη":"5", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["πέντε"]}},
			"6": {"στίξη":"6", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["έξι"]}},
			"7": {"στίξη":"7", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["εφτά"]}},
			"8": {"στίξη":"8", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["οκτό"]}},
			"9": {"στίξη":"9", "μέρος του λόγου":"στίξη", "Μεταδεδομένα":{"όνομα":["αριθμός"], "αριθμός":["εννιά"]}},
								}
	
	def ορθογραφία_διαγραφή(self, πακέτο):
		ορθογραφία = {}
		self.sql.ορθογραφία.διαγραφή(πακέτο, ορθογραφία)
		return ορθογραφία
	
	def ορθογραφία_νέα(self, πακέτο):
		ορθογραφία = {}
		self.sql.ορθογραφία.νέα(πακέτο, ορθογραφία)
		return ορθογραφία	
		
	def ορθογραφία_φόρτωση(self):
		ορθογραφία = {}
		self.sql.ορθογραφία.φόρτωση(ορθογραφία)
		return ορθογραφία
	
	def διάλεκτοι_φόρτωση(self, όλα=False):
		if όλα:
			διάλεκτοι = {}
			self.sql.διάλεκτοι.φόρτωση(διάλεκτοι, True)
			return διάλεκτοι
		else:
			self.sql.διάλεκτοι.φόρτωση(self.δ["διάλεκτοι"])
	
	def διάλεκτοι_νέα(self, αναγνώριση):
		self.sql.διάλεκτοι.νέα(αναγνώριση, self.δ["διάλεκτοι"])
		
	def διάλεκτοι_διαγραφή(self, αναγνώριση):
		self.sql.διάλεκτοι.διαγραφή(αναγνώριση, self.δ["διάλεκτοι"])
		
	def διάλεκτοι_ιστορικό(self, αναγνώριση):
		return self.sql.διάλεκτοι.ιστορικό(αναγνώριση)
		
	def διάλεκτοι_τρέχον(self, αναγνώριση):
		self.sql.διάλεκτοι.τρέχον(αναγνώριση, self.δ["διάλεκτοι"])
	
	def τονισμοί_φόρτωση(self, όλα=False):
		if όλα:
			τονισμοί = {}
			self.sql.τονισμοί.φόρτωση(τονισμοί, True)
			return τονισμοί
		else:
			self.sql.τονισμοί.φόρτωση(self.δ["τονισμοί"])
			
	def τονισμοί_νέος(self, αναγνώριση):
		self.sql.τονισμοί.νέος(αναγνώριση, self.δ["τονισμοί"])
		
	def τονισμοί_διαγραφή(self, αναγνώριση):
		self.sql.τονισμοί.διαγραφή(αναγνώριση, self.δ["τονισμοί"])
	
	def τονισμοί_ιστορικό(self, αναγνώριση):
		return self.sql.τονισμοί.ιστορικό(αναγνώριση)
	
	def τονισμοί_τρέχον(self, αναγνώριση):
		self.sql.τονισμοί.τρέχον(αναγνώριση, self.δ["τονισμοί"])
	
	def καταλήξεις_φόρτωση(self, όλα=False):
		if όλα:
			καταλήξεις = {}
			self.sql.καταλήξεις.φόρτωση(καταλήξεις, True)
			return καταλήξεις
		else:
			self.sql.καταλήξεις.φόρτωση(self.δ["καταλήξεις"])
			
	def καταλήξεις_ιστορικό(self, αναγνώριση):
		return self.sql.καταλήξεις.ιστορικό(αναγνώριση)
	
	def καταλήξεις_νέα(self, αναγνώριση):
		self.sql.καταλήξεις.νέα(αναγνώριση, self.δ["καταλήξεις"])
		
	def καταλήξεις_τρέχον(self, αναγνώριση):
		return self.sql.καταλήξεις.τρέχον(αναγνώριση, self.δ["καταλήξεις"])
	
	def καταλήξεις_διαγραφή(self, αναγνώριση):
		self.sql.καταλήξεις.διαγραφή(αναγνώριση, self.δ["καταλήξεις"])
		
	def ανώμαλα_φόρτωση(self, όλα=False):
		if όλα:
			ανώμαλα = {}
			self.sql.ανώμαλα.φόρτωση(ανώμαλα, self.δ["μεταδεδομένα"], self.δ["κλίμακες"], True)
			return ανώμαλα
		else:
			self.sql.ανώμαλα.φόρτωση(self.δ["ανώμαλα"], self.δ["μεταδεδομένα"], self.δ["κλίμακες"])
	
	def ανώμαλα_ιστορικό(self, αναγνώριση):
		return self.sql.ανώμαλα.ιστορικό(αναγνώριση, self.δ["μεταδεδομένα"], self.δ["κλίμακες"])
	
	def ανώμαλα_τρέχον(self, αναγνώριση):
		return self.sql.ανώμαλα.τρέχον(αναγνώριση, self.δ["ανώμαλα"], self.δ["μεταδεδομένα"], self.δ["κλίμακες"])
	
	def ανώμαλα_διαγραφή(self, αναγνώριση):
		self.sql.ανώμαλα.διαγραφή(αναγνώριση, self.δ["ανώμαλα"], self.δ["μεταδεδομένα"], self.δ["κλίμακες"])
	
	def ανώμαλα_νέο(self, αναγνώριση):
		self.sql.μεταδεδομένα.νέα(αναγνώριση, self.δ["μεταδεδομένα"])
		self.sql.κλίμακες.νέα(αναγνώριση, self.δ["κλίμακες"])
		self.sql.ανώμαλα.νέα(αναγνώριση, self.δ["ανώμαλα"], self.δ["μεταδεδομένα"], self.δ["κλίμακες"])
		
	def ουσιαστικά_φόρτωση(self, όλα=False):
		if όλα:
			ουσιαστικά = []
			κατηγοριοτονισμoί = {}
			self.sql.ουσιαστικά.φόρτωση(ουσιαστικά, self.δ["μεταδεδομένα"], self.δ["κλίμακες"], κατηγοριοτονισμoί,
				self.δ["καταλήξεις"]["ουσιαστικό"], self.δ["τονισμοί"]["ουσιαστικό"], self.δ["διάλεκτοι"], True)
			return [ουσιαστικά, κατηγοριοτονισμoί]
		else:
			self.sql.ουσιαστικά.φόρτωση(self.δ["ουσιαστικά"], self.δ["μεταδεδομένα"],
												self.δ["κλίμακες"], self.δ["κατηγοριοτονισμoί"]["ουσιαστικό"],
												self.δ["καταλήξεις"]["ουσιαστικό"], self.δ["τονισμοί"]["ουσιαστικό"], 
												self.δ["διάλεκτοι"])
	
	def ουσιαστικά_ιστορικό(self, αναγνώριση):
		return self.sql.ουσιαστικά.ιστορικό(αναγνώριση, self.δ["μεταδεδομένα"], self.δ["κλίμακες"])
	
	def ουσιαστικό_νέο(self, αναγνώριση):
		self.sql.μεταδεδομένα.νέα(αναγνώριση, self.δ["μεταδεδομένα"])
		self.sql.κλίμακες.νέα(αναγνώριση, self.δ["κλίμακες"])
		ουσιαστικά = []
		self.sql.ουσιαστικά.νέα(αναγνώριση, ουσιαστικά, self.δ["μεταδεδομένα"], self.δ["κλίμακες"],
								self.δ["κατηγοριοτονισμoί"]["ουσιαστικό"],
								self.δ["καταλήξεις"]["ουσιαστικό"], self.δ["τονισμοί"]["ουσιαστικό"],
								self.δ["διάλεκτοι"])
		δείκτης_θ = 0
		δείκτης_ο = 0
		μήκος_ο = len(ουσιαστικά)
		while δείκτης_θ < len(self.δ["θέματα"]) and δείκτης_ο < μήκος_ο:
			if self.δ["θέματα"][δείκτης_θ]:
				if self.δ["θέματα"][δείκτης_θ]["μέρος του λόγου"] == "ουσιαστικό":
					self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
					δείκτης_ο += 1
			else:
				self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
				δείκτης_ο += 1
			δείκτης_θ += 1
		if δείκτης_θ == len(self.δ["θέματα"]):
			for ν in range(δείκτης_ο, μήκος_ο):
				self.δ["θέματα"].append(ουσιαστικά[ν])
				
	def ουσιαστικά_διαγραφή(self, αναγνώριση):
		ουσιαστικά = []
		self.sql.ουσιαστικά.διαγραφή(αναγνώριση, ουσιαστικά, self.δ["μεταδεδομένα"], self.δ["κλίμακες"],
								self.δ["κατηγοριοτονισμoί"]["ουσιαστικό"])
		δείκτης_θ = 0
		δείκτης_ο = 0
		μήκος_ο = len(ουσιαστικά)
		while δείκτης_θ < len(self.δ["θέματα"]) and δείκτης_ο < μήκος_ο:
			if self.δ["θέματα"][δείκτης_θ]:
				if self.δ["θέματα"][δείκτης_θ]["μέρος του λόγου"] == "ουσιαστικό":
					self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
					δείκτης_ο += 1
			else:
				self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
				δείκτης_ο += 1
			δείκτης_θ += 1
		if δείκτης_θ == len(self.δ["θέματα"]):
			for ν in range(δείκτης_ο, μήκος_ο):
				self.δ["θέματα"].append(ουσιαστικά[ν])
	
	def ουσιαστικά_τρέχον(self, αναγνώριση):
		ουσιαστικά = []
		self.sql.ουσιαστικά.τρέχον(αναγνώριση, ουσιαστικά, self.δ["μεταδεδομένα"], self.δ["κλίμακες"],
								self.δ["κατηγοριοτονισμoί"]["ουσιαστικό"])
		δείκτης_θ = 0
		δείκτης_ο = 0
		μήκος_ο = len(ουσιαστικά)
		while δείκτης_θ < len(self.δ["θέματα"]) and δείκτης_ο < μήκος_ο:
			if self.δ["θέματα"][δείκτης_θ]:
				if self.δ["θέματα"][δείκτης_θ]["μέρος του λόγου"] == "ουσιαστικό":
					self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
					δείκτης_ο += 1
			else:
				self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
				δείκτης_ο += 1
			δείκτης_θ += 1
		if δείκτης_θ == len(self.δ["θέματα"]):
			for ν in range(δείκτης_ο, μήκος_ο):
				self.δ["θέματα"].append(ουσιαστικά[ν])
				
	def επίθετα_φόρτωση(self, όλα=False):
		if όλα:
			ουσιαστικά = []
			κατηγοριοτονισμoί = {}
			self.sql.επίθετα.φόρτωση(ουσιαστικά, self.δ["μεταδεδομένα"], self.δ["κλίμακες"],
				κατηγοριοτονισμoί, self.δ["καταλήξεις"]["επίθετο"], self.δ["τονισμοί"]["επίθετο"], 
				self.δ["διάλεκτοι"], True)
			return [ουσιαστικά, κατηγοριοτονισμoί]
		else:
			self.sql.επίθετα.φόρτωση(self.δ["επίθετα"], self.δ["μεταδεδομένα"],
				self.δ["κλίμακες"], self.δ["κατηγοριοτονισμoί"]["επίθετο"],
				self.δ["καταλήξεις"]["επίθετο"], self.δ["τονισμοί"]["επίθετο"], self.δ["διάλεκτοι"])
	
	def επίθετα_ιστορικό(self, αναγνώριση):
		return self.sql.επίθετα.ιστορικό(αναγνώριση, self.δ["μεταδεδομένα"], self.δ["κλίμακες"])
	
	def επίθετο_νέο(self, αναγνώριση):
		self.sql.μεταδεδομένα.νέα(αναγνώριση, self.δ["μεταδεδομένα"])
		self.sql.κλίμακες.νέα(αναγνώριση, self.δ["κλίμακες"])
		ουσιαστικά = []
		self.sql.επίθετα.νέα(αναγνώριση, ουσιαστικά, self.δ["μεταδεδομένα"], self.δ["κλίμακες"],
								self.δ["κατηγοριοτονισμoί"]["επίθετο"],
				self.δ["καταλήξεις"]["επίθετο"], self.δ["τονισμοί"]["επίθετο"], self.δ["διάλεκτοι"])
		δείκτης_θ = 0
		δείκτης_ο = 0
		μήκος_ο = len(ουσιαστικά)
		while δείκτης_θ < len(self.δ["θέματα"]) and δείκτης_ο < μήκος_ο:
			if self.δ["θέματα"][δείκτης_θ]:
				if self.δ["θέματα"][δείκτης_θ]["μέρος του λόγου"] == "επίθετο":
					self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
					δείκτης_ο += 1
			else:
				self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
				δείκτης_ο += 1
			δείκτης_θ += 1
		if δείκτης_θ == len(self.δ["θέματα"]):
			for ν in range(δείκτης_ο, μήκος_ο):
				self.δ["θέματα"].append(ουσιαστικά[ν])
				
	def επίθετα_διαγραφή(self, αναγνώριση):
		ουσιαστικά = []
		self.sql.επίθετα.διαγραφή(αναγνώριση, ουσιαστικά, self.δ["μεταδεδομένα"], self.δ["κλίμακες"],
								self.δ["κατηγοριοτονισμoί"]["επίθετο"])
		δείκτης_θ = 0
		δείκτης_ο = 0
		μήκος_ο = len(ουσιαστικά)
		while δείκτης_θ < len(self.δ["θέματα"]) and δείκτης_ο < μήκος_ο:
			if self.δ["θέματα"][δείκτης_θ]:
				if self.δ["θέματα"][δείκτης_θ]["μέρος του λόγου"] == "επίθετο":
					self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
					δείκτης_ο += 1
			else:
				self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
				δείκτης_ο += 1
			δείκτης_θ += 1
		if δείκτης_θ == len(self.δ["θέματα"]):
			for ν in range(δείκτης_ο, μήκος_ο):
				self.δ["θέματα"].append(ουσιαστικά[ν])
	
	def επίθετα_τρέχον(self, αναγνώριση):
		ουσιαστικά = []
		self.sql.επίθετα.τρέχον(αναγνώριση, ουσιαστικά, self.δ["μεταδεδομένα"], self.δ["κλίμακες"],
								self.δ["κατηγοριοτονισμoί"]["επίθετο"])
		δείκτης_θ = 0
		δείκτης_ο = 0
		μήκος_ο = len(ουσιαστικά)
		while δείκτης_θ < len(self.δ["θέματα"]) and δείκτης_ο < μήκος_ο:
			if self.δ["θέματα"][δείκτης_θ]:
				if self.δ["θέματα"][δείκτης_θ]["μέρος του λόγου"] == "επίθετο":
					self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
					δείκτης_ο += 1
			else:
				self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
				δείκτης_ο += 1
			δείκτης_θ += 1
		if δείκτης_θ == len(self.δ["θέματα"]):
			for ν in range(δείκτης_ο, μήκος_ο):
				self.δ["θέματα"].append(ουσιαστικά[ν])
	
	def κατηγοροτονισμοί_φόρτωση(self, όλα=False):
		if όλα:
			ανώμαλα = {"ρήμα":{}, "μετοχή":{}}
			self.sql.κατηγοριοτονισμοί.φόρτωση(ανώμαλα, self.δ["καταλήξεις"], self.δ["τονισμοί"], True)
			return ανώμαλα
		else:
			self.sql.κατηγοριοτονισμοί.φόρτωση(self.δ["κατηγοριοτονισμoί"], self.δ["καταλήξεις"], self.δ["τονισμοί"])
	
	def κατηγοροτονισμοί_ιστορικό(self, αναγνώριση):
		return self.sql.κατηγοριοτονισμοί.ιστορικό(αναγνώριση)
	
	def ρήματα_φόρτωση(self, όλα=False):
		if όλα:
			θέματα = []
			#self.δ["ομάδες"] = {"ρήμα":{}, "μετοχή":{}}
			#self.sql.ομάδες.φόρτωση(self.δ["ομάδες"], self.δ["κατηγοριοτονισμoί"])
			self.sql.θέματα.φόρτωση(θέματα, self.δ["μεταδεδομένα"],
				self.δ["κλίμακες"], self.δ["ομάδες"], self.δ["διάλεκτοι"], True)
			return [θέματα, self.δ["ομάδες"]]
		else:
			#ομάδα = {"ρήμα":{}, "μετοχή":{}}
			#self.sql.ομάδες.φόρτωση(ομάδα, self.δ["κατηγοριοτονισμoί"])
			self.sql.θέματα.φόρτωση(self.δ["θέματα"], self.δ["μεταδεδομένα"],
				self.δ["κλίμακες"], self.δ["ομάδες"], self.δ["διάλεκτοι"])
	
	def ρήματα_ιστορικό(self, αναγνώριση):
		return self.sql.θέματα.ιστορικό(αναγνώριση, self.δ["μεταδεδομένα"], self.δ["κλίμακες"], self.δ["ομάδες"])
	
	def ρήματα_νέο(self, αναγνώριση):
		self.sql.μεταδεδομένα.νέα(αναγνώριση, self.δ["μεταδεδομένα"])
		self.sql.κλίμακες.νέα(αναγνώριση, self.δ["κλίμακες"])
		ουσιαστικά = []
		θέματα = []
		self.sql.θέματα.νέα(αναγνώριση, θέματα, self.δ["μεταδεδομένα"],
				self.δ["κλίμακες"], self.δ["ομάδες"], self.δ["διάλεκτοι"])
	
	def κατηγοροτονισμοί_τρέχον(self, αναγνώριση):
		return self.sql.κατηγοριοτονισμοί.τρέχον(αναγνώριση, self.δ["κατηγοριοτονισμoί"], self.δ["καταλήξεις"], self.δ["τονισμοί"])
	
	def κατηγοροτονισμοί_διαγραφή(self, αναγνώριση):
		self.sql.κατηγοριοτονισμοί.διαγραφή(αναγνώριση, self.δ["κατηγοριοτονισμoί"], self.δ["καταλήξεις"], self.δ["τονισμοί"])
	
	def κατηγοροτονισμοί_νέο(self, αναγνώριση):
		self.sql.κατηγοριοτονισμοί.νέα(αναγνώριση, self.δ["κατηγοριοτονισμoί"], self.δ["καταλήξεις"], self.δ["τονισμοί"])
		
	def ομάδες_νέα(self, αναγνώριση):
		return self.sql.ομάδες.νέα(αναγνώριση, self.δ["ομάδες"], self.δ["κατηγοριοτονισμoί"])
	
	def ρήματα_τρέχον(self, αναγνώριση):
		ουσιαστικά = []
		self.sql.θέματα.τρέχον(αναγνώριση)
	
	def ρήματα_διαγραφή(self, αναγνώριση):
		ουσιαστικά = []
		self.sql.θέματα.διαγραφή(αναγνώριση)
#		δείκτης_θ = 0
#		δείκτης_ο = 0
#		μήκος_ο = len(ουσιαστικά)
#		while δείκτης_θ<len(self.δ["θέματα"]) and δείκτης_ο<μήκος_ο:
#			if self.δ["θέματα"][δείκτης_θ]:
#				if self.δ["θέματα"][δείκτης_θ]["μέρος του λόγου"]=="ρήμα":
#					self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
#					δείκτης_ο +=1
#			else:
#				self.δ["θέματα"][δείκτης_θ] = ουσιαστικά[δείκτης_ο]
#				δείκτης_ο +=1
#			δείκτης_θ += 1
#		if δείκτης_θ==len(self.δ["θέματα"]):
#			for ν in range(δείκτης_ο, μήκος_ο):
#				self.δ["θέματα"].append(ουσιαστικά[ν])
