#!/usr/bin/python3.2
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
μήκος = len
τύπωσε = print

class Σύνθεση():
	def __init__(self, γραμματική):
		self.γραμματική = γραμματική
		
	def σύνθεση(self, κΣτοιχεία, διάλεκτος=None):
		if not κΣτοιχεία:
			return ""
			
		νέο_κείμενο = []
		ν = 0
		μγ = len(κΣτοιχεία)
		while ν<μγ:
			αρχικό = κΣτοιχεία[ν][0]
			κΛέξη = κΣτοιχεία[ν][1]
			μτλ = κΣτοιχεία[ν][2]
			αναλύσεις = κΣτοιχεία[ν][3]
			if not μτλ or μτλ=="στίξη":
				νέο_κείμενο.append(αρχικό)
			elif "επίθετο"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]["κατάληξη"])
				else:
					επίθετο = self.γραμματική.επίθετα.κλίνε(αρχικό,  διάλεκτος=διάλεκτος)
					if επίθετο:
						νέο_κείμενο.append(επίθετο[0])
			elif "ουσιαστικό"==μτλ[0] and αναλύσεις[0].get("κατάληξη"):
				ουσιαστικό = αναλύσεις[0]["κατάληξη"]
				if "ανώμαλο" not in αναλύσεις[0]:
					ουσιαστικό = self.γραμματική.ουσιαστικά.κλίνε(αρχικό, διάλεκτος=διάλεκτος)
				if ουσιαστικό:
					if αρχικό[0]==αρχικό[0].capitalize()[0]:
						νέο_κείμενο.append(ουσιαστικό[0].capitalize())
					else:
						νέο_κείμενο.append(ουσιαστικό[0])
			elif "αντωνυμία"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]["κατάληξη"])
			elif "ρήμα"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]["κατάληξη"])
				else:
					ρήμα = None#self.γραμματική.ρήματα.κλίνε(κΣτοιχεία[ν][0])
					αναγνώριση = αναλύσεις[0]
					if αναγνώριση['χρόνος']=="μέλλοντας":
						ρήμα = self.γραμματική.ρήματα.μέλλοντας(αρχικό, αναγνώριση["φωνή"], 
									αναγνώριση["έγκλιση"], αναγνώριση["αριθμός"], αναγνώριση["πρόσωπο"], 
									αναγνώριση["διάλεκτος"])
					if ρήμα:
						νέο_κείμενο.append(ρήμα[0])
					else:
						νέο_κείμενο.append(αρχικό)
			elif "μετοχή"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]["κατάληξη"])
			elif "πρόθεση"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]['λήμμα'])
			elif "μόριο"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]['λήμμα'])
			elif "άρθρο"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]['κατάληξη'])
			elif "σύνδεσμος"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					if αρχικό[0]==αρχικό[0].capitalize()[0]:
						νέο_κείμενο.append(αναλύσεις[0]['λήμμα'].capitalize())
					else:
						νέο_κείμενο.append(αναλύσεις[0]['λήμμα'])
			elif "επίρρημα"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]['λήμμα'])
			elif "επιφώνημα"==μτλ[0]:
				if "ανώμαλο" in αναλύσεις[0]:
					νέο_κείμενο.append(αναλύσεις[0]['λήμμα'])
			ν+=1
					
		return " ".join(νέο_κείμενο)
