#!/usr/bin/python3.2
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

class Άρθρα():
	"""Κλίνει και αναγνωρίζει τα άρθρα μαζί με τις ιδιότητες τους"""
	def __init__(self, τονιστής, δεδομένα, αναγνώριση):
		self.τ = τονιστής
		self.αναγνώριση = αναγνώριση
		self.δεδομένα = δεδομένα
		self.πτώση_σε_αριθμό = {"ονομαστική":0, "γενική":1, "δοτική":2, "αιτιατική":3, "κλητική":4}
		self.αριθμό_σε_πτώση = {0:"ονομαστική", 1:"γενική", 2:"δοτική", 3:"αιτιατική", 4:"κλητική"}
		self.αριθμοί = {"ενικός":0, "δυϊκός":5, "πληθυντικός":10}
		self.αριθμό_σε_αριθμό = {0:"ενικός", 1:"δυϊκός", 2:"πληθυντικός"}
		self.γένος_σε_αριθμό = {"αρσενικό":0, "θηλυκό":1, "ουδέτερο":2}
		self.αριθμό_σε_γένος = {0:"αρσενικό", 1:"θηλυκό", 2:"ουδέτερο"}

		self.γένη = self.γένος_σε_αριθμό.keys()
		self.πτώσεις = self.πτώση_σε_αριθμό.keys()
											
	def _πλήρη_κλίση(self, αναγνώριση):
		"""Κλίνει πλήρως το άρθρο.
		
		Επιστρέφη το άρθρο της αναγνώριση κλιμένο 
		σε όλους τους αριθμούς, πτώσεις και γένη.

		Μεταβλητές:
			αναγνώριση: Το αναγνωρισμένο άρθρο.

		Επιστρέφει:
		  Ένα λεξικό με άρθρα στην μορφή:
		  {"γένος":[["άρθρο ενικός ονομαστική1",], .... ["πληθυντικός κλητική1",]]}
		  Αν δεν είναι έγκηρες οι τιμές των μεταβητών,
		  επιστρέφει το λεξικό με τα γένη χωρίς άρθρα.
		"""
		αποτέλεσμα = {}
		διάλεκτος = αναγνώριση['διάλεκτος']
		for γένος in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
			αποτέλεσμα[γένος] = []
			for αριθμός in ["ενικός", "δυϊκός", "πληθυντικός"]:
				for πτώση in ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]:
					αποτέλεσμα[γένος].append(self.κλίνε(αριθμός, πτώση, γένος, διάλεκτος))
		return αποτέλεσμα
	
	def κλίνε(self, λέξη, αριθμός='ενικός', πτώση='ονομαστική', γένος='αρσενικό', διάλεκτος=None):
		"""Επιστρέφη άρθρα.

		Επιστρέφη άρθρα με βάση της λέξης, αριθμός, πτώση, γένος και διάλεκτο.

		Μεταβλητές:
			λέξη:      Άρθρο που αναγνωρίζεται.
			αριθμός:   Αποδεκτές τιμές "ενικός", "δυϊκός", "πληθυντικός".
			πτώση: 	  Αποδεκτές τιμές "ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική".
			γένος: 	  Αποδεκτές τιμές "αρσενικό",   "θηλυκό", "ουδέτερο".
			διάλεκτος: Αποδεκτές τιμές "κοινή", "δημοτική", "γερμανικά".

		Επιστρέφει:
		  Μία λίστα με ένα άρθρο.
		  Αν δεν είναι έγκηρες οι τιμές των μεταβητών,
		  επιστρέφει άδεια λίστα.
		"""
		
		αποτελέσματα = []
		
		if not (αριθμός in self.αριθμοί.keys() and πτώση in self.πτώσεις and\
			γένος in self.γένη and διάλεκτος in self.δεδομένα.δ["διάλεκτοι"] and\
			διάλεκτος in self.δεδομένα.δ["ανώμαλα"]["άρθρο"]):
			return αποτελέσματα
		
		θέση = self.αριθμοί[αριθμός] + self.πτώση_σε_αριθμό[πτώση]
		
		αναγνωρίσεις = self.αναγνώριση.αναγνώριση(λέξη, self.δεδομένα, διάλεκτος)
		self.αναγνώριση._φίλτρο_κατηγοριών(αναγνωρίσεις, "άρθρο", διάλεκτος)
		if αναγνωρίσεις:
			for αναγνώριση in αναγνωρίσεις:
				αποτελέσματα += self.δεδομένα.δ["ανώμαλα"]["άρθρο"][διάλεκτος][αναγνώριση["ΑΑ"]]['καταλήξεις'][γένος]['καταλήξεις'][θέση]
			
		return αποτελέσματα
			