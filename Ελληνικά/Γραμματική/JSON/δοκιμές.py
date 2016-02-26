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

import os, json
from multiprocessing import Process, Pipe
if 'Ελληνικά' in os.path.abspath('.').split("/")[-1]:
	φάκελος = os.path.join(".","Γραμματική")
elif 'δοκιμές' in os.path.abspath('.'):
	φάκελος = '..'
elif 'src' in os.path.abspath('.')[-3:]:
	φάκελος = 'Ελληνικά'
else:
	φάκελος = '.'
φάκελος = os.path.join(φάκελος, "Ελληνικά", "δεδομένα", "δοκιμές")
τύπωσε = print
κείμενο = str
μήκος = len
εύρος = range

class Δεδομένα():
	def __init__(self):
		# Tύποι Δεδομένων
		#
		# Λεξικό ρημάτων - αρχείο json:
		#  {διάλεκτος:
		#		θέμα:[{
		#				συχνότητα:         αριθμός,
		#				συνθετικό:         συνθετικό,
		#				αύξηση:            αύξηση,
		#           ενεστωτική αύξηση: αύξηση
		#				χρόνος: {καταλήξεις:[], τονισμοί:[]}},],
		#
		# η (κ)αύξηση είναι προαιρετική
		# η (κ)ενεστωτική αύξηση είναι προαιρετική
		# το (κ)συνθετικό είναι προαιρετικό
		#
		# self.θέματα:
		#  {διάλεκτος:[{
		#				συχνότητα: αριθμός,
		#				συνθετικό: συνθετικό,
		#				κΣυνθετικό: κΣυνθετικό,
		#				αύξηση:    αύξηση,
		#				κΑύξηση:    κΑύξηση,
		#				θέμα:     θέμα
		#           κΛέξη:   κΘέμα,
		#				ενεστωτική αύξηση: ενεστωτική αύξηση
		#				κΕνεστωτική αύξηση: κΕνεστωτική αύξηση
		#				χρόνος: {καταλήξεις:[], τονισμοί:[]}},],
		# η (κ)αύξηση είναι προαιρετική
		# η (κ)ενεστωτική αύξηση είναι προαιρετική
		# το (κ)συνθετικό είναι προαιρετικό
		#
		#
		# self.κατηγορίες:
		#  {διάλεκτος:
		#  	{χρόνος:
		#		   {κατηγορία:καταλήξεις}}}
		#
		# self.τονισμοί:
		#  {διάλεκτος:
		#		{κατηγορία:τονισμοί}}
		#
		# self.ανώμαλα
		#  {διάλεκτος:
		# 		[{χρόνος:
		#  		{φωνή:
		# 				{έγκλιση:
		#					{"καταλήξεις":καταλήξεις,
		#					 "κKαταλήξεις":κΚαταλήξεις,
		#					 "συχνότητες":συχνότητες}}}},},]}
		#  
		pass

	def φόρτωση(self, δεδομένα):
		for μέρος_του_λόγου in δεδομένα:
			δεδομένα[μέρος_του_λόγου].clear()
			if μέρος_του_λόγου=="ουσιαστικό":
				διαδρομή = os.path.join(φάκελος, 'ουσιαστικῶν.json')
			elif μέρος_του_λόγου=="επίθετο":
				διαδρομή = os.path.join(φάκελος, 'επίθετα.json')
			elif μέρος_του_λόγου=="ρήμα":
				διαδρομή = os.path.join(φάκελος, 'ρημάτων.json')
			elif μέρος_του_λόγου=="μετοχή":
				διαδρομή = os.path.join(φάκελος, 'μετοχῶν.json')
			elif μέρος_του_λόγου=="αντωνυμία":
				διαδρομή = os.path.join(φάκελος, 'αντωνυμίες.json')
			else:
				continue
			
			if os.path.exists(διαδρομή):
				αρχείο = open(διαδρομή, 'r', encoding='utf-8')
				json_κείμενο = αρχείο.read()
				αρχείο.close()
				json_αντικείμενο = json.loads(json_κείμενο, 'utf-8')
				δεδομένα[μέρος_του_λόγου].update(json_αντικείμενο)
			else:
				τύπωσε("Αποτυχία φόρτωση δοκιμών "+μέρος_του_λόγου+".\n",'To '+κείμενο(διαδρομή)+' δεν υπάρχει.')
	
	def φόρτωση_κατηγοριῶν(self, child_conn):
		κατηγορίες = {"ρήμα":{}, "μετοχή":{}, "επίθετο":{}, "ουσιαστικό":{}}
		self.__φόρτωση(os.path.join(φάκελος, 'κατηγορίες', "ρημάτων.json"), κατηγορίες["ρήμα"])
		self.__φόρτωση(os.path.join(φάκελος, 'κατηγορίες', "μετοχῶν.json"), κατηγορίες["μετοχή"])
		self.__φόρτωση(os.path.join(φάκελος, 'κατηγορίες', "επιθέτων.json"), κατηγορίες["επίθετο"])
		self.__φόρτωση(os.path.join(φάκελος, 'κατηγορίες', "ουσιαστικῶν.json"), κατηγορίες["ουσιαστικό"])
		self.__έλεγχος_κατηγοριών(κατηγορίες)
		child_conn.send(κατηγορίες)
		child_conn.close()
		
	def φόρτωση_τονισμῶν(self, child_conn):
		τονισμοί = {"ρήμα":{}, "επίθετο":{}, "ουσιαστικό":{}}
		self.__φόρτωση(os.path.join(φάκελος, 'τονισμοί', "ρημάτων.json"), τονισμοί["ρήμα"])
		self.__φόρτωση(os.path.join(φάκελος, 'τονισμοί', "επιθέτων.json"), τονισμοί["επίθετο"])
		self.__φόρτωση(os.path.join(φάκελος, 'τονισμοί', "ουσιαστικῶν.json"), τονισμοί["ουσιαστικό"])
		
		self.__έλεγχος_τόνων(τονισμοί)
		child_conn.send(τονισμοί)
		child_conn.close()
		
	def φόρτωση_θεμάτων(self, child_conn):
		θέματα = {}
		self.__φόρτωση_θεμάτων(os.path.join(φάκελος, 'λεξικά', "ρημάτων.json"), θέματα, "ρήμα", True)
		self.__φόρτωση_θεμάτων(os.path.join(φάκελος, 'λεξικά', "ουσιαστικῶν.json"), θέματα, "ουσιαστικό")
		self.__φόρτωση_θεμάτων(os.path.join(φάκελος, 'λεξικά', "επιθέτων.json"), θέματα, "επίθετο")
		
		μεταδεδομένα, κλίμακες = self.__έλεγχος_θεμάτων(θέματα)
		child_conn.send([θέματα, μεταδεδομένα, κλίμακες])
		child_conn.close()
		
	def φόρτωση_ανώμαλα(self, child_conn):
		ανώμαλα = {"ρήμα":{}, "επίθετο":{}, "ουσιαστικό":{},
			"επίρρημα":{}, "επιφώνημα":{}, "μόριο":{}, "πρόθεση":{}, "σύνδεσμος":{}, 
			"άρθρο":{},	"αντωνυμία":{}}
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "ρήματα.json"), ανώμαλα["ρήμα"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "ουσιαστικά.json"), ανώμαλα["ουσιαστικό"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "επίθετα.json"), ανώμαλα["επίθετο"])
		
		# ΑΚΛΗΤΑ
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "άρθρα.json"), ανώμαλα["άρθρο"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "επιρρήματα.json"), ανώμαλα["επίρρημα"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "αντωνυμίες.json"), ανώμαλα["αντωνυμία"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "επιφωνήματα.json"), ανώμαλα["επιφώνημα"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "μόρια.json"), ανώμαλα["μόριο"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "προθέσεις.json"), ανώμαλα["πρόθεση"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "σύνδεσμοι.json"), ανώμαλα["σύνδεσμος"])
		
		μεταδεδομένα, κλίμακες = self.__κωδικοποίηση_ανώμαλων(ανώμαλα)
		child_conn.send([ανώμαλα, μεταδεδομένα, κλίμακες])
		child_conn.close()
	
	def επαναφόρτωση(self):
		"""Επαναφόρτωση των κατηγοριών των ρημμάτων και των λημμάτων."""
		κparent_conn, κchild_conn = Pipe()
		τparent_conn, τchild_conn = Pipe()
		θparent_conn, θchild_conn = Pipe()
		αparent_conn, αchild_conn = Pipe()
		κ = Process(target=self.φόρτωση_κατηγοριῶν, args=(κchild_conn,))
		τ = Process(target=self.φόρτωση_τονισμῶν, args=(τchild_conn,))
		θ = Process(target=self.φόρτωση_θεμάτων, args=(θchild_conn,))
		α = Process(target=self.φόρτωση_ανώμαλα, args=(αchild_conn,))
		κ.start()
		τ.start()
		θ.start()
		α.start()
		self.κατηγορίες = κparent_conn.recv()
		self.τονισμοί = τparent_conn.recv()
		self.θέματα, μεταδεδομένα, κλίμακες = θparent_conn.recv()
		self.ανώμαλα, μεταδεδομένα2, κλίμακες2 = αparent_conn.recv()
		τ.join()
		κ.join()
		θ.join()
		α.join()
		#keys = self.μεταδεδομένα2.keys()
		#for key in keys:
		#	if key not in self.μεταδεδομένα:
		#		self.μεταδεδομένα[key] = []
		#	self.μεταδεδομένα[key] = list(set(μεταδεδομένα[key]+μεταδεδομένα2[key])) 
		self.κλίμακες = list(set(κλίμακες+κλίμακες2)) 
		
	def __κΚαταλήξεις(self, καταλήξεις):
		κΚαταλήξεις = []
		cac = {}
		for κατάληξη in καταλήξεις:
			υπο = []
			for υποκατάληξη in κατάληξη:
				if υποκατάληξη in cac:
					υπο.append(cac[υποκατάληξη])
				else:
					κωδ = self.τ.κωδικοποιητής(υποκατάληξη)
					υπο.append(κωδ)
					cac[υποκατάληξη] = κωδ
			κΚαταλήξεις.append(υπο)
		return κΚαταλήξεις
	
	def __κωδικοποίηση_ανώμαλων(self, ανώμαλα):
		μεταδεδομένα = {}
		κλίμακες = {}
		for μτλ, διάλεκτοι in ανώμαλα.items():
			for διάλεκτος, σύνολα in διάλεκτοι.items():
				αα = 0
				for σύνολο in σύνολα:
					if ανώμαλα[μτλ][διάλεκτος].__class__==list:
						if "μεταδεδομένα" in ανώμαλα[μτλ][διάλεκτος][αα]:
							for k in ανώμαλα[μτλ][διάλεκτος][αα]["μεταδεδομένα"]:
								if k not in μεταδεδομένα:
									μεταδεδομένα[k] = []
								for μστ in ανώμαλα[μτλ][διάλεκτος][αα]["μεταδεδομένα"][k]:
									if μστ not in μεταδεδομένα[k]:
										μεταδεδομένα[k].append(μστ)
						if "κλίμακες" in ανώμαλα[μτλ][διάλεκτος][αα]:
							for k in ανώμαλα[μτλ][διάλεκτος][αα]["κλίμακες"]:
								if k not in κλίμακες:
									κλίμακες = []
								#if ανώμαλα[μτλ][διάλεκτος][αα]["κλίμακες"][k] not in κλίμακες[k]:
								#	κλίμακες[k].append(ανώμαλα[μτλ][διάλεκτος][αα]["κλίμακες"][k])
					if μτλ in ["επιφώνημα", "μόριο", "σύνδεσμος", "πρόθεση", "επίρρημα"] and\
						not "κΛέξη" in σύνολο:
						κΛέξη = self.τ.κωδικοποιητής(σύνολο["λήμμα"])
						ανώμαλα[μτλ][διάλεκτος][αα]["κΛέξη"] = κΛέξη
					elif μτλ=="ρήμα":
						if "ρήμα" in σύνολο:
							for χρόνο, φωνές in σύνολο["ρήμα"].items():
								for φωνή, εγκλίσεις in φωνές.items():
									for έγκλιση, τιμές in εγκλίσεις.items():
										if "κΚαταλήξεις" in τιμές:
											continue
										ανώμαλα[μτλ][διάλεκτος][αα]["ρήμα"][χρόνο][φωνή][έγκλιση]["κΚαταλήξεις"] = self.__κΚαταλήξεις(τιμές["καταλήξεις"])
						if "μετοχή" in σύνολο:
							for χρόνο, φωνές in σύνολο["μετοχή"].items():
								for φωνή, γένη in φωνές.items():
									for γένος, τιμές in γένη.items():
										if "κΚαταλήξεις" in τιμές:
											continue
										ανώμαλα[μτλ][διάλεκτος][αα]["μετοχή"][χρόνο][φωνή][γένος]["κΚαταλήξεις"] = self.__κΚαταλήξεις(τιμές["καταλήξεις"])
					elif μτλ=="επίθετο":
						for γένος, τιμές in σύνολο.items():
							if γένος in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
								if "κΚαταλήξεις" in τιμές:
									continue
								ανώμαλα[μτλ][διάλεκτος][αα][γένος]["κΚαταλήξεις"] = self.__κΚαταλήξεις(τιμές["καταλήξεις"])
					elif μτλ=="ουσιαστικό" and not "κΚαταλήξεις" in σύνολο:
						ανώμαλα[μτλ][διάλεκτος][αα]["κΚαταλήξεις"] = self.__κΚαταλήξεις(σύνολο["καταλήξεις"])
					elif μτλ=="αντωνυμία":
						if "κατάληξη" in σύνολο:
							κΚατάληξη = self.τ.κωδικοποιητής(σύνολο["κατάληξη"])
							ανώμαλα[μτλ][διάλεκτος][αα]["κΚατάληξη"] = κΚατάληξη
						else:
							for γένος, τιμές in σύνολο.items():
								if γένος in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
									ανώμαλα[μτλ][διάλεκτος][αα][γένος]["κΚαταλήξεις"] = self.__κΚαταλήξεις(τιμές["καταλήξεις"])
								elif γένος in ["α", "β", "γ"]:
									for γένος2, τιμές2 in τιμές.items():
										if γένος2 in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
											ανώμαλα[μτλ][διάλεκτος][αα][γένος][γένος2]["κΚαταλήξεις"] = self.__κΚαταλήξεις(τιμές2["καταλήξεις"])
					elif μτλ=="άρθρο":
						γένος = σύνολο
						ανώμαλα[μτλ][διάλεκτος][γένος]["κΚαταλήξεις"] = self.__κΚαταλήξεις(σύνολα[γένος]["καταλήξεις"])
					αα += 1
		return μεταδεδομένα, κλίμακες
		
	def φόρτωση_άκλητα(self):
		αparent_conn, αchild_conn = Pipe()
		α = Process(target=self._φόρτωση_άκλητα, args=(αchild_conn,))
		α.start()
		self.ανώμαλα, self.μεταδεδομένα, self.κλίμακες = αparent_conn.recv()
		α.join()
		
	def _φόρτωση_άκλητα(self, child_conn):
		# ΑΚΛΗΤΑ
		ανώμαλα = {"άρθρο":{}, "αντωνυμία":{},
			"επίρρημα":{}, "επιφώνημα":{}, "μόριο":{}, "πρόθεση":{}, "σύνδεσμος":{}}
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "άρθρα.json"), ανώμαλα["άρθρο"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "επιρρήματα.json"), ανώμαλα["επίρρημα"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "αντωνυμίες.json"), ανώμαλα["αντωνυμία"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "επιφωνήματα.json"), ανώμαλα["επιφώνημα"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "μόρια.json"), ανώμαλα["μόριο"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "προθέσεις.json"), ανώμαλα["πρόθεση"])
		self.__φόρτωση(os.path.join(φάκελος, 'ανώμαλα', "σύνδεσμοι.json"), ανώμαλα["σύνδεσμος"])
		
		μεταδεδομένα, κλίμακες = self.__κωδικοποίηση_ανώμαλων(ανώμαλα)
		child_conn.send([ανώμαλα, μεταδεδομένα, κλίμακες])
		child_conn.close()
		
	def __φόρτωση(self, διαδρομή, μεταβλητή, clear=True):
		if clear:
			μεταβλητή.clear()
		
		if os.path.exists(διαδρομή):
			αρχείο = open(διαδρομή, 'r')
			δεδομένα = αρχείο.read()
			αρχείο.close()
			
			μεταβλητή.update(json.loads(δεδομένα, 'utf-8'))
		else:
			print('Το αρχείο %s δεν υπάρχει.' % διαδρομή)
			
	def __φόρτωση_θεμάτων(self, διαδρομή, μεταβλητή, όνομα, clear=False):
		if clear:
			μεταβλητή.clear()
			
		if os.path.exists(διαδρομή):
			αρχείο = open(διαδρομή, 'r')
			δεδομένα = json.loads(αρχείο.read(), 'utf-8')
			αρχείο.close()
			
			for διάλεκτο in δεδομένα:
				μέγεθος = len(δεδομένα[διάλεκτο])
				if διάλεκτο not in μεταβλητή:
					μεταβλητή[διάλεκτο] = []
				for ν in range(μέγεθος):
					δεδομένα[διάλεκτο][ν]["μέρος του λόγου"] = όνομα
					δεδομένα[διάλεκτο][ν]["διάλεκτος"] = διάλεκτο
					μεταβλητή[διάλεκτο].append(δεδομένα[διάλεκτο][ν])
		else:
			print('Το αρχείο %s δεν υπάρχει.' % διαδρομή)
			
	def __έλεγχος_κατηγοριών(self, κατηγορίες):
		for μτλ in ["ρήμα", "μετοχή"]:#, "επίθετο", "ουσιαστικό"]:
			map_κατηγορίες = {}
			for διάλεκτος, χρόνοι in κατηγορίες[μτλ].items():
				map_κατηγορίες[διάλεκτος] = {}
				for χρόνο, ακατηγορίες in χρόνοι.items():
					map_κατηγορίες[διάλεκτος][χρόνο] = []
					for αριθμό, σύνολο in ακατηγορίες.items():
						while int(αριθμό)>=len(map_κατηγορίες[διάλεκτος][χρόνο]):
							map_κατηγορίες[διάλεκτος][χρόνο].append({})
						σύνολο["κΚαταλήξεις"] = self.__κΚαταλήξεις(σύνολο['καταλήξεις'])
						map_κατηγορίες[διάλεκτος][χρόνο][int(αριθμό)] = σύνολο
			κατηγορίες[μτλ].clear()
			κατηγορίες[μτλ].update(map_κατηγορίες)
			if μτλ=="μετοχή":
				for διάλεκτος in κατηγορίες[μτλ]:
					κατηγορίες[μτλ][διάλεκτος]["συντελεσμένος μέλλοντας"] = κατηγορίες[μτλ][διάλεκτος]["μέλλοντας"]
		
		for μτλ in ["επίθετο", "ουσιαστικό"]:
			map_κατηγορίες = {}
			for διάλεκτος, ακατηγορίες in κατηγορίες[μτλ].items():
				map_κατηγορίες[διάλεκτος] = []
				for αριθμό, σύνολο in ακατηγορίες.items():
					while int(αριθμό)>=len(map_κατηγορίες[διάλεκτος]):
						map_κατηγορίες[διάλεκτος].append({})
					σύνολο["κΚαταλήξεις"] = self.__κΚαταλήξεις(σύνολο['καταλήξεις'])
					map_κατηγορίες[διάλεκτος][int(αριθμό)] = σύνολο
			κατηγορίες[μτλ].clear()
			κατηγορίες[μτλ].update(map_κατηγορίες)
		
	def __έλεγχος_τόνων(self, τονισμοί):
		for μτλ in τονισμοί:
			map_τόνων = {}
			for διάλεκτος, ακατηγορίες in τονισμοί[μτλ].items():
				map_τόνων[διάλεκτος] = []
				for αριθμό, σύνολο in ακατηγορίες.items():
					while int(αριθμό)>=len(map_τόνων[διάλεκτος]):
						map_τόνων[διάλεκτος].append({"τονισμοί":[]})
					map_τόνων[διάλεκτος][int(αριθμό)]["τονισμοί"] = σύνολο
			τονισμοί[μτλ].clear()
			τονισμοί[μτλ].update(map_τόνων)
		
	def __έλεγχος_θεμάτων(self, θέματα):
		μεταδεδομένα = []
		κλίμακες = []
		for διάλεκτος, θέμα in θέματα.items():
			μέγεθος = len(θέμα)
			for v in range(μέγεθος):
				if "μεταδεδομένα" in θέματα[διάλεκτος][v]:
					for k in θέματα[διάλεκτος][v]["μεταδεδομένα"]:
						if k not in μεταδεδομένα:
							μεταδεδομένα.append(k)
				if "κλίμακες" in θέματα[διάλεκτος][v]:
					for k in θέματα[διάλεκτος][v]["κλίμακες"]:
						if k not in κλίμακες:
							κλίμακες.append(k)
				if θέματα[διάλεκτος][v]["μέρος του λόγου"] == "ρήμα":
					θέματα[διάλεκτος][v]["κΛέξη"] = self.τ.κωδικοποιητής(θέματα[διάλεκτος][v]["θέμα"])
					if "συνθετικό" in θέματα[διάλεκτος][v]:
						θέματα[διάλεκτος][v]["κΣυνθετικό"] = self.τ.κωδικοποιητής(θέματα[διάλεκτος][v]["συνθετικό"])
					if "ενεστωτική αύξηση" in θέματα[διάλεκτος][v]:
						θέματα[διάλεκτος][v]["κΕνεστωτική αύξηση"] = self.τ.κωδικοποιητής(θέματα[διάλεκτος][v]["ενεστωτική αύξηση"])
					if "αύξηση παρακείμενου" in θέματα[διάλεκτος][v]:
						θέματα[διάλεκτος][v]["κΑύξηση παρακείμενου"] = self.τ.κωδικοποιητής(θέματα[διάλεκτος][v]["αύξηση παρακείμενου"])
					if "αύξηση" in θέματα[διάλεκτος][v]:
						θέματα[διάλεκτος][v]["κΑύξηση"] = self.τ.κωδικοποιητής(θέματα[διάλεκτος][v]["αύξηση"])
				else:
					θέματα[διάλεκτος][v]["κΛέξη"] = self.τ.κωδικοποιητής(θέματα[διάλεκτος][v]["λήμμα"])
					if "συνθετικό" in θέματα[διάλεκτος][v]:
						θέματα[διάλεκτος][v]["κΣυνθετικό"] = self.τ.κωδικοποιητής(θέματα[διάλεκτος][v]["συνθετικό"])
		return [μεταδεδομένα , κλίμακες]
		
	def _αποθήκευση(self):
		self.__αποθήκευση_λεξικού()

	def _αποθήκευση_λεξικού(self):
		νέα_θέματα = {}
		for διάλεκτος, θέματα in self.θέματα.items():
			νέα_θέματα[διάλεκτος] = {}
			for θέμα in θέματα:
				if θέμα["θέμα"] not in νέα_θέματα[διάλεκτος]:
					νέα_θέματα[διάλεκτος][θέμα["θέμα"]] = []
				νέα_θέματα[διάλεκτος][θέμα["θέμα"]].append(θέμα)
			
		κείμενο = "{\n"
		for διάλεκτος, θέματα in νέα_θέματα.items():
			κείμενο += '\t"'+διάλεκτος+'":{\n '
			τθέματα = list(θέματα.keys())
			τθέματα.sort()
			for θέμα in τθέματα:
				κείμενο += '\t\t"'+θέμα+'":['
				σύνολα = θέματα[θέμα]
				for σύνολο in σύνολα:
					if κείμενο[-1]=="[":
						κείμενο += '{'
					else:
						κείμενο += '\t\t\t{'
					for κλειδί in ['συχνότητα', 'συνθετικό', 'αύξηση', 
									'ενεστωτική αύξηση', 'αύξηση παρακείμενου',
									'ενεστώτας', 'παρατατικός', 'αόριστος', 
									'παρακείμενος', 'υπερσυντέλικος', 'μέλλοντας', 
									'συντελεσμένος μέλλοντας']:
						if κλειδί in σύνολο:
							if κλειδί=='συχνότητα':
								κείμενο += '"'+κλειδί+'":'+str(σύνολο[κλειδί])+',\n'
							elif κλειδί in ['συνθετικό', 'αύξηση', 'ενεστωτική αύξηση', 'αύξηση παρακείμενου']:
								κείμενο += '\t\t\t"'+κλειδί+'":"'+σύνολο[κλειδί]+'",\n'
							elif κλειδί in ['ενεστώτας', 'παρατατικός', 'αόριστος', 
									'παρακείμενος', 'υπερσυντέλικος', 'μέλλοντας', 
									'συντελεσμένος μέλλοντας']:
								if διάλεκτος=="δημοτική":
									σύνολο[κλειδί]["καταλήξεις"][2] = 0
									σύνολο[κλειδί]["τονισμοί"][2] = 0
								κείμενο += '\t\t\t"'+κλειδί+'":{\n'
								κείμενο += '\t\t\t\t"καταλήξεις":'+str(σύνολο[κλειδί]["καταλήξεις"])+',\n'
								κείμενο += '\t\t\t\t"τονισμοί":'+str(σύνολο[κλειδί]["τονισμοί"])
								κείμενο += '},\n'
								if διάλεκτος=="δημοτική" and κλειδί=="αόριστος":
									κείμενο += '\t\t\t"μέλλοντας":{\n'
									kat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
									ton = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
									kat[0] = σύνολο[κλειδί]["καταλήξεις"][1]
									kat[5] = σύνολο[κλειδί]["καταλήξεις"][6]
									kat[10] = σύνολο[κλειδί]["καταλήξεις"][11]
									ton[0] = σύνολο[κλειδί]["τονισμοί"][1]
									ton[5] = σύνολο[κλειδί]["τονισμοί"][6]
									ton[10] = σύνολο[κλειδί]["τονισμοί"][11]
									κείμενο += '\t\t\t\t"καταλήξεις":'+str(kat)+',\n'
									κείμενο += '\t\t\t\t"τονισμοί":'+str(ton)
									κείμενο += '},\n'
					κείμενο = κείμενο[:-2]+'},\n'
				κείμενο = κείμενο[:-2]+'],\n'
			κείμενο = κείμενο[:-2]+'},\n'
		κείμενο = κείμενο[:-2]+"\n}"
		
		όνομα = "ρημάτων1.json"
		διαδρομή = os.path.join(φάκελος, 'λεξικά')
		if not os.path.exists(διαδρομή):
			os.mkdir(διαδρομή)
		διαδρομή = os.path.join(διαδρομή, όνομα)
		
		αρχείο = open(διαδρομή, 'w')
		αρχείο.write(κείμενο)
		αρχείο.close()
