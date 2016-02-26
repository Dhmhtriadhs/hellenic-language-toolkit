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


import os
from multiprocessing import Process, Pipe
if "Γραμματική" in os.getcwd():
	# Κλητά
	from Ουσιαστικά import Ουσιαστικά
	from Επίθετα    import Επίθετα
	from Ρήματα import Ρήματα
	from Μετοχές import Μετοχές
	# Άκλητα(=δεν προσθέτουμε λέξεις)
	from Άρθρα      import Άρθρα
	from Αντωνυμίες import Αντωνυμίες
	from Άκλητα     import Άκλητα
	from Επιρρήματα import Επιρρήματα
	import δεδομένα, ευρετήρια, αναγνώριση
	from Τονιστής   import Τονιστής
else:
	# Κλητά
	from Ελληνικά.Γραμματική.Ουσιαστικά import Ουσιαστικά
	from Ελληνικά.Γραμματική.Επίθετα    import Επίθετα
	from Ελληνικά.Γραμματική.Ρήματα import Ρήματα
	from Ελληνικά.Γραμματική.Μετοχές import Μετοχές
	# Άκλητα
	from Ελληνικά.Γραμματική.Άρθρα      import Άρθρα
	from Ελληνικά.Γραμματική.Αντωνυμίες import Αντωνυμίες
	from Ελληνικά.Γραμματική.Επιρρήματα import Επιρρήματα
	
	import Ελληνικά.Γραμματική.αναγνώριση as αναγνώριση
	import Ελληνικά.Γραμματική.εκτίμηση as εκτίμηση
	
class Γραμματική():
	def __init__(self, δεδομένα, τονιστής, develop=None):
		self.τ = τονιστής
		self._δεδομένα = δεδομένα
		self._αναγνώριση = αναγνώριση.Αναγνώριση(self.τ, self._δεδομένα.δ["διάλεκτοι"])
		self._εκτίμηση = εκτίμηση.Εκτίμηση(self.τ, self._δεδομένα.δ["διάλεκτοι"])
		
		self.α  = Άρθρα(self.τ, self._δεδομένα, self._αναγνώριση)
		self.αν = Αντωνυμίες(self.τ, self._δεδομένα, self._αναγνώριση)
		self.επ = Επιρρήματα(self.τ, self._αναγνώριση)
		self.ο  = Ουσιαστικά(self.τ, self._δεδομένα, self._αναγνώριση)
		self.ε  = Επίθετα(self.τ, self._δεδομένα, self._αναγνώριση)
		self.ρ  = Ρήματα(self.τ, self._δεδομένα, self._αναγνώριση)
		self.μ  = Μετοχές(self.τ, self._δεδομένα, self._αναγνώριση, self.ρ)
		
		self.άρθρα = self.α
		self.ουσιαστικά = self.ο
		self.επίθετα    = self.ε
		self.αντωνυμίες = self.αν
		self.επιρρήματα = self.επ
		self.ρήματα  = self.ρ
		self.μετοχές  = self.μ
		
		self.στίξη = {
			",":"κόμμα", " ":"κενό", ".":"τελεία", 
			"·":"άνω τελεία", "-":"ενωτικό"}
	
	def αναγνώριση(self, λέξη, διάλεκτος=None):
		return self._αναγνώριση.αναγνώριση(λέξη, self._δεδομένα, διάλεκτος)
	
if __name__ == "__main__":
	γραμματική = Γραμματική("δημοτική", True)
	
	
		