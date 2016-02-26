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

import numpy as np
from copy import deepcopy
μήκος = len
τύπωσε = print

class Ανάλυση():
	def __init__(self, γραμματική):
		self.γραμματική = γραμματική
		self.γ = γραμματική
		self.στίξη = {
			",":"κόμμα", " ":"κενό", ".":"τελεία", 
			"·":"άνω τελεία", "-":"ενωτικό"}
		self.ακολουθείες = {
			"δημοτική":{
				# μτλ1:[
				#	{"θέση":0,
				#	"αγνόηση στίξης":["",""], 
				#  μτλ2:"", 
				#  "ισότητες":{}, ισότητες ανάμεσα στα μτλ1 και και μτλ2 για επιλογή μτλ1
				#  "συνθήκες":{}, του μτλ2 για να ισχύουν οι «επιλογές» του μτλ1,
				#  "επιλογές":{}, του μτλ1 ]
				"αντωνυμία":[{"θέση":1, "μτλ":"ρήμα", "επιλογές":{'Μεταδεδομένα': {'τύπος αντωνυμίας': ['προσωπική']}}}],
				"επίρρημα":[{"θέση":-1, "μτλ":"επίθετο", "επιλογές":{'Μεταδεδομένα': {'ιδιότητες': ["τοπικό στάση","δεικτικό"]}}}],
				"ρήμα":[{"θέση":-1, "μτλ":"μόριο", "συνθήκες":{'λήμμα': 'νὰ'}, "επιλογές":{'έγκλιση': 'υποτακτική'}}],
				"άρθρο":[{"θέση":1, "μτλ":"ουσιαστικό", "ισότητες":['γένος', 'αριθμός']},#, 'πτώση'
							{"θέση":1, "μτλ":"επίθετο", "ισότητες":['γένος', 'αριθμός']}],#, 'πτώση'
				"μόριο":[{"θέση":1, "μτλ":"ρήμα", "επιλογές":{'Μεταδεδομένα': {'ιδιότητες': ['δεικτικά', 'βουλητικά']}}},
							{"θέση":1, "μτλ":"μόριο", "επιλογές":{'Μεταδεδομένα': {'ιδιότητες': ['προτρεπτικά']}}}],
				"πρόθεση":[{"θέση":1, "μτλ":"άρθρο", "επιλογές":{'Μεταδεδομένα': {'ιδιότητες': ['κύρια']}}},
							{"θέση":1, "μτλ":"αντωνυμία", "επιλογές":{'Μεταδεδομένα': {'ιδιότητες': ['κύρια']}}}]
			}
		}
		self.ακολουθείες["κοινή"] = self.ακολουθείες["δημοτική"]
	
	def _ακολουθείες(self, κΣτοιχεία, διάλεκτος):
		ν = 0
		μγ = len(κΣτοιχεία)
		while ν<μγ:
			νέες_αναγνωρίσεις = []
			for αν1 in κΣτοιχεία[ν][-1]:
				if αν1['μέρος του λόγου'] not in self.ακολουθείες[διάλεκτος]:
					continue
				σύνολα = self.ακολουθείες[διάλεκτος][αν1['μέρος του λόγου']]
				addit = False
				for σύνολο in σύνολα:
					off = σύνολο["θέση"]
					if off>0:
						while (ν+off)<μγ and κΣτοιχεία[ν+off][1]==None:
							off += 1
					else:
						while (ν+off)>0 and κΣτοιχεία[ν+off][1]==None:
							off -= 1
							
					if (ν+off)<μγ and (ν+off)>0:
						for αν2 in κΣτοιχεία[ν+off][-1]:
							if σύνολο["μτλ"]==αν2['μέρος του λόγου']:
								if "ισότητες" in σύνολο:
									fc = [0,0]
									for k in σύνολο["ισότητες"]:
										if k in αν1 and k in αν2 and\
											αν1[k]==αν2[k]:
											fc[1]+=1
										fc[0]+=1
									if fc[0]==fc[1]:
										νέες_αναγνωρίσεις.append(αν1)
										addit = True
										break
								elif "επιλογές" in σύνολο and "συνθήκες" in σύνολο:
									fc = [0,0]
									for k,v in σύνολο["συνθήκες"].items():
										if αν2[k]==v:
											fc[1]+=1
										fc[0]+=1
									if fc[0]==fc[1]:
										for k,v in σύνολο["επιλογές"].items():
											if v.__class__==dict:
												for k2, v2 in v.items():
													if αν1[k][k2]==v2:
														fc[1]+=1
													fc[0]+=1
											else:
												if αν1[k]==v:
													fc[1]+=1
												fc[0]+=1
										if fc[0]==fc[1]:
											νέες_αναγνωρίσεις.append(αν1)
											addit = True
											break
								elif "επιλογές" in σύνολο and "συνθήκες" not in σύνολο:
									fc = [0,0]
									for k,v in σύνολο["επιλογές"].items():
										if v.__class__==dict:
											for k2, v2 in v.items():
												if αν1[k][k2]==v2:
													fc[1]+=1
												fc[0]+=1
										else:
											if αν1[k]==v:
												fc[1]+=1
											fc[0]+=1
									if fc[0]==fc[1]:
										νέες_αναγνωρίσεις.append(αν1)
										addit = True
										break
						if addit:
							break
			if νέες_αναγνωρίσεις:
				κΣτοιχεία[ν][-1] = νέες_αναγνωρίσεις
			ν+=1
				
	def _ανάλυσε(self, στοιχεία, διάλεκτος=None):
		κΣτοιχεία = []
		if not στοιχεία:
			return κΣτοιχεία
		if not διάλεκτος:
			διάλεκτος = self.διάλεκτος
		
		for στοιχείο in στοιχεία:
			αναγνωρίσεις = self.γραμματική._αναγνώριση._αναγνώριση(στοιχείο[1], self.γραμματική._δεδομένα, διάλεκτος)
			κΣτοιχεία.append([στοιχείο[0], στοιχείο[1], None, αναγνωρίσεις])
		self._ακολουθείες(κΣτοιχεία, διάλεκτος)
		
		ν = 0
		μγ = len(κΣτοιχεία)
		while ν<μγ:
			if not κΣτοιχεία[ν][2]:
				μτλ = []
				for αναγνώριση in κΣτοιχεία[ν][-1]:
					μτλ.append(αναγνώριση["μέρος του λόγου"])
				κΣτοιχεία[ν][2] = μτλ
			ν += 1
		return κΣτοιχεία
	
	def ανάλυσε(self, κείμενο, διάλεκτος=None, raw=False):
		if not κείμενο:
			return κείμενο
		if not διάλεκτος:
			return κείμενο
			
		στοιχεία = []
		acc = ""
		
		for γράμμα in κείμενο:
			if γράμμα in self.γ._δεδομένα.δ["στίξη"]:
				if acc:
					στοιχεία.append([acc, self.γραμματική.τ.κωδικοποιητής(acc)])
					στοιχεία.append([γράμμα, self.γραμματική.τ.κωδικοποιητής(γράμμα)])
					acc = ""
				else:
					στοιχεία.append([γράμμα, self.γραμματική.τ.κωδικοποιητής(γράμμα)])
			else:
				acc += γράμμα
		if acc:
			στοιχεία.append([acc, self.γραμματική.τ.κωδικοποιητής(acc)])
			
		κΣτοιχεία = self._ανάλυσε(στοιχεία, διάλεκτος)
		if not raw:
			νέα_στοιχεία = []
			for κΣτοιχείο in κΣτοιχεία:
				if κΣτοιχείο[1]==None:
					del κΣτοιχείο[1]
					νέα_στοιχεία.append(κΣτοιχείο)
				else:
					νστοιχείο = [κΣτοιχείο[0], κΣτοιχείο[2], []]
					for κ in deepcopy(κΣτοιχείο[-1]):
						if 'κΣυνθετικό' in κ:
							del κ['κΣυνθετικό']
						if 'κΑύξηση' in κ:
							del κ['κΑύξηση']
						if 'κΑύξηση παρακείμενου' in κ:
							del κ['κΑύξηση παρακείμενου']
						if 'κΕνεστωτική αύξηση' in κ:
							del κ['κΕνεστωτική αύξηση']
						if 'ανώμαλο' in κ:
							del κ['ανώμαλο'] 
						if 'κΛέξη' in κ:
							del κ['κΛέξη']
						if 'κΚατάληξη' in κ:
							del κ['κΚατάληξη']
						if 'συχνότητα' in κ:
							del κ['συχνότητα']
						if 'κατηγορία' in κ:
							del κ['κατηγορία']
						if 'συχνότητα' in κ:
							del κ['συχνότητα']
						if 'τονισμοί' in κ:
							del κ['τονισμοί']
						if 'ρήμα' in κ:
							del κ['ρήμα']
						if 'μετοχή' in κ:
							del κ['μετοχή']
						νστοιχείο[-1].append(κ)
						
					νέα_στοιχεία.append(νστοιχείο)
		else:
			νέα_στοιχεία = κΣτοιχεία
		
		return νέα_στοιχεία
	