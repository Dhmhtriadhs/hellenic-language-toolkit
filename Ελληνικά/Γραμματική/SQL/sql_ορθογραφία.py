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

import time

τύπωσε = print
κείμενο = str
μήκος = len
εύρος = range

class Ορθογραφία():
	def __init__(self, sql):
		self.sql = sql
	
	def φόρτωση(self, ορθογραφία):
		ορθογραφία.clear()
		cur = self.sql.conn.cursor()
		σύνολα = cur.execute('select Κλειδί, Συγγραφέας, ὄνομα, '+
					'κεφαλαία, πνεύματα, τόνοι, αρχή, μέση, τέλος, εμπρός, πίσω from Ορθογραφία;')
		self.sql.conn.commit()
		for σύνολο in σύνολα:
			Κλειδί, Συγγραφέας, ὄνομα, κεφαλαία, πνεύματα, τόνοι, αρχή, μέση, τέλος, εμπρός, πίσω = σύνολο
			ορθογραφία[ὄνομα] = {}
			ορθογραφία[ὄνομα]["Συγγραφέας"] = Συγγραφέας
			ορθογραφία[ὄνομα]["Κλειδί"] = Κλειδί
			ορθογραφία[ὄνομα]["όνομα"] = ὄνομα
			ορθογραφία[ὄνομα]["κεφαλαία"] = κεφαλαία
			ορθογραφία[ὄνομα]["πνεύματα"] = πνεύματα
			ορθογραφία[ὄνομα]["τόνοι"] = τόνοι
			ορθογραφία[ὄνομα]["αρχή"] = eval(αρχή)
			ορθογραφία[ὄνομα]["μέση"] = eval(μέση)
			ορθογραφία[ὄνομα]["τέλος"] = eval(τέλος)
			ορθογραφία[ὄνομα]["εμπρός"] = εμπρός
			ορθογραφία[ὄνομα]["πίσω"] = πίσω
		
	def νέα(self, αναγνώριση, ορθογραφία):
		Κλειδί = αναγνώριση.get("Κλειδί")
		ὄνομα = αναγνώριση.get("όνομα")
		Συγγραφέας = αναγνώριση.get("Συγγραφέας")
		if not Συγγραφέας:
			Συγγραφέας = "admin"
		if not ὄνομα:
			return
		# Αν υπάρχει ΑΑ, προσθήκη ετικέτας «ανενεργό» στο παλιό
		# Αν υπάρχει Όνομα, προσθήκη ετικέτας «ανενεργό» στο παλιό
		# Αν δεν υπάρχει ΑΑ δημιουργία καινούργιου
		cur = self.sql.conn.cursor()
		if Κλειδί:
			cur.execute('update Ορθογραφία set '+
				'Συγγραφέας=?, ὄνομα=?, κεφαλαία=?, πνεύματα=?, τόνοι=?, '+
				'αρχή=?, μέση=?, τέλος=?, εμπρός=?, πίσω=? where Κλειδί=?;', 
				(Συγγραφέας, ὄνομα, 
				αναγνώριση["κεφαλαία"], αναγνώριση["πνεύματα"], 
				αναγνώριση["τόνοι"], str(αναγνώριση["αρχή"]), 
				str(αναγνώριση["μέση"]), str(αναγνώριση["τέλος"]),
				αναγνώριση["εμπρός"], αναγνώριση["πίσω"],  
				Κλειδί))
		else:
			cur.execute('insert into Ορθογραφία '+
				'(Συγγραφέας, ὄνομα, κεφαλαία, πνεύματα, τόνοι, '+
				'αρχή, μέση, τέλος, εμπρός, πίσω) values '+
				'(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', 
				(Συγγραφέας, ὄνομα, 
				αναγνώριση["κεφαλαία"], αναγνώριση["πνεύματα"], 
				αναγνώριση["τόνοι"], str(αναγνώριση["αρχή"]), 
				str(αναγνώριση["μέση"]), str(αναγνώριση["τέλος"]),
				αναγνώριση["εμπρός"], αναγνώριση["πίσω"]))
		self.sql.conn.commit()
		self.φόρτωση(ορθογραφία)
		
	def διαγραφή(self, αναγνώριση, ορθογραφία):
		cur = self.sql.conn.cursor()
		Κλειδί = αναγνώριση["Κλειδί"]
		cur.execute('delete from Ορθογραφία where Κλειδί=?;', (Κλειδί, ))
		self.φόρτωση(ορθογραφία)
		
		self.sql.conn.commit()
		