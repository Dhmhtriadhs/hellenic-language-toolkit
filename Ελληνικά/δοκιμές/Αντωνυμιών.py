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

class Δοκιμές_Αντωνυμιών():
	def __init__(self, γραμματική, δεδομένα):
		self.αντωνυμίες = γραμματική.αντωνυμίες
		self.αναγνώριση = γραμματική.αναγνώριση
		self.δοκιμές = δεδομένα.κ["αντωνυμία"]

	def δοκιμές_κλίσης(self):
		δοκιμασμένα, αποτυχίες = 0, 0
		μετρητής, αποτυχίες = 0, 0
		for διάλεκτος, λέξεις in self.δοκιμές.items():
			for λέξη, σύνολα in λέξεις.items():
				for σύνολο in σύνολα:
					αριθμός = σύνολο.get("αριθμός")
					πτώση = σύνολο.get("πτώση")
					γένος = σύνολο.get("γένος")
					if not πτώση:
						πτώση = ["ονομαστική"]
					for πτω in πτώση:
						αποτελέσματα = []
						πρόσωπο, τύπος, κτήτορες = None, None, None
						if σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="προσωπική":
							πρόσωπο = σύνολο["πρόσωπο"]
							τύπος = σύνολο["Μεταδεδομένα"]["τύπος"][0]
							αποτελέσματα = self.αντωνυμίες.προσωπικές(αριθμός, πτω, πρόσωπο, διάλεκτος, γένος, τύπος)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="δεικτική":
							αποτελέσματα = self.αντωνυμίες.δεικτικές(αριθμός, πτω, διάλεκτος, γένος, λέξη)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="οριστική":
							αποτελέσματα = self.αντωνυμίες.οριστικές(αριθμός, πτω, διάλεκτος, γένος)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="κτητική":
							if "κτήτορες" in σύνολο["Μεταδεδομένα"]:
								κτήτορες = σύνολο["Μεταδεδομένα"]["κτήτορες"][0]
							πρόσωπο = σύνολο["πρόσωπο"]
							αποτελέσματα = self.αντωνυμίες.κτητικές(αριθμός, πτω, πρόσωπο, διάλεκτος, γένος, κτήτορες)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="αυτοπαθής":
							πρόσωπο = σύνολο["πρόσωπο"]
							αποτελέσματα = self.αντωνυμίες.αυτοπαθής(αριθμός, πτω, πρόσωπο, διάλεκτος, γένος)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="αλληλοπαθητική":
							αποτελέσματα = self.αντωνυμίες.αλληλοπαθητικές(αριθμός, πτω, διάλεκτος, γένος)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="ερωτηματική":
							αποτελέσματα = self.αντωνυμίες.ερωτηματικές(αριθμός, πτω, διάλεκτος, γένος, λέξη)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="αόριστη":
							αποτελέσματα = self.αντωνυμίες.αόριστες(αριθμός, πτω, διάλεκτος, γένος, λέξη)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="επιμεριστική":
							αποτελέσματα = self.αντωνυμίες.επιμεριστικές(αριθμός, πτω, διάλεκτος, γένος, λέξη)
						elif σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"][0]=="αναφορική":
							αποτελέσματα = self.αντωνυμίες.αναφορικές(αριθμός, πτω, διάλεκτος, γένος, λέξη)
						else:
							continue
							
						if λέξη not in αποτελέσματα or not αποτελέσματα:
							τύπωσε(λέξη, διάλεκτος, σύνολο["Μεταδεδομένα"]["τύπος αντωνυμίας"],αριθμός, πτώση, γένος, πρόσωπο, τύπος)
							τύπωσε( "ΑΠΟΤΕΛΕΣΜΑ:", αποτελέσματα, "   ΑΝΑΜΕΝΟΤΑΝ:", σύνολο)
							αποτυχίες += 1
						δοκιμασμένα += 1

		τύπωσε("Δοκιμές κλίσης Αντωνυμιών", "Δοκιμές:",δοκιμασμένα," Αποτυχίες:", αποτυχίες)

	def δοκιμές_αναγνώρισης(self):
		μετρητής, αποτυχίες = 0, 0
		for διάλεκτος, λέξεις in self.δοκιμές.items():
			for λέξη, σύνολα in λέξεις.items():
				
				αστοχίες_list = []
				αποτελέσματα = self.αναγνώριση(λέξη, διάλεκτος)
				
				if not αποτελέσματα:
					τύπωσε(λέξη, "ΧΩΡΙΣ ΑΠΟΤΕΛΕΣΜΑΤΑ", σύνολο)
					αποτυχίες += 1
					μετρητής += 1
					continue
				
				fc = [0,0]
				αστοχίες_list = []
				for σύνολο in σύνολα:
					fc[0]+=1
					for αποτέλεσμα in αποτελέσματα:
						if αποτέλεσμα["διάλεκτος"]!=διάλεκτος:
							continue
						
						αστοχίες = self.__σύγκριση_λεξικών(σύνολο, αποτέλεσμα)
						if not αστοχίες:
							fc[1]+=1
						else:
							αστοχίες_list.append(αστοχίες)
						
				if fc[0]!=fc[1]:
					print(fc)
					τύπωσε(λέξη, σύνολο)
					τύπωσε(σύνολα)
					τύπωσε(αποτελέσματα)
					t=False
					for αστοχία in αστοχίες_list:
						for k,v in αστοχίες.items():
							τύπωσε(k,"   ΑΝΑΜΕΝΟΤΑΝ:",v[0],"ΑΠΟΤΕΛΕΣΜΑ:",  '"'+str(v[1])+'"')
							t=True
							break
						if t:
							break
						#print()
					αποτυχίες += 1
				μετρητής += 1

		τύπωσε("Δοκιμές αναγνώρισης Αντωνυμιών", "Δοκιμές:", μετρητής," Αποτυχίες:",αποτυχίες)
		
	def __σύγκριση_λεξικών(self, λεξικό, αποτέλεσμα):
		αστοχίες = {}

		for k,v in λεξικό.items():
			if k in ["κατηγορία", 'κΚατάληξη', 'ανώμαλο']:
				continue
			if k=="γένος" and not αποτέλεσμα.get("γένος"):
				pass
			elif k not in αποτέλεσμα:
				αστοχίες[k] = [v, 'Τίποτα']
			else:
				if v!=αποτέλεσμα[k]:
					αστοχίες[k] = [v, αποτέλεσμα[k]]
		
		return αστοχίες
