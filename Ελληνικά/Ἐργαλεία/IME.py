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

class IME():
	def __init__(self, γραμματική):
		self.γ = γραμματική
		self.τ = self.γ.τ
		self.bανώμαλα = self.γ._ευρετήρια.bανώμαλα
		self.bθεμάτων = self.γ._ευρετήρια.bθεμάτων
		self.rανώμαλα = self.γ._ευρετήρια.rανώμαλα
		self.rθεμάτων = self.γ._δεδομένα.θέματα
		self._επιλογή = []
		self.κατάσταση = 0
		self.αλληλουχία = []
		self.διάλεκτος = self.γ.διάλεκτος
		self.υποψηφιότητες_λημμάτων = {}
		self.υποψηφιότητες_λέξεων = {}
		self.τΛήμμα = ""
		self.mode = ""
		self.αντιστοιχίες_καταλήξεων = {}
		self.cache = {"κοινή":{}, "δημοτική":{}}
		self.cache_λέξεις = {"κοινή":{}, "δημοτική":{}}
		self.cache_λήμματα = {"κοινή":{}, "δημοτική":{}}
		# (συμπλήρωση των bΚαταλήξεις;;;;;)
		# μυνήματα
		# ["text", μύνημα[1]]
		# ["backspace"]
		# ["reset"]
		# ["preedit"]
		# ["commit", λέξη]
		# => ["list", "horizontal", απο, αποτελέσματα]
		# => ["list", "vertical", αποτελέσματα[0], list(καταλήξεις.keys())]
		#
		# υποψηφιότητες: βάζουμε γράμματα, βρίσκουμε λήμματα, κλίνουμε όλα τα λήμματα με μέγεθος+2, επιστροφή
		# ημικλίση: κλίνουμε όλες τις λέξεις
		
	def __merge_dicts(self, d1,d2):
		for k, v in d2.items():
			if k not in d1:
				d1[k] = v
			else:
				for k2, v2 in v.items():
					if k2 not in d1[k]:
						d1[k][k2] = v2
					else:
						d1[k][k2]+=v2
	
	def __merge_dic_list(self, d1,d2):
		for k, v in d2.items():
			if k not in d1:
				d1[k] = v
			else:
				for k2 in v:
					if k2 not in d1[k]:
						d1[k].append(k2)
							
	def __υποψηφιότητες(self, γράμματα, διάλεκτος):
		# IN:
		# ημιλέξη
		#
		# OUT
		# {ΔΑ:{ημιλέξη:[{ιδιότητες},]}}
		
		# init				
		κΛέξη = self.τ.κωδικοποιητής(γράμματα)
		bΛέξη = self.τ.απλοποιητής(κΛέξη)
		κμέγεθος = κΛέξη.size
		bμέγεθος = bΛέξη.size
		άθροισμα = (κΛέξη & 255).sum()
		
		κεφαλαία, κεφαλαίο = None, None
		if κμέγεθος>1 and γράμματα[1].isupper():
			κεφαλαία = True
		elif γράμματα and γράμματα[0].isupper():
			κεφαλαίο = True
		
		αποτέλεσμα = {}
		αποτελέσματα = []
		
		# main
		# stepsearch: {Δάθροισμα:λέξη:[ιδιότητες]
		αποτέλεσμα = self._stepsearch(κΛέξη, bΛέξη, κμέγεθος, bμέγεθος, άθροισμα)
		
		# output
		# self.υποψηφιότητες_λημμάτων: {λέξη:ιδιότητες}
		νέο_λεξικό = {}
		
		κλειδιά = list(αποτέλεσμα.keys())
		κλειδιά.sort()
		λέξεις = []
		for κλειδί in κλειδιά:
			for σύνολο in αποτέλεσμα[κλειδί]:
				λέξη = None
				if 'κατάληξη' in σύνολο:
					λέξη = σύνολο['κατάληξη']
				else:
					if 'λήμμα' in σύνολο:
						if "συνθετικό" in σύνολο:
							λέξη = σύνολο['συνθετικό']+σύνολο['λήμμα']
						else:
							λέξη = σύνολο['λήμμα']
					elif 'θέμα' in σύνολο:
						λέξη = σύνολο['θέμα']
						# ποιο συνθετικό:
						#["συνθετικό", "αύξηση", "ενεστωτική αύξηση", "αύξηση παρακείμενου"]
				
				if σύνολο.get("ανώμαλο"):
					self.cache_λέξεις[λέξη] = σύνολο
				else:
					self.cache_λήμματα[λέξη] = σύνολο
					
				if λέξη:
					if κεφαλαία:
						λέξη = λέξη.upper()
					elif κεφαλαίο:
						λέξη = λέξη.capitalize()
					if λέξη not in λέξεις:
						λέξεις.append(λέξη)
		
		return λέξεις
	
	def __ημικλίση(self, γράμματα, αριθμός, πτώση, γένος):
		# match άρθρο-επίθετο-ουσιαστικό(αριθμό,πτώση,γένος)
		# match αντωνυμία-ρήμα(πρόσωπο, αριθμό)
		
		# init
		κΛέξη = self.τ.κωδικοποιητής(γράμματα)
		bΛέξη = self.τ.απλοποιητής(κΛέξη)
		κμέγεθος = κΛέξη.size
		bμέγεθος = bΛέξη.size
		άθροισμα = (κΛέξη & 255).sum()
		
		κεφαλαία, κεφαλαίο = None, None
		if κμέγεθος>1 and γράμματα[1].isupper():
			κεφαλαία = True
		elif γράμματα and γράμματα[0].isupper():
			κεφαλαίο = True
		
		αποτέλεσμα = {}
		αποτελέσματα = []
		
		# main
		αποτέλεσμα = self.γ.α._stepsearch(κΛέξη, bΛέξη, κμέγεθος, bμέγεθος, άθροισμα)
		αποτέλεσμα2 = self.γ.αν._stepsearch(κΛέξη, bΛέξη, κμέγεθος, bμέγεθος, άθροισμα)
		self.__merge_dicts(αποτέλεσμα, αποτέλεσμα2)
		αποτέλεσμα3 = self.γ.ακ._stepsearch(κΛέξη, bΛέξη, κμέγεθος, bμέγεθος, άθροισμα)
		self.__merge_dicts(αποτέλεσμα, αποτέλεσμα3)
		αποτέλεσμα4 = self.γ.επ._stepsearch(κΛέξη, bΛέξη, κμέγεθος, bμέγεθος, άθροισμα)
		self.__merge_dicts(αποτέλεσμα, αποτέλεσμα4)
		αποτέλεσμα5 = self.γ.ο._ημικλίση(κΛέξη, bΛέξη, κμέγεθος, bμέγεθος, αριθμός, πτώση, γένος, άθροισμα)
		self.__merge_dicts(αποτέλεσμα, αποτέλεσμα5)
		
		# output
		κ = list(αποτέλεσμα.keys())
		κ.sort()
		
		for κκ in κ:
			self.__merge_dic_list(self.υποψηφιότητες_λέξεων, αποτέλεσμα[κκ])
			λέξεις = list(αποτέλεσμα[κκ].keys())
			λέξεις.sort()
			if κεφαλαία:
				λέξεις = [λέξη.upper() for λέξη in λέξεις]
			elif κεφαλαίο:
				λέξεις = [λέξη.capitalize() for λέξη in λέξεις]
			αποτελέσματα += λέξεις
		
		return αποτελέσματα
	
	def __καταλήξεις(self, λήμμα):
		# match άρθρο-επίθετο-ουσιαστικό(αριθμό,πτώση,γένος)
		# match αντωνυμία-ρήμα(πρόσωπο, αριθμό), "κλίση":{}
		
		# init
		καταλήξεις = []
		
		μτλ = λήμμα['μέρος του λόγου']
		διάλεκτος = λήμμα["διάλεκτος"]
		if μτλ=='ουσιαστικό':
			κατάληξη = self.γ._δεδομένα.κατηγορίες["ουσιαστικό"][διάλεκτος]
			κατηγορία = λήμμα["κατηγορία"]
			for υπο in κατάληξη[κατηγορία]["καταλήξεις"]:
				καταλήξεις += υπο 
		elif μτλ=='επίθετο':
			κατάληξη = self.γ._δεδομένα.κατηγορίες["επίθετο"][διάλεκτος]
			κατηγορίες = λήμμα["κατηγορίες"]
			for κατηγορία in κατηγορίες:
				for υπο in κατάληξη[κατηγορία]["καταλήξεις"]:
					καταλήξεις += υπο 
		elif μτλ=='ρήμα':
			αποτελέσματα[λήμμα]= [λήμμα]
		elif μτλ=='μετοχή':
			pass
		
		return list(set(καταλήξεις))
	
	def __σύνθεση(self, λήμμα, κατάληξη):
		μτλ = λήμμα['μέρος του λόγου']
		διάλεκτος = λήμμα["διάλεκτος"]
		if μτλ=='ουσιαστικό':
			pass
		elif μτλ=='επίθετο':
			pass
		elif μτλ=='ρήμα':
			pass
		elif μτλ=='μετοχή':
			pass
		return [λήμμα["λήμμα"]+κατάληξη]
	
	def _stepsearch(self, κΛέξη, bΛέξη, κμέγεθος, bμέγεθος, άθροισμα, διάλεκτος=None):
		αποτελέσματα = {}
		if διάλεκτος:
			τΔιάλεκτος = διάλεκτος
		else:
			τΔιάλεκτος = self.διάλεκτος
			
		for ευρετήριο, κλέξη, μέγεθος, rdict in [[self.bανώμαλα, bΛέξη, bμέγεθος, self.rανώμαλα], 
															[self.bθεμάτων, bΛέξη, bμέγεθος, self.rθεμάτων]]:
			if αποτελέσματα:
				break
			
			ακ = {}
			λεξικά = self.τ.stepfinder(ευρετήριο[τΔιάλεκτος], κλέξη, μέγεθος, ακ)
			
			κατηγορίες = []
			self.τ.rv(λεξικά, κατηγορίες, 0)
			
			for κατηγορία in κατηγορίες:
				ανώμαλο = rdict[τΔιάλεκτος][κατηγορία]
				τκΛέξη = []
				if 'κΛέξη' in ανώμαλο:
					τκΛέξη = ανώμαλο['κΛέξη']
				elif "κΚατάληξη" in ανώμαλο:
					τκΛέξη = ανώμαλο['κΚατάληξη']
				else:
					continue
				
				αθρ = (τκΛέξη[:κμέγεθος]&255).sum().item()
				αθρ = abs(αθρ-άθροισμα)+abs(τκΛέξη.size-κμέγεθος)
				
				if not αθρ in αποτελέσματα:
					αποτελέσματα[αθρ] = []
				αποτελέσματα[αθρ].append(ανώμαλο)
		
		return αποτελέσματα
	
	def μυνήματα(self, διάλεκτος, εντολή, γράμματα=None, κατάληξη=None):
		if εντολή == "μηδενισμός":
			self.αλληλουχία = []
		elif εντολή == "υποψηφιότητες":
			return ["υποψηφιότητες", self.__υποψηφιότητες(γράμματα, διάλεκτος)]
		elif εντολή == "επιλογή":
			if γράμματα in self.cache_λέξεις:
				self.αλληλουχία.append(γράμματα)
				return ["OK"]
			elif γράμματα in self.cache_λήμματα:
				return ["καταλήξεις", self.__καταλήξεις(self.cache_λήμματα[γράμματα])]
		elif εντολή == "κατάληξη" and γράμματα in self.cache_λήμματα:
			return ["υποψηφιότητες", self.__σύνθεση(self.cache_λήμματα[γράμματα], κατάληξη)]
		return []
	
	def μυνήματα0(self, μύνημα):
		# init
		απάντηση = ["text", μύνημα[1]]
		postfix = ""
		στοιχείο = []
		
		if μύνημα[1][-1] in [" ", ".", ","]:
			if μύνημα[0]=="commit":
				postfix = μύνημα[1][-1]
			μύνημα[1] = μύνημα[1][:-1]
		
		if μύνημα[0]=="backspace":
			if μύνημα[1]:
				απάντηση = ["text", μύνημα[1]]
			else:
				απάντηση = ["text", ""]
		elif μύνημα[0]=="reset":
			# init
			self.τΛήμμα = ""
			αποτελέσματα = ""
			self.mode = ""
			απάντηση = ["text", ""]
			self.αντιστοιχίες_καταλήξεων.clear()
		elif μύνημα[0]=="preedit":
			# init
			self.τΛήμμα = ""
			αποτελέσματα = ""
			
			# main
			if len(self.αλληλουχία)>1 and\
				self.αλληλουχία[-1][0]==" " and\
				self.αλληλουχία[-2][1]=="άρθρο":
				self.mode = "ημικλήση"
				αριθμός = self.αλληλουχία[-2][3]
				πτώση = self.αλληλουχία[-2][4][0]
				γένος = self.αλληλουχία[-2][2]
				αποτελέσματα = self.__ημικλίση(μύνημα[1], αριθμός, πτώση, γένος)
			else:
				self.mode = "υποψηφιότητες"
				αποτελέσματα = self.__υποψηφιότητες(μύνημα[1])
			
			# output
			μ_αποτελέσματα = len(αποτελέσματα)
			if μ_αποτελέσματα>1:
				κΛέξη = self.τ.κωδικοποιητής(μύνημα[1])
				απο = self.τ.απο(κΛέξη)
				απάντηση = ["list", "horizontal", απο, αποτελέσματα]
			elif μ_αποτελέσματα==1:
				if self.mode == "ημικλήση":
					απάντηση = ["text", αποτελέσματα[0]]
				else:
					self.mode = "καταλήξεις"
					καταλήξεις = self.__καταλήξεις(αποτελέσματα[0])
					απάντηση = ["list", "vertical", αποτελέσματα[0], list(καταλήξεις.keys())]
			else:
				απάντηση = ["text", μύνημα[1]]
			
		elif μύνημα[0]=="διάλεκτος":
			self.διάλεκτος = μύνημα[1]
			απάντηση = ["διάλεκτος", μύνημα[1]]
		elif μύνημα[0]=="commit":
			# main
			if self.mode == "υποψηφιότητες":
				καταλήξεις = self.__καταλήξεις(μύνημα[1])
				κΛέξη = self.τ.κωδικοποιητής(μύνημα[1])
				λέξη = self.τ.απο(κΛέξη)
				
				μ_καταλήξεις = len(καταλήξεις)
				if μ_καταλήξεις>1:
					self.mode = "καταλήξεις"
					self.τΛήμμα = μύνημα[1]
					απάντηση = ["list", "vertical", λέξη, list(καταλήξεις.keys())]
				elif μ_καταλήξεις==1:
					for k,v in καταλήξεις.items():
						if self.mode == "καταλήξεις":
							απάντηση = ["text", v+postfix]
						else:
							καταλήξεις2 = self.__καταλήξεις(v)
							απάντηση = ["list", "vertical", v, list(καταλήξεις2.keys())]
					self.mode = ""
				else:
					απάντηση = ["text", μύνημα[1]+postfix]
					self.mode = ""
			
			elif self.mode == "καταλήξεις":
				if μύνημα[1] in self.αντιστοιχίες_καταλήξεων:
					στοιχείο = self.αντιστοιχίες_καταλήξεων[μύνημα[1]][0]
					απάντηση = ["text", στοιχείο[0]+postfix]
					
					self.αντιστοιχίες_καταλήξεων.clear()
				self.mode = ""
			elif self.mode == "ημικλήση":
				if μύνημα[1] in self.υποψηφιότητες_λέξεων:
					στοιχείο = self.υποψηφιότητες_λέξεων[μύνημα[1]]
					απάντηση = ["text", μύνημα[1]+postfix]
				self.mode = ""
			
			# memory
			if στοιχείο:
				self.αλληλουχία.append(στοιχείο)
				
			self.τΛήμμα = ""
			if στοιχείο and postfix:
				είδος = ""
				if postfix==" ":
					είδος = "κενό"
				elif postfix==".":
					είδος = "τελεία"
				elif postfix==",":
					είδος = "κόμμα"
				self.αλληλουχία.append([postfix, "στίξη", είδος])
				
		return απάντηση

# TODO: BACKSPACE 