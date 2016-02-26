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

class Δοκιμές_Άρθρων():
	def __init__(self, γραμματική):
		self.άρθρα = γραμματική.άρθρα
		self.αναγνώριση = γραμματική.αναγνώριση
		self.γένος_σε_αριθμό = {"αρσενικό":0, "θηλυκό":1, "ουδέτερο":2}
		self.αριθμοί = {"ενικός":0, "δυϊκός":5, "πληθυντικός":10}
		self.πτώση_σε_αριθμό = {"ονομαστική":0, "γενική":1, "δοτική":2, "αιτιατική":3, "κλητική":4}
		self.δεδομένα = {
				"κοινή":[
					[["ὁ"], ["τοῦ"], ["τῷ"], ["τὸν"], ["ὦ"], ["τὼ"], ["τοῖν"], ["τοῖν"], ["τὼ"], ["ὦ"], ["οἱ"], ["τῶν"], ["τοῖς"], ["τοὺς"], ["ὦ"]],
					[["ἡ"], ["τῆς"], ["τῇ"], ["τὴν"], ["ὦ"], ["τὰ"], ["ταῖν"], ["ταῖν"], ["τὰ"], ["ὦ"], ["αἱ"], ["τῶν"], ["ταῖς"], ["τὰς"], ["ὦ"]],
					[["τὸ"], ["τοῦ"], ["τῷ"], ["τὸ"], ["ὦ"], ["τὼ"], ["τοῖν"], ["τοῖν"], ["τὼ"], ["ὦ"], ["τὰ"], ["τῶν"], ["τοῖς"], ["τὰ"], ["ὦ"]]],
				"δημοτική":[
					[["ὁ"], ["τοῦ"], [], ["τὸν"], [], [], [], [], [], [], ["οἱ"], ["τῶν"], [], ["τοὺς"], []],
					[["ἡ"], ["τῆς"], [], ["τὴν"], [], [], [], [], [], [], ["οἱ"], ["τῶν"], [], ["τὶς"], []],
					[["τὸ"], ["τοῦ"], [], ["τὸ"], [], [], [], [], [], [], ["τὰ"], ["τῶν"], [], ["τὰ"], []]]}

	def δοκιμές_κλίσης(self):
		δοκιμασμένα, αποτυχίες = 0, 0
		for διάλεκτος, λέξεις in self.δεδομένα.items():
			for γένος in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
				for αριθμός in ["ενικός", "δυϊκός", "πληθυντικός"]:
					for πτώση in ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]:
						θέση1 = self.γένος_σε_αριθμό[γένος]
						θέση2 = self.αριθμοί[αριθμός]+self.πτώση_σε_αριθμό[πτώση]
						λέξη = λέξεις[θέση1][θέση2]
						
						αποτελέσματα = self.άρθρα.κλίνε(λέξεις[0][0], αριθμός, πτώση, γένος, διάλεκτος)
						
						if αποτελέσματα != λέξη:
							τύπωσε(αριθμός, πτώση, γένος, διάλεκτος)
							τύπωσε("ΑΠΟΤΕΛΕΣΜΑ:", αποτελέσματα, "   ΑΝΑΜΕΝΟΤΑΝ:", λέξη)
							αποτυχίες += 1
						δοκιμασμένα += 1
		τύπωσε("Δοκιμές κλίσης Άρθρων", "Δοκιμές:", δοκιμασμένα, " Αποτυχίες:", αποτυχίες)

	def δοκιμές_αναγνώρισης(self):
		μετρητής, αποτυχίες = 0, 0
		for διάλεκτος, λέξεις in self.δεδομένα.items():
			for γένος in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
				for αριθμός in ["ενικός", "δυϊκός", "πληθυντικός"]:
					
					σύνολα = {}
					for πτώση in ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]:
						θέση1 = self.γένος_σε_αριθμό[γένος]
						θέση2 = self.αριθμοί[αριθμός]+self.πτώση_σε_αριθμό[πτώση]
						λέξη = λέξεις[θέση1][θέση2]
						if not λέξη:
							continue
						for υλέξη in λέξη:
							if υλέξη in σύνολα:
								σύνολα[υλέξη]['πτώση'].append(πτώση)
								σύνολα[υλέξη]['πτώση'].sort()
							else:
								σύνολο = {'αριθμός': αριθμός, 'διάλεκτος': διάλεκτος, 
										'κατάληξη': υλέξη, 'γένος': γένος, 'πτώση': [πτώση], 
										'μέρος του λόγου': 'άρθρο'}
								σύνολα[υλέξη] = σύνολο
					
					for λέξη, σύνολο in σύνολα.items():
						αποτέλεσμα = self.αναγνώριση(λέξη, διάλεκτος)
						for α in αποτέλεσμα:
							αστοχίες = self.__σύγκριση_λεξικών(σύνολο, α)
							if not αστοχίες:
								break
						
						if not αποτέλεσμα:
							τύπωσε(λέξη, "   ΑΝΑΜΕΝΟΤΑΝ:", σύνολο, "ΑΠΟΤΕΛΕΣΜΑ:", αποτέλεσμα)
							αποτυχίες += 1
						elif αστοχίες:
							τύπωσε(λέξη, διάλεκτος, τύπο, γένος, αριθμός, σύνολο["πτώση"])
							for k,v in αστοχίες.items():
								τύπωσε(k, "   ΑΝΑΜΕΝΟΤΑΝ:", v[0], "ΑΠΟΤΕΛΕΣΜΑ:", v[1])
							αποτυχίες += 1
						
						μετρητής += 1
		τύπωσε("Δοκιμές αναγνώρισης Άρθρων", "Δοκιμές:", μετρητής, " Αποτυχίες:", αποτυχίες)
		
	def __σύγκριση_λεξικών(self, λεξικό, αποτέλεσμα):
		αστοχίες = {}
		if αποτέλεσμα["μέρος του λόγου"]!="άρθρο":
			return αστοχίες
		for k,v in λεξικό.items():
			if k not in αποτέλεσμα:
				αστοχίες[k] = [v, 'Τίποτα']
			else:
				if v!=αποτέλεσμα[k]:
					αστοχίες[k] = [v, αποτέλεσμα[k]]
		
		return αστοχίες
