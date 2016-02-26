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

import json, os
import cherrypy
from cherrypy.lib.static import serve_file
import threading
from copy import deepcopy

class web():
	def __init__(self, ελληνικά, json_out=False):
		self.json_out = json_out
		self.στίξη = {
			",":"κόμμα", " ":"κενό", ".":"τελεία", 
			"·":"άνω τελεία", "-":"ενωτικό"}
		self.ελληνικά = ελληνικά
		
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def HLT(self, *kwd):
		n=len(kwd)
		dkwd = []
		for k in kwd:
			dkwd.append(k.encode('latin').decode('utf-8'))
		
		print("kwd",dkwd)
		dump = []
		if n==0:
			raise cherrypy.HTTPRedirect("index.html")
		
		elif n>2 and dkwd[1]=="εξαγωγή":
			if dkwd[2]=="διαγραφή":
				πακέτο = dkwd[3]
				self.ελληνικά.εξαγωγή.διαγραφή(πακέτο)
				return "OK"
			elif dkwd[2]=="δημιουργία":
				πακέτο = eval(dkwd[3])
				if πακέτο["τύπος"]=="hunspell":
					timh = self.ελληνικά.εξαγωγή.hunspell(πακέτο["τίτλος"], πακέτο["διάλεκτοι"])
					return str(timh)
			elif dkwd[2]=="πρόοδος":
				input = dkwd[3]
				timh = self.ελληνικά.εξαγωγή.πρόοδος(int(input))
				return str(timh)
			elif dkwd[2]=="αποτέλεσμα":
				cherrypy.response.headers['Content-Type'] = "application/x-download"
				return self.ελληνικά.εξαγωγή.αποτέλεσμα(dkwd[3])
		elif n>2 and dkwd[1]=="dump":
			dump = []
			if dkwd[2]=="εξαγωγή":
				dump.append(self.ελληνικά.εξαγωγή.έτοιμα())
			elif dkwd[2]=="διάλεκτοι":
				dump.append(self.ελληνικά.γ._δεδομένα.διάλεκτοι_φόρτωση(True))
			elif dkwd[2]=="άρθρο":
				έξοδος = {}
				for διάλεκτος, ανώμαλα in self.ελληνικά.γ._δεδομένα.ανώμαλα_φόρτωση(True)["άρθρο"].items():
					έξοδος[διάλεκτος] = []
					for ανώμαλο in ανώμαλα:
						if "τρέχον" in ανώμαλο["ἐτικέτες"]:
							έξοδος[διάλεκτος].append(ανώμαλο)
				dump.append(έξοδος)
			elif dkwd[2]=="αντωνυμία":
				έξοδος = {}
				for διάλεκτος, ανώμαλα in self.ελληνικά.γ._δεδομένα.ανώμαλα_φόρτωση(True)["αντωνυμία"].items():
					έξοδος[διάλεκτος] = {}
					for ανώμαλο in ανώμαλα:
						if "τρέχον" in ανώμαλο["ἐτικέτες"]:
							for μέτα in ανώμαλο["Μεταδεδομένα"]["τύπος αντωνυμίας"]:
								if μέτα not in έξοδος[διάλεκτος]:
									έξοδος[διάλεκτος][μέτα] = []
							έξοδος[διάλεκτος][μέτα].append(ανώμαλο)
				dump.append(έξοδος)
			elif dkwd[2] in ["μόριο", "επίρρημα", "πρόθεση", "σύνδεσμος", "επιφώνημα"]:
				έξοδος = {}
				for διάλεκτος, ανώμαλα in self.ελληνικά.γ._δεδομένα.ανώμαλα_φόρτωση(True)[dkwd[2]].items():
					έξοδος[διάλεκτος] = []
					for ανώμαλο in ανώμαλα:
						if "τρέχον" in ανώμαλο["ἐτικέτες"]:
							έξοδος[διάλεκτος].append(ανώμαλο)
				dump.append(έξοδος)
			elif dkwd[2]=="επίθετο":
				dump.append(self.ελληνικά.γ.επίθετα.dump())
			elif dkwd[2]=="ουσιαστικό":
				dump.append(self.ελληνικά.γ.ουσιαστικά.dump())
			elif dkwd[2]=="ρήμα":
				dump.append(self.ελληνικά.γ.ρήματα.dump())
			elif dkwd[2]=="μετοχή":
				dump.append(self.ελληνικά.γ.μετοχές.dump())
			return str(dump).replace("'",'"').replace("None", "null").replace("True", "true")
		elif n>3 and kwd[0].encode('latin').decode('utf-8')=='Ελληνικά':
			order = kwd[1].encode('latin').decode('utf-8')
			if order in ["IME", "ΙΜΕ"]:
				διάλεκτος = kwd[2].encode('latin').decode('utf-8')
				εντολή = kwd[3].encode('latin').decode('utf-8')
				γράμματα = kwd[4].encode('latin').decode('utf-8')
				κατάληξη = None
				if len(kwd)>5:
					κατάληξη = kwd[5].encode('latin').decode('utf-8')
				ανάλυση = self.ελληνικά.IME.μυνήματα(διάλεκτος, εντολή, γράμματα, κατάληξη)
				
				if self.json_out:
					return json.dumps(ανάλυση, 'utf-8') # json version
				else:
					return str(ανάλυση) # plain text version
			elif order=="ανάλυση":
				διάλεκτος = kwd[2].encode('latin').decode('utf-8')
				κείμενο = kwd[3].encode('latin').decode('utf-8')
				
				ανάλυση = self.ελληνικά.ανάλυσε(κείμενο, διάλεκτος)
				
				if self.json_out:
					return json.dumps(ανάλυση, 'utf-8') # json version
				else:
					return str(ανάλυση).replace("None", "null") # plain text version
			elif order=="αναγνώριση":
				διάλεκτος = kwd[2].encode('latin').decode('utf-8')
				λέξεις = kwd[3].encode('latin').decode('utf-8')
				
				αναγνώριση = self.αναγνώριση(λέξεις, διάλεκτος)
				
				if self.json_out:
					return json.dumps(αναγνώριση, 'utf-8') # json version
				else:
					return str(αναγνώριση).replace("None", "null") # plain text version
			elif order=="πολυτονισμός":
				διάλεκτος = kwd[2].encode('latin').decode('utf-8')
				κείμενο = kwd[3].encode('latin').decode('utf-8')
				
				πολυτονισμός = self.ελληνικά.πολυτόνισε(κείμενο, διάλεκτος)
				
				if self.json_out:
					return json.dumps(πολυτονισμός, 'utf-8') # json version
				else:
					return str(πολυτονισμός).replace("None", "null") # plain text version
			elif order=="κλίση":
				διάλεκτος = dkwd[2]
				λέξεις = dkwd[3]
				
				κλίσεις = self.κλίση(λέξεις, διάλεκτος)
				print("κλίσεις",κλίσεις)
				if self.json_out:
					return json.dumps(κλίσεις, 'utf-8') # json version
				else:
					return str(κλίσεις).replace("'",'"').replace("None", "null") # plain text version
			elif order=="κλίση_web":
				διάλεκτος = dkwd[3]
				άκλητο = dkwd[2]
				dump = []
				
				if άκλητο=="επίθετο":
					λέξη = dkwd[4]
					dump.append(self.ελληνικά.γ.επίθετα.dump(διάλεκτος, λέξη))
				elif άκλητο=="ουσιαστικό":
					λέξη = dkwd[4]
					dump.append(self.ελληνικά.γ.ουσιαστικά.dump(διάλεκτος, λέξη))
				elif άκλητο=="μετοχή":
					λέξη = dkwd[4]
					dump.append(self.ελληνικά.γ.μετοχές.dump(διάλεκτος, λέξη))
				elif άκλητο=="ρήμα":
					λέξη = dkwd[4]
					dump.append(self.ελληνικά.γ.ρήματα.dump(διάλεκτος, λέξη))
				if self.json_out:
					return json.dumps(dump, 'utf-8') # json version
				else:
					return str(dump).replace("'",'"').replace("None", "null") # plain text version
		elif n>2:
			if dkwd[1]=="js":
				print("FILE",kwd[2])
				path = os.path.join("Ελληνικά","web", "public", "js", kwd[2])
				if os.path.exists(path):
					f=open(path,'r')
					js=f.read()
					f.close()
					return js
			else:
				return ""
		elif n>1 and kwd[0].encode('latin').decode('utf-8')=='Ελληνικά':
			order = kwd[1].encode('latin').decode('utf-8')
			if order=="index.html":
				print("FILE","index.html")
				f=open(os.path.join("Ελληνικά","web", "public", "index.html"),'r')
				html=f.read()
				f.close()
				return html
			else:
				print("FILE",order+".html")
				path = os.path.join("Ελληνικά","web", "public", order+".html")
				if os.path.exists(path):
					f=open(path,'r')
					html=f.read()
					f.close()
					return html
		raise cherrypy.HTTPRedirect("http://localhost:7000/HLT/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AC/index.html")
		
	def κλίση(self, text, διάλεκτος):
		κλίσεις = [] # [λέξη, {διάλεκτος1:[κλίση]}]
		
		acc = ""
		στοιχεία = []
		for γράμμα in text:
			if γράμμα in self.στίξη:
				if acc:
					αναγνωρίσεις = []
					αναγνωρίσεις += deepcopy(self.ελληνικά.γ.αναγνώριση(acc, διάλεκτος))
					self.ελληνικά.γ._αναγνώριση._φίλτρο_κατηγοριών(αναγνωρίσεις)
					στοιχεία.append([acc, αναγνωρίσεις])
					acc = ""
			else:
				acc += γράμμα
				
		if acc:
			αναγνωρίσεις = deepcopy(self.ελληνικά.γ.αναγνώριση(acc, διάλεκτος))
			self.ελληνικά.γ._αναγνώριση._φίλτρο_κατηγοριών(αναγνωρίσεις)
			στοιχεία.append([acc, αναγνωρίσεις])
			
		for στοιχείο in στοιχεία:
			κλίση = [στοιχείο[0]]
			κλιμένα = {}
			for αναγνώριση in στοιχείο[1]:
				μέρος_του_λόγου = αναγνώριση["μέρος του λόγου"]
				διάλεκτος = αναγνώριση["διάλεκτος"]
				if διάλεκτος not in κλιμένα:
					κλιμένα[διάλεκτος] = {}
				if μέρος_του_λόγου not in κλιμένα:
					κλιμένα[διάλεκτος][μέρος_του_λόγου] = []
				if μέρος_του_λόγου=="άρθρο":
					κλιμένα[διάλεκτος][μέρος_του_λόγου].append(self.ελληνικά.γ.άρθρα._πλήρη_κλίση(αναγνώριση))
				elif μέρος_του_λόγου=="ουσιαστικό":
					αποτέλεσμα = {}
					for γένος, τιμές in self.ελληνικά.γ.ουσιαστικά._πλήρη_κλίση(αναγνώριση).items():
						αποτέλεσμα[γένος] = []
						for τιμή in τιμές:
							υ = []
							for υπο in τιμή:
								υ.append(self.ελληνικά.γ.τ.απο(υπο, True))
							αποτέλεσμα[γένος].append(υ)
					κλιμένα[διάλεκτος][μέρος_του_λόγου].append(αποτέλεσμα)
				elif μέρος_του_λόγου=="επίθετο":
					αποτέλεσμα = {}
					for γένος, τιμές in self.ελληνικά.γ.επίθετα._πλήρη_κλίση(αναγνώριση).items():
						αποτέλεσμα[γένος] = []
						for τιμή in τιμές:
							υ = []
							for υπο in τιμή:
								υ.append(self.ελληνικά.γ.τ.απο(υπο, True))
							αποτέλεσμα[γένος].append(υ)
					κλιμένα[διάλεκτος][μέρος_του_λόγου].append(αποτέλεσμα)
				elif μέρος_του_λόγου=="ρήμα":
					αποτέλεσμα = {}
					for χρόνος, φωνές in self.ελληνικά.γ.ρήματα._πλήρη_κλίση(αναγνώριση).items():
						αποτέλεσμα[χρόνος] = {}
						for φωνή, εγκλίσεις in φωνές.items():
							αποτέλεσμα[χρόνος][φωνή] = {}
							for έγκλιση, τιμές in εγκλίσεις.items():
								αποτέλεσμα[χρόνος][φωνή][έγκλιση] = []
								for τιμή in τιμές:
									υ = []
									for υπο in τιμή:
										υ.append(self.ελληνικά.γ.τ.απο(υπο, True))
									αποτέλεσμα[χρόνος][φωνή][έγκλιση].append(υ)
					κλιμένα[διάλεκτος][μέρος_του_λόγου].append(αποτέλεσμα)
				elif μέρος_του_λόγου=="μετοχή":
					αποτέλεσμα = {}
					for γένος, τιμές in self.ελληνικά.γ.μετοχές._πλήρη_κλίση(αναγνώριση).items():
						αποτέλεσμα[γένος] = []
						for τιμή in τιμές:
							υ = []
							for υπο in τιμή:
								υ.append(self.ελληνικά.γ.τ.απο(υπο, True))
							αποτέλεσμα[γένος].append(υ)
					κλιμένα[διάλεκτος][μέρος_του_λόγου].append(αποτέλεσμα)
				elif μέρος_του_λόγου=="αντωνυμία":
					κλιμένα[διάλεκτος][μέρος_του_λόγου].append(self.ελληνικά.γ.αντωνυμίες._πλήρη_κλίση(αναγνώριση))
				else:
					κλ = ""
					if "λήμμα" in αναγνώριση:
						κλ = αναγνώριση["λήμμα"]
					elif "κατάληξη" in αναγνώριση:
						κλ = αναγνώριση["κατάληξη"]
					κλιμένα[διάλεκτος][μέρος_του_λόγου].append({"άκλητο":κλ})
			κλίση.append(κλιμένα)
			κλίσεις.append(κλίση)
		return κλίσεις
		
	def αναγνώριση(self, text, διάλεκτος):
		στοιχεία = []
		acc = ""
		for γράμμα in text:
			if γράμμα in self.στίξη:
				if acc:
					αναγνωρίσεις = deepcopy(self.ελληνικά.γ.αναγνώριση(acc, διάλεκτος))
					ν, μγ = 0, len(αναγνωρίσεις)
					while ν<μγ:
						if "κΚατάληξη" in αναγνωρίσεις[ν]:
							del αναγνωρίσεις[ν]["κΚατάληξη"]
						if "κΛέξη" in αναγνωρίσεις[ν]:
							del αναγνωρίσεις[ν]["κΛέξη"]
						ν+=1
					στοιχεία.append([acc, αναγνωρίσεις])
					acc = ""
			else:
				acc += γράμμα
		if acc:
			αναγνωρίσεις = deepcopy(self.ελληνικά.γ.αναγνώριση(acc, διάλεκτος))
			ν, μγ = 0, len(αναγνωρίσεις)
			while ν<μγ:
				for διαγραφόμενο in ["κΣυνθετικό", "κΑύξηση", "κΚατάληξη", "κΛέξη", "ανώμαλο"]:
					if διαγραφόμενο in αναγνωρίσεις[ν]:
						del αναγνωρίσεις[ν][διαγραφόμενο]
				ν+=1
			στοιχεία.append([acc, αναγνωρίσεις])
		
		return στοιχεία
		
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def index(self):
		raise cherrypy.HTTPRedirect("http://localhost:7000/HLT/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AC/index.html")
		