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

class Διάλεκτοι():
	def __init__(self, sql):
		self.sql = sql
	
	def φόρτωση(self, διάλεκτοι, όλα=False):
		διάλεκτοι.clear()
		cur = self.sql.conn.cursor()
		if όλα:
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, Ὄνομα, '+
					'Εικονική, Δυϊκός, Δοτική, Πτώσεις, Ῥῆμα, Μετοχή, Ἐπεκτάσεις, Παρατηρήσεις from Διάλεκτοι as p '+
					'WHERE Ἡμερομηνία=(SELECT MAX(Ἡμερομηνία) FROM '+
					'Διάλεκτοι WHERE ΑΑ=p.ΑΑ);')
		else:
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, Ὄνομα, '+
					'Εικονική, Δυϊκός, Δοτική, Πτώσεις, Ῥῆμα, Μετοχή, Ἐπεκτάσεις, Παρατηρήσεις from Διάλεκτοι as p '+
					'WHERE Ἐτικέτες LIKE "%τρέχον%" AND Ἡμερομηνία=(SELECT MAX(Ἡμερομηνία) FROM '+
					'Διάλεκτοι WHERE ΑΑ=p.ΑΑ);')
		self.sql.conn.commit()
		for σύνολο in σύνολα:
			Κλειδί, ΑΑ, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, Ὄνομα, Εικονική, Δυϊκός, Δοτική, Πτώσεις, Ῥῆμα, Μετοχή, Ἐπεκτάσεις, Παρατηρήσεις = σύνολο
			διάλεκτοι[Ὄνομα] = {}
			διάλεκτοι[Ὄνομα]["Συγγραφέας"] = Συγγραφέας
			διάλεκτοι[Ὄνομα]["ἐτικέτες"] = Ἐτικέτες
			διάλεκτοι[Ὄνομα]["ΑΑ"] = ΑΑ
			διάλεκτοι[Ὄνομα]["Κλειδί"] = Κλειδί
			διάλεκτοι[Ὄνομα]["όνομα"] = Ὄνομα
			διάλεκτοι[Ὄνομα]["εικονική"] = Εικονική
			διάλεκτοι[Ὄνομα]["Παρατηρήσεις"] = Παρατηρήσεις
			διάλεκτοι[Ὄνομα]["Ἡμερομηνία"] = Ἡμερομηνία
			διάλεκτοι[Ὄνομα]["πτώσεις"] = eval(Πτώσεις)
			διάλεκτοι[Ὄνομα]["δυϊκός"] = int(Δυϊκός)
			διάλεκτοι[Ὄνομα]["δοτική"] = Δοτική
			if διάλεκτοι[Ὄνομα]["δυϊκός"]:
				διάλεκτοι[Ὄνομα]["πρόσωπα"] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
			else:
				διάλεκτοι[Ὄνομα]["πρόσωπα"] = [0, 1, 2, 6, 7, 8]
			διάλεκτοι[Ὄνομα]["ρήμα"] = eval(Ῥῆμα)
			διάλεκτοι[Ὄνομα]["μετοχή"] = eval(Μετοχή)
			διάλεκτοι[Ὄνομα]["επεκτάσεις"] = eval(Ἐπεκτάσεις)
		#if close:
		#	self.sql.close()
		
	def νέα(self, αναγνώριση, διάλεκτοι):
		#self.sql.open()
		
		όνομα = αναγνώριση.get("όνομα")
		ΑΑ = αναγνώριση.get("ΑΑ")
		# Αν υπάρχει ΑΑ, προσθήκη ετικέτας «ανενεργό» στο παλιό
		# Αν υπάρχει Όνομα, προσθήκη ετικέτας «ανενεργό» στο παλιό
		# Αν δεν υπάρχει ΑΑ δημιουργία καινούργιου
		cur = self.sql.conn.cursor()
		if όνομα:
			σετ = {}
			if ΑΑ:
				for σύνολο in cur.execute('select Κλειδί, Ἐτικέτες from Διάλεκτοι where ΑΑ=?;', (ΑΑ, )):
					if σύνολο:
						σετ[σύνολο[0]] = σύνολο[1]
			for σύνολο in cur.execute('select Κλειδί, Ἐτικέτες, ΑΑ from Διάλεκτοι where Ὄνομα=?;', (όνομα, )):
				if σύνολο:
					σετ[σύνολο[0]] = σύνολο[1]
					αναγνώριση["ΑΑ"] = σύνολο[2]
					ΑΑ = αναγνώριση["ΑΑ"]
				else:
					ΑΑ = None
			for k,v in σετ.items():
				if "τρέχον" in v:
					cur.execute('update Διάλεκτοι set Ἐτικέτες=? where Κλειδί=?;', (v.replace("τρέχον", "ανενεργό"), k))
		if ΑΑ in [None, 0]:
			αναγνώριση["ΑΑ"] = 1
			cur.execute('select max(ΑΑ) from Διάλεκτοι;')
			for c in cur:
				if c and c[0]:
					αναγνώριση["ΑΑ"] = c[0]+1
			
		self.__αποθήκευση(αναγνώριση)
		self.sql.conn.commit()
		self.φόρτωση(διάλεκτοι)
		#self.sql.close()
	
	def __αποθήκευση(self, σύνολο):
		# Προαιρετικά
		Ἡμερομηνία = σύνολο.get("Ἡμερομηνία")
		if not Ἡμερομηνία:
			Ἡμερομηνία = time.strftime("%Y%m%d%H%M%S")
		Συγγραφέας = σύνολο.get("Συγγραφέας")
		if not Συγγραφέας:
			Συγγραφέας = "admin"
		Ἐτικέτες = σύνολο.get("ἐτικέτες")
		if not Ἐτικέτες:
			Ἐτικέτες = "τρέχον, "
		Παρατηρήσεις = σύνολο.get("Παρατηρήσεις")
		if not Παρατηρήσεις:
			Παρατηρήσεις = ""
		Εικονική = σύνολο.get("εικονική")
		Ἐπεκτάσεις = σύνολο.get("επεκτάσεις")
		# Υποχρεωτικά
		ΑΑ = σύνολο["ΑΑ"]
		Ὄνομα = σύνολο["όνομα"]
		Δυϊκός = σύνολο["δυϊκός"]
		Δοτική = σύνολο["δοτική"]
		Πτώσεις = σύνολο["πτώσεις"] 
		Ῥῆμα = σύνολο["ρήμα"]
		Μετοχή = σύνολο["μετοχή"]
		cur = self.sql.conn.cursor()
		cur.execute('insert into Διάλεκτοι (ΑΑ, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, '+
			'Ὄνομα, Εικονική, Δυϊκός, Δοτική, Πτώσεις, Ῥῆμα, Μετοχή, Ἐπεκτάσεις, Παρατηρήσεις) '+
			'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
			(ΑΑ, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, Ὄνομα, Εικονική, Δυϊκός, Δοτική, str(Πτώσεις), 
			str(Ῥῆμα), str(Μετοχή), str(Ἐπεκτάσεις), Παρατηρήσεις))
		
	def διαγραφή(self, αναγνώριση, διάλεκτοι):
		#self.sql.open()
		cur = self.sql.conn.cursor()
		Κλειδί = αναγνώριση["Κλειδί"]
		σετ = []
		for σύνολο in cur.execute('select Ἐτικέτες from Διάλεκτοι where Κλειδί=?;', (Κλειδί, )):
			if σύνολο:
				σετ.append(σύνολο[0])
		for σ in σετ:
			up = False
			if "διαγραμμένο" in σ:
				up = False
			elif "τρέχον" in σ:
				σ=σ.replace("τρέχον", "διαγραμμένο")
				up = True
			elif "ανενεργό" in σ:
				σ=σ.replace("ανενεργό", "διαγραμμένο")
				up = True
			if up:
				cur.execute('update Διάλεκτοι set Ἐτικέτες=? where Κλειδί=?;', (σ, Κλειδί))
		self.φόρτωση(διάλεκτοι)
		
		self.sql.conn.commit()
		#self.sql.close()
		
	def ιστορικό(self, αναγνώριση):
		#self.sql.open()
		αποτέλεσμα = []
		ΑΑ = αναγνώριση.get("ΑΑ")
		if ΑΑ:
			cur = self.sql.conn.cursor()
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, Ὄνομα, '+
					'Εικονική, Δυϊκός, Δοτική, Πτώσεις, Ῥῆμα, Μετοχή, Ἐπεκτάσεις, Παρατηρήσεις from Διάλεκτοι as p '+
					'WHERE ΑΑ=?;', (ΑΑ,))
			self.sql.conn.commit()
			for σύνολο in σύνολα:
				Κλειδί, ΑΑ, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, Ὄνομα, Εικονική, Δυϊκός, Δοτική, Πτώσεις, Ῥῆμα, Μετοχή, Ἐπεκτάσεις, Παρατηρήσεις = σύνολο
				διάλεκτοι = {}
				διάλεκτοι["Συγγραφέας"] = Συγγραφέας
				διάλεκτοι["ἐτικέτες"] = Ἐτικέτες
				διάλεκτοι["ΑΑ"] = ΑΑ
				διάλεκτοι["Κλειδί"] = Κλειδί
				διάλεκτοι["όνομα"] = Ὄνομα
				διάλεκτοι["εικονική"] = Εικονική
				διάλεκτοι["Παρατηρήσεις"] = Παρατηρήσεις
				διάλεκτοι["Ἡμερομηνία"] = Ἡμερομηνία
				διάλεκτοι["πτώσεις"] = eval(Πτώσεις)
				διάλεκτοι["δυϊκός"] = Δυϊκός
				διάλεκτοι["δοτική"] = Δοτική
				διάλεκτοι["ρήμα"] = eval(Ῥῆμα)
				διάλεκτοι["μετοχή"] = eval(Μετοχή)
				διάλεκτοι["επεκτάσεις"] = eval(Ἐπεκτάσεις)
				αποτέλεσμα.append(διάλεκτοι)
		self.sql.conn.commit()
		#self.sql.close()
		return αποτέλεσμα
	
	def τρέχον(self, αναγνώριση, διάλεκτοι):
		#self.sql.open()
		
		ΑΑ = αναγνώριση["ΑΑ"]
		Κλειδί = αναγνώριση["Κλειδί"]
		σετ = []
		τρέχον = None
		cur = self.sql.conn.cursor()
		for σύνολο in cur.execute('select Κλειδί, Ἐτικέτες from Διάλεκτοι where ΑΑ=?;', (ΑΑ, )):
			if σύνολο and σύνολο[0]!=Κλειδί:
				σετ.append([σύνολο[0], σύνολο[1]])
			elif σύνολο[0]==Κλειδί:
				τρέχον = σύνολο[1]
		for σ in σετ:
			if "τρέχον" in σ[1]:
				cur.execute('update Διάλεκτοι set Ἐτικέτες=? where Κλειδί=?;', (σ[1].replace("τρέχον", "ανενεργό"), σ[0]))
		if τρέχον:
			if "ανενεργό" in τρέχον:
				τρέχον = τρέχον.replace("ανενεργό", "")
			if "διαγραμμένο" in τρέχον:
				τρέχον = τρέχον.replace("διαγραμμένο", "")
			νέο_τρέχον = []
			for σ in τρέχον.split(","):
				σσ = σ.strip()
				if σσ:
					νέο_τρέχον.append(σσ)
			νέο_τρέχον.append("τρέχον")
			cur.execute('update Διάλεκτοι set Ἐτικέτες=? where Κλειδί=?;', 
							(", ".join(νέο_τρέχον), Κλειδί))
		self.φόρτωση(διάλεκτοι)
		self.sql.conn.commit()
		#self.sql.close()
		