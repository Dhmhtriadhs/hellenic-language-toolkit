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
τύπωσε=print

class Δοκιμές_Μετοχῶν():
	def __init__(self, γραμματική, δεδομένα):
		self.γραμματική = γραμματική
		self.μετοχές = γραμματική.μετοχές
		self.αναγνώριση = γραμματική.αναγνώριση
		self.δεδομένα = δεδομένα.κ["μετοχή"]
		self._μεταβλητές()
		self._αναγνωρίσεις()
		
	def _μεταβλητές(self):
		self.αριθμό_σε_πτώση  = { 0:"ονομαστική",   1:"γενική",   2:"δοτική",   3:"αιτιατική",   4:"κλητική"   }
		self.αριθμό_σε_αριθμό = { 0:"ενικός",   1:"δυϊκός",   2:"πληθυντικός"    }
		self.λεξικό_αναγνώρισης = {}
			
	def _αναγνωρίσεις(self):
		self.λεξικό_αναγνώρισης.clear()
		for διάλεκτος, λήμματα in self.δεδομένα.items():
			if not λήμματα:
				continue
			self.λεξικό_αναγνώρισης[διάλεκτος] = {}
			rtemp = {}
			for λήμμα, γένη in λήμματα.items():
				for γένος in γένη:
					for ααριθμός in [0,1,2]:
						ttmp = {}
						αριθμός = self.αριθμό_σε_αριθμό[ααριθμός]
						for απτώση in range(5):
							πτώση = self.αριθμό_σε_πτώση[απτώση]
							καταλήξεις = γένη[γένος][ααριθμός*5+απτώση]
							for υποκατάληξη in καταλήξεις:
								if not υποκατάληξη in ttmp:
									κλέξη = self.μετοχές.τ.κωδικοποιητής(υποκατάληξη)
									self.μετοχές.τ.αφαίρεσε_τόνους(κλέξη)
									αλέξη = self.μετοχές.τ.απο(κλέξη, True)
									υποσύνολο = {
										"διάλεκτος":διάλεκτος,
										"αριθμός":self.αριθμό_σε_αριθμό[ααριθμός],
										"πτώση":[πτώση],
										"γένος":γένος,
										"αλέξη":αλέξη}
									ttmp[υποκατάληξη] = υποσύνολο
								else:
									ttmp[υποκατάληξη]["πτώση"].append(πτώση)
									ttmp[υποκατάληξη]["πτώση"].sort()
						for k,v in ttmp.items():
							if not k in rtemp:
								rtemp[k] = [v]
							else:
								rtemp[k].append(v)
			self.λεξικό_αναγνώρισης[διάλεκτος] = rtemp
								
	def δοκιμές_αναγνώρισης(self):
		# Έλεγχος: διαλέκτου, αριθμού, πτώσης, γένους, λήμματος+κατάληξης, 
		μετρητής, αποτυχίες = 0, 0
		
		for διάλεκτος, λέξεις in self.λεξικό_αναγνώρισης.items():
			for λέξη, δεδομένα in λέξεις.items():
				
				αποτελέσματα = self.αναγνώριση(λέξη, διάλεκτος)
				αστοχίες_list = []
				
				for δεδομένο in δεδομένα:
					αστοχίες_list = [] 
					for αποτέλεσμα in αποτελέσματα:
						if αποτέλεσμα["μέρος του λόγου"]!="μετοχή":
							continue
						αστοχίες = self.__σύγκριση_λεξικών(δεδομένο, αποτέλεσμα, λέξη)
						if not αστοχίες:
							αστοχίες_list = []
							break
						else:
							αστοχίες_list.append(αστοχίες)
					
				if αστοχίες_list:
					print(λέξη, διάλεκτος)
					for αστοχία in αστοχίες_list:
						for k,v in αστοχία.items():
							print(k,"   ΑΝΑΜΕΝΟΤΑΝ:",v[0],"ΑΠΟΤΕΛΕΣΜΑ:",  v[1])
						print()
					αποτυχίες += 1
				μετρητής += 1
						
		print("Δοκιμές αναγνώρισης Μετοχῶν","Δοκιμές:", μετρητής," Αποτυχίες:",αποτυχίες)
		return αποτυχίες

	def __σύγκριση_λεξικών(self, λεξικό, αποτέλεσμα, λέξη):
		αστοχίες = {}

		for k,v in λεξικό.items():
			if k=="αλέξη":
				if "ανώμαλο" in αποτέλεσμα:
					continue
				if not v.endswith(αποτέλεσμα['κατάληξη']):
					αστοχίες[k] = [v, αποτέλεσμα['κατάληξη']+"1"]
				if αποτέλεσμα.get('θέμα','') not in v:
					αστοχίες[k] = [v, αποτέλεσμα['θέμα']]
			elif not k in αποτέλεσμα:
				αστοχίες[k] = [v, 'Τίποτα']
			else:
				if v!=αποτέλεσμα[k]:
					αστοχίες[k] = [v, αποτέλεσμα[k]]

		return αστοχίες
	
	def δοκιμές_κλίσης(self):
		δοκιμασμένα = 0
		αποτυχίες = 0
		for διάλεκτος, λέξεις in self.δεδομένα.items():
			λέξεις = list(λέξεις.keys())
			λέξεις.sort()
			for λέξη in λέξεις:
				for γένος in ['αρσενικό','θηλυκό','ουδέτερο']:
					δείκτης_αριθμού = 0
					for αριθμός in ['ενικός','δυϊκός','πληθυντικός']:
						δείκτης_πτώσης = 0
						for πτώση in ['ονομαστική','γενική','δοτική','αιτιατική','κλητική']:
							αποτελέσματα = self.μετοχές.κλίνε(λέξη, αριθμός, πτώση, γένος, διάλεκτος=διάλεκτος)
							αναμενόμενο =  self.δεδομένα[διάλεκτος][λέξη][γένος][δείκτης_αριθμού*5+δείκτης_πτώσης]
							if αποτελέσματα:
								OK = False
								for a in αναμενόμενο:
									if a not in αποτελέσματα:
										OK = True
										break

								if OK:
									print( λέξη, διάλεκτος, γένος, αριθμός, πτώση)
									print( "ΑΠΟΤΕΛΕΣΜΑ:", αποτελέσματα, "   ΑΝΑΜΕΝΟΤΑΝ:", αναμενόμενο)
									αποτυχίες += 1
								δοκιμασμένα += 1
							elif αναμενόμενο:
								print(λέξη, "ΑΠΟΤΕΛΕΣΜΑ:", αποτελέσματα,"   ΑΝΑΜΕΝΟΤΑΝ:",αναμενόμενο, αριθμός, πτώση, γένος, διάλεκτος)
								αποτυχίες += 1
								δοκιμασμένα += 1
							δείκτης_πτώσης += 1
						δείκτης_αριθμού += 1
		print("Δοκιμές κλίσης Μετοχῶν", "Δοκιμές:",δοκιμασμένα," Αποτυχίες:", αποτυχίες)
		return αποτυχίες
