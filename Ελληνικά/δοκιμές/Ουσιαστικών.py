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

import os, sys, json

τύπωσε = print
κείμενο = str
λίστα = list
μήκος = len
εύρος = range
ακέραιος = int
τίποτα = None
ναι = True
όχι = False

class Δοκιμές_Ουσιαστικών():
	def __init__(self, γραμματική, δεδομένα):
		self.αριθμό_σε_αριθμό = {0:"ενικός", 1:"δυϊκός", 2:"πληθυντικός"}
		self.αριθμό_σε_πτώση = {0:"ονομαστική", 1:"γενική", 2:"δοτική", 3:"αιτιατική", 4:"κλητική"}
		self.ουσιαστικά = γραμματική.ουσιαστικά
		self.αναγνώριση = γραμματική.αναγνώριση
		self.δεδομένα = δεδομένα.κ["ουσιαστικό"]

	def δοκιμές_κλίσης(self):
		αποτυχίες, δοκιμασμένα = 0, 0
		for διάλεκτος, λέξεις in self.δεδομένα.items():
			
			λέξεις = list(λέξεις.keys())
			λέξεις.sort()
			for λέξη in λέξεις:
				δείκτης_αριθμού = 0
				for αριθμός in ["ενικός", "δυϊκός", "πληθυντικός"]:
					δείκτης_πτώσης = 0
					for πτώση in ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]:
						αποτελέσματα = self.ουσιαστικά.κλίνε(λέξη, αριθμός, πτώση, διάλεκτος)
						αναμενόμενο =  self.δεδομένα[διάλεκτος][λέξη][δείκτης_αριθμού*5+δείκτης_πτώσης]

						OK = False
						for a in αναμενόμενο:
							if a and αποτελέσματα and a not in αποτελέσματα:
								OK = True
						if OK or (αναμενόμενο and not αποτελέσματα):
							τύπωσε( λέξη, αριθμός, πτώση, διάλεκτος)
							τύπωσε( "ΑΠΟΤΕΛΕΣΜΑ:", αποτελέσματα, "   ΑΝΑΜΕΝΟΤΑΝ:", αναμενόμενο)
							αποτυχίες += 1
						δοκιμασμένα += 1
						δείκτης_πτώσης += 1
					δείκτης_αριθμού += 1
		τύπωσε("Δοκιμές κλίσης Ουσιαστικῶν", "Δοκιμές:",δοκιμασμένα," Αποτυχίες:", αποτυχίες)
		return αποτυχίες

	def δοκιμές_αναγνώρισης(self):
		μετρητής, αποτυχίες = 0, 0
		for διάλεκτος, λέξεις in self.δεδομένα.items():
			έξεις = list(λέξεις.keys())
			έξεις.sort()
			
			for λέξη in έξεις:
				καταλήξεις = λέξεις[λέξη]
				σύνολο = { "διάλεκτος":διάλεκτος,}
				
				for ααριθμό in [0,5,10]:
					νέες_καταλήξεις = {}
					αριθμός = self.αριθμό_σε_αριθμό[ααριθμό // 5]
					
					for ν in range(5):
						κατάληξη = καταλήξεις[ααριθμό+ν]
						πτώση   = self.αριθμό_σε_πτώση[ν % 5]
						
						for υποκατάληξη in κατάληξη:
							if υποκατάληξη in νέες_καταλήξεις:
								νέες_καταλήξεις[υποκατάληξη]['πτώση'].append(πτώση)
							else:
								υποσύνολο = σύνολο.copy()
								
								υποσύνολο["αριθμός"] = αριθμός
								υποσύνολο["πτώση"] = [πτώση]
								νέες_καταλήξεις[υποκατάληξη] = υποσύνολο

					for υποκατάληξη, υποσύνολο in νέες_καταλήξεις.items():
						υποσύνολο['πτώση'].sort()
						if len(υποσύνολο['πτώση'])==5:
							del υποσύνολο['πτώση']
							del υποσύνολο['αριθμός']
						αποτελέσματα = self.αναγνώριση(υποκατάληξη, διάλεκτος)
	
						αστοχίες_list = []
						for αποτέλεσμα in αποτελέσματα:
							if αποτέλεσμα["μέρος του λόγου"]!="ουσιαστικό" or\
								αποτέλεσμα["διάλεκτος"]!=διάλεκτος:
								continue
							αστοχίες = self.__σύγκριση_λεξικών(υποσύνολο, αποτέλεσμα, υποκατάληξη)
							if αστοχίες:
								αστοχίες_list.append(αστοχίες)
							else:
								αστοχίες_list.append("Επιτυχία")
						μετρητής += 1
						if not "Επιτυχία" in αστοχίες_list:
							αποτυχίες += 1
							if αποτυχίες>100:
								continue
							if 'πτώση' in υποσύνολο:
								print(λέξη, υποκατάληξη, διάλεκτος, υποσύνολο['αριθμός'], υποσύνολο['πτώση'], αποτελέσματα)
							else:
								print(λέξη, υποκατάληξη, διάλεκτος, αποτελέσματα)
							for αστοχία in αστοχίες_list:
								for k,v in αστοχία.items():
									τύπωσε(k,"   ΑΝΑΜΕΝΟΤΑΝ:",v[0],"ΑΠΟΤΕΛΕΣΜΑ:",  v[1])
								print()
							
		τύπωσε("Δοκιμές αναγνώρισης Ουσιαστικῶν", "Δοκιμές:", μετρητής," Αποτυχίες:",αποτυχίες)
		return αποτυχίες

	def __σύγκριση_λεξικών(self, λεξικό, αποτέλεσμα, λέξη):
		αστοχίες = {}
		for k,v in λεξικό.items():
			if k not in αποτέλεσμα:
				if not αποτέλεσμα.get('κατηγορία') and\
					k in ['αριθμός', 'πτώση']:
					pass
				else:
					αστοχίες[k] = [v, 'Τίποτα']
			elif k in ['αριθμός', 'πτώση'] and αποτέλεσμα[k]==None:
				pass
			elif k in ['αριθμός', 'πτώση']:
				pass
			else:
				if v!=αποτέλεσμα[k]:
					αστοχίες[k] = [v, αποτέλεσμα[k]]
		
		return αστοχίες

	def _επαλήθευση_λεξικού(self):
		"Ελέγχει αν όλο το λεξικό μπορεί να αναγνωριστεί και κλιθεί."
		self.δεδομένα.clear()
		self.δεδομένα["δημοτική"] = {}
		self.δεδομένα["κοινή"] = {}
		τΚατηγορίες = {"δημοτική":[], "κοινή":[]}
		τΔεδομένα = {"δημοτική":{}, "κοινή":{}}
		for λήμμα, διάλεκτοι in self.ουσιαστικά.δ.λήμματα.items():
			κΛήμμα = self.ουσιαστικά.τ.κωδικοποιητής(λήμμα)
			for διάλεκτος, κατηγορίες in διάλεκτοι.items():
				if διάλεκτος!="συχνότητα":
					for κατηγορία in κατηγορίες:
						αρχικό, νέα_δεδομένα = None, []
						for αριθμός in ["ενικός", "δυϊκός", "πληθυντικός"]:
							for πτώση in ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]:
								αποτέλεσμα = self.ουσιαστικά._κλίνε(κΛήμμα, κατηγορία, αριθμός, πτώση, διάλεκτος)
								if not αρχικό and αποτέλεσμα:
									αρχικό = self.ουσιαστικά.τ.απόκωδικοποιητής(αποτέλεσμα[0])
								ν = 0
								for α in αποτέλεσμα:
									αποτέλεσμα[ν] = self.ουσιαστικά.τ.απόκωδικοποιητής(αποτέλεσμα[ν])
									ν += 1 
								νέα_δεδομένα.append(αποτέλεσμα)
						if κατηγορία not in τΚατηγορίες[διάλεκτος]:
							τΚατηγορίες[διάλεκτος].append(κατηγορία)
							τΔεδομένα[διάλεκτος][αρχικό] = νέα_δεδομένα
						self.δεδομένα[διάλεκτος][αρχικό] = νέα_δεδομένα
		
		for διάλεκτος, κατηγορίες in self.ουσιαστικά.δ.ανώμαλα.items():
			if διάλεκτος!="συχνότητα":
				for κατηγορία in κατηγορίες:
					αρχικό, νέα_δεδομένα = None, []
					
					νέα_δεδομένα = κατηγορίες[κατηγορία]['καταλήξεις']
					if not αρχικό and νέα_δεδομένα:
						αρχικό = νέα_δεδομένα[0][0]
					
					if κατηγορία not in τΚατηγορίες[διάλεκτος]:
						τΚατηγορίες[διάλεκτος].append(κατηγορία)
						τΔεδομένα[διάλεκτος][αρχικό] = νέα_δεδομένα
					self.δεδομένα[διάλεκτος][αρχικό] = νέα_δεδομένα
		
		αποτυχίες = self.δοκιμές_αναγνώρισης()
		αποτυχίες += self.δοκιμές_κλίσης()
		self.φόρτωση_δοκιμών()
		αποτυχίες += self.δοκιμές_αναγνώρισης()
		αποτυχίες += self.δοκιμές_κλίσης()
		
		if not αποτυχίες:
			νέα = self.δεδομένα.copy()
			
			αποθήκευση = False
			for διάλεκτος, λέξεις in τΔεδομένα.items():
				for λέξη, καταλήξεις in λέξεις.items():
					if λέξη not in νέα[διάλεκτος]:
						νέα[διάλεκτος][λέξη] = καταλήξεις
						αποθήκευση = True
			
			if αποθήκευση:
				κείμενο = 'δοκιμές = {\n'
				διάλεκτοι = list(λεξικό.keys())
				διάλεκτοι.sort()
				for διάλεκτος in διάλεκτοι:
					κείμενο += '\t"'+διάλεκτος+'": { \n'
					κατηγορίες = list(λεξικό[διάλεκτος].keys())
					κατηγορίες.sort()
					for κατηγορία in κατηγορίες:
						καταλήξεις = λεξικό[διάλεκτος][κατηγορία]
						κείμενο += '\t\t'+('%12s' % ('"'+str(κατηγορία)+'"'))+': '
						κείμενο += str(καταλήξεις).replace("'", '"')+",\n"
					κείμενο = κείμενο[:-2]+'},\n'
				κείμενο = κείμενο[:-2]+'\n}\n//=\n'
				
				αρχείο = open('ουσιαστικῶν.js','w')
				αρχείο.write(κείμενο)
				αρχείο.close()
		
if __name__=="__main__":
	δο = Δοκιμές_Ουσιαστικών()
	δο._επαλήθευση_λεξικού()
