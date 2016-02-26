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

import os, sqlite3
if 'Ελληνικά' in os.path.abspath('.').split("/")[-1]:
	φάκελος = os.path.join(".","Γραμματική")
elif 'δοκιμές' in os.path.abspath('.'):
	φάκελος = '..'
elif 'src' in os.path.abspath('.')[-3:]:
	φάκελος = 'Ελληνικά'
else:
	φάκελος = '.'
τύπωσε = print
κείμενο = str
μήκος = len
εύρος = range
print(os.path.abspath('.'))
from Ελληνικά.Γραμματική.SQL.sql_διάλεκτοι import Διάλεκτοι
from Ελληνικά.Γραμματική.SQL.sql_τονισμοί import Τονισμοί
from Ελληνικά.Γραμματική.SQL.sql_καταλήξεις import Καταλήξεις
from Ελληνικά.Γραμματική.SQL.sql_ανώμαλα import Ανώμαλα
from Ελληνικά.Γραμματική.SQL.sql_μεταδεδομένα import Μεταδεδομένα
from Ελληνικά.Γραμματική.SQL.sql_κλίμακες import Κλίμακες
from Ελληνικά.Γραμματική.SQL.sql_ουσιαστικά import Ουσιαστικά
from Ελληνικά.Γραμματική.SQL.sql_επίθετα import Επίθετα
from Ελληνικά.Γραμματική.SQL.sql_κατηγοριοτονισμοί import Κατηγοριοτονισμοί
from Ελληνικά.Γραμματική.SQL.sql_ομάδες import Ομάδες
from Ελληνικά.Γραμματική.SQL.sql_θέματα import Θέματα
from Ελληνικά.Γραμματική.SQL.sql_ορθογραφία import Ορθογραφία

class Δεδομένα():
	def __init__(self, τονιστής):
		self.τ = τονιστής
		self.conn = None
		self.open()
		self.διάλεκτοι = Διάλεκτοι(self)
		self.τονισμοί = Τονισμοί(self)
		self.μεταδεδομένα = Μεταδεδομένα(self)
		self.κλίμακες = Κλίμακες(self)
		self.καταλήξεις = Καταλήξεις(self, self.τ)
		self.ανώμαλα = Ανώμαλα(self, self.τ)
		self.ουσιαστικά = Ουσιαστικά(self, self.τ)
		self.επίθετα = Επίθετα(self, self.τ)
		self.κατηγοριοτονισμοί = Κατηγοριοτονισμοί(self)
		self.ομάδες = Ομάδες(self)
		self.θέματα = Θέματα(self, self.τ)
		self.ορθογραφία = Ορθογραφία(self)
	
	def open(self):
		self.conn = sqlite3.connect(os.path.join(φάκελος, "Ελληνικά", "δεδομένα", "HLT_multi.db"), check_same_thread=False)
		
	def close(self):
		self.conn.close()

	def επαναφόρτωση(self, δεδομένα):
		"""Επαναφόρτωση των κατηγοριών των ρημμάτων και των λημμάτων."""

		self.διάλεκτοι.φόρτωση(δεδομένα["διάλεκτοι"])
		self.ορθογραφία.φόρτωση(δεδομένα["ορθογραφία"])
		
		self.μεταδεδομένα.φόρτωση(δεδομένα["μεταδεδομένα"])
		self.κλίμακες.φόρτωση(δεδομένα["κλίμακες"])
		self.ανώμαλα.φόρτωση(δεδομένα["ανώμαλα"], δεδομένα["μεταδεδομένα"], δεδομένα["κλίμακες"])
		
		self.τονισμοί.φόρτωση(δεδομένα["τονισμοί"])
		self.καταλήξεις.φόρτωση(δεδομένα["καταλήξεις"])
		self.κατηγοριοτονισμοί.φόρτωση(δεδομένα["κατηγοριοτονισμoί"], 
												δεδομένα["καταλήξεις"], δεδομένα["τονισμοί"])
		self.ομάδες.φόρτωση(δεδομένα["ομάδες"], δεδομένα["κατηγοριοτονισμoί"])
		
		δεδομένα["θέματα"] = []
		self.θέματα.φόρτωση(δεδομένα["θέματα"], δεδομένα["μεταδεδομένα"], 
				δεδομένα["κλίμακες"], δεδομένα["ομάδες"],
				δεδομένα["διάλεκτοι"])
		self.ουσιαστικά.φόρτωση(δεδομένα["θέματα"], δεδομένα["μεταδεδομένα"], 
				δεδομένα["κλίμακες"], δεδομένα["κατηγοριοτονισμoί"]["ουσιαστικό"], 
				δεδομένα["καταλήξεις"]["ουσιαστικό"], δεδομένα["τονισμοί"]["ουσιαστικό"],
				δεδομένα["διάλεκτοι"])
		self.επίθετα.φόρτωση(δεδομένα["θέματα"], δεδομένα["μεταδεδομένα"], 
				δεδομένα["κλίμακες"], δεδομένα["κατηγοριοτονισμoί"]["επίθετο"], 
				δεδομένα["καταλήξεις"]["επίθετο"], δεδομένα["τονισμοί"]["επίθετο"],
				δεδομένα["διάλεκτοι"])
		