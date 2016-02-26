#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, dimitriadis dimitris
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the dimitriadis dimitris nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
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
λίστα = list
μήκος = len
εύρος = range
ακέραιος = int
τίποτα = None
ναι = True
όχι = False

class Δοκιμές_Επιφωνημάτων():
	def __init__(self, γραμματική):
		self.αναγνώριση = γραμματική.αναγνώριση
		self.δεδομένα_αναγνώρισης = []

	def δοκιμές_αναγνώρισης(self):
		δεδομένα_αναγνώρισης = [
			["βαβαὶ",  "κοινή", "θαυμαστικά"],
			["παπαῖ",  "κοινή", "θαυμαστικά"],	["ἆ",      "κοινή", "θαυμαστικά"],
			["ὤ",      "κοινή", "θαυμαστικά"],	["ὦ",      "κοινή", "κλητικά"],
			["ἰώ",     "κοινή",   "σχετλιαστικά"],
			["ἰού",    "κοινή",   "σχετλιαστικά"], ["οὐαί",   "κοινή",   "σχετλιαστικά"],
			["οἴμοι",  "κοινή",   "σχετλιαστικά"], ["φεῦ",    "κοινή",   "σχετλιαστικά"],
			["παπαῖ",  "κοινή",   "σχετλιαστικά"],
			["ἆ",      "κοινή",   "εκπληκτικά"],
			["εὐὰν",     "κοινή",   "θειαστικά"],
			["εὐοῖ",     "κοινή",   "θειαστικά"],	["ἅ",        "κοινή",   "γελαστικά"],
			["ἆ",       "δημοτική",   "θαυμαστικά"],	["ποπό",    "δημοτική",   "θαυμαστικά"],
			["ὤ",       "δημοτική",   "θαυμαστικά"],	["μπά",     "δημοτική",   "θαυμαστικά"],
			["ἆ",       "δημοτική",   "απορία"],	["ὄ",       "δημοτική",   "απορία"],
			["μπά",     "δημοτική",   "απορία"],
			["ἄχ",      "δημοτική",   "πόνος"],	["ὄχ",      "δημοτική",   "πόνος"],
			["ἄου",     "δημοτική",   "πόνος"],	["ὤ",       "δημοτική",   "πόνος"],
			["ὄχου",    "δημοτική",   "λύπη"],	["ἀλί",     "δημοτική",   "λύπη"],
			["ἀλίμονο", "δημοτική",   "λύπη"],
			["ἔ",       "δημοτική",   "περίπαιγμα"],	["αχαχούχα","δημοτική",   "περίπαιγμα"],
			["οὖ",      "δημοτική",   "περίπαιγμα"],
			["Εἴθε",    "δημοτική",   "ευχή"],	["μακάρι",  "δημοτική",   "ευχή"],
			["ἄμποτε",  "δημοτική",   "ευχή"],
			["χμ",      "δημοτική",   "αβεβαιότητα"],
			["εὔγε",    "δημοτική",   "έπαινος"],	["μπράβο",  "δημοτική",   "έπαινος"],
			["ἔ",       "δημοτική",   "κάλεσμα"],	["ὤ",       "δημοτική",   "κάλεσμα"],
			["ἔ",       "δημοτική",   "ειρωνεία"],	["οὖ",      "δημοτική",   "ειρωνεία"],
			["ἔ",       "δημοτική",   "αηδία"],		["οὖ",      "δημοτική",   "αηδία"],
			["ποῦφ",    "δημοτική",   "αηδία"],
			["οὖφ",     "δημοτική",   "στενοχώρια"],	
			["ἄιντε",   "δημοτική",   "παρακίνηση"],	["ἄμε",     "δημοτική",   "παρακίνηση"],
			["μάρς",    "δημοτική",   "παρακίνηση"],	["ἄλτ",     "δημοτική",   "παρακίνηση"],
			["στόπ",    "δημοτική",   "παρακίνηση"],	["σούτ",    "δημοτική",   "παρακίνηση"],
			["στ",      "δημοτική",   "παρακίνηση"],	["ἀέρα",    "δημοτική",   "παρακίνηση"],
			# ["πά πά πά","δημοτική",   "στενοχώρια"],
			# ["ἄ μπά",   "δημοτική",   "άρνηση"],
			# ["οἷον εὐοῖ","κοινή",   "θειαστικά"],	
			# ["οἷον ἰώ","κοινή",   "σχετλιαστικά"],
			# ["οἷον ὤ", "κοινή", "θαυμαστικά"],	
			]
		μετρητής, αποτυχίες = 0, 0

		for σύνολο in δεδομένα_αναγνώρισης:
			αποτέλεσμα = self.αναγνώριση(σύνολο[0], σύνολο[1])
			if αποτέλεσμα:
				nfound = False
				for α in αποτέλεσμα:
					if α['μέρος του λόγου']=='επιφώνημα' and\
						σύνολο[2] in α["Μεταδεδομένα"]['ιδιότητες']:
						nfound = True
						break
				if not nfound:
					τύπωσε("   ΑΝΑΜΕΝΟΤΑΝ:",σύνολο,"ΑΠΟΤΕΛΕΣΜΑ:",  αποτέλεσμα)
					αποτυχίες += 1
			else:
				τύπωσε("   ΑΝΑΜΕΝΟΤΑΝ:",σύνολο,"ΧΩΡΙΣ ΑΠΟΤΕΛΕΣΜΑ:",  αποτέλεσμα)
				αποτυχίες += 1

			μετρητής += 1
		τύπωσε("Δοκιμές αναγνώρισης Επιφωνημάτων", "Δοκιμές:", μετρητής," Αποτυχίες:",αποτυχίες)

if __name__=="__main__":
	δπ = Δοκιμές_Επιφωνημάτων()
	δπ.δοκιμές_αναγνώρισης()