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

class Μεταδεδομένα():
	def __init__(self, sql):
		self.sql = sql

	def νέα(self, αναγνώριση, μεταδεδομένα):
		διάλεκτος = αναγνώριση["διάλεκτος"]
		νέα_μέτα = []
		για_διαγραφή = []
		for ὄνομα, τιμές in αναγνώριση["Μεταδεδομένα"].items():
			if διάλεκτος in μεταδεδομένα:
				for μέτα in μεταδεδομένα[διάλεκτος]:
					if not μέτα:
						continue
					if μέτα["ὄνομα"]==ὄνομα and μέτα["τιμές"]==τιμές:
						νέα_μέτα.append(μέτα["ΑΑ"])
						για_διαγραφή.append(ὄνομα)
						break
		for κλειδί in για_διαγραφή:
			del αναγνώριση["Μεταδεδομένα"][κλειδί]
		if len(αναγνώριση["Μεταδεδομένα"])>0:
			cur = self.sql.conn.cursor()
			for ὄνομα, τιμές in αναγνώριση["Μεταδεδομένα"].items():
				ΑΑ = 1
				cur.execute('select max(ΑΑ) from Μεταδεδομένα where Διάλεκτος=?;', (διάλεκτος, ))
				for c in cur:
					if c and c[0]:
						ΑΑ = c[0]+1
				νέο_σύνολο = {"ΑΑ":ΑΑ, "Συγγραφέας":"admin",
					"διάλεκτος":διάλεκτος, "Παρατηρήσεις":None,
					"ἐτικέτες":"τρέχον, ", "ὄνομα":ὄνομα, "τιμές":τιμές}
				self.__αποθήκευση(νέο_σύνολο)
				νέα_μέτα.append(ΑΑ)
			
			self.sql.conn.commit()
			self.φόρτωση(μεταδεδομένα)
		αναγνώριση["Μεταδεδομένα"] = νέα_μέτα
	
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
			
		# Υποχρεωτικά
		ΑΑ = σύνολο["ΑΑ"]
		Διάλεκτος = σύνολο["διάλεκτος"]
		ὄνομα = σύνολο["ὄνομα"]
		τιμές = str(σύνολο["τιμές"])
		
		cur = self.sql.conn.cursor()
		cur.execute('insert into Μεταδεδομένα (ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, '+
				'Ἐτικέτες, ὄνομα, τιμές, Παρατηρήσεις) '+
			'values (?, ?, ?, ?, ?, ?, ?, ?)', 
			(ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, ὄνομα, τιμές, Παρατηρήσεις))
			
	def τρέχον(self, αναγνώριση, καταλήξεις):
		#self.sql.open()
		
		ΑΑ = αναγνώριση["ΑΑ"]
		Κλειδί = αναγνώριση["Κλειδί"]
		μτλ = αναγνώριση["μέρος του λόγου"]
		διάλεκτος = αναγνώριση["διάλεκτος"]
		χρόνος = αναγνώριση.get("χρόνος")
		σετ = []
		τρέχον = None
		cur = self.sql.conn.cursor()
		for σύνολο in cur.execute(
			'select Κλειδί, Ἐτικέτες from Μεταδεδομένα where ΑΑ=? and μέρος_του_λόγου=? and Διάλεκτος=? and (Χρόνος=? or Χρόνος is null);', 
			(ΑΑ, μτλ, διάλεκτος, χρόνος)):
			if σύνολο and σύνολο[0]!=Κλειδί:
				σετ.append([σύνολο[0], σύνολο[1]])
			elif σύνολο[0]==Κλειδί:
				τρέχον = σύνολο[1]
		for σ in σετ:
			if "τρέχον" in σ[1]:
				cur.execute('update Μεταδεδομένα set Ἐτικέτες=? where Κλειδί=?;', (σ[1].replace("τρέχον", "ανενεργό"), σ[0]))
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
			cur.execute('update Μεταδεδομένα set Ἐτικέτες=? where Κλειδί=?;', 
							(", ".join(νέο_τρέχον), Κλειδί))
		self.φόρτωση(καταλήξεις)
		self.sql.conn.commit()
		#self.sql.close()
	
	def διαγραφή(self, αναγνώριση, τονισμοί):
		#self.sql.open()
		cur = self.sql.conn.cursor()
		Κλειδί = αναγνώριση["Κλειδί"]
		σετ = []
		for σύνολο in cur.execute('select Ἐτικέτες from Μεταδεδομένα where Κλειδί=?;', (Κλειδί, )):
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
				cur.execute('update Μεταδεδομένα set Ἐτικέτες=? where Κλειδί=?;', (σ, Κλειδί))
		self.φόρτωση(τονισμοί)
		
		self.sql.conn.commit()
		#self.sql.close()

	def φόρτωση(self, μεταδεδομένα, όλα=False):
		μεταδεδομένα.clear()
		cur = self.sql.conn.cursor()
		if όλα:
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, '+
				'Ἐτικέτες, ὄνομα, τιμές, Παρατηρήσεις from Μεταδεδομένα as p '+
				'WHERE Ἡμερομηνία=(SELECT MAX(Ἡμερομηνία) FROM Μεταδεδομένα '+
				'WHERE Διάλεκτος=p.Διάλεκτος and ΑΑ=p.ΑΑ);')
		else:
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, '+
				'Ἐτικέτες, ὄνομα, τιμές, Παρατηρήσεις from Μεταδεδομένα as p '+
				'WHERE Ἐτικέτες LIKE "%τρέχον%" AND Ἡμερομηνία=(SELECT MAX(Ἡμερομηνία) FROM '+
				'Μεταδεδομένα WHERE Διάλεκτος=p.Διάλεκτος and ΑΑ=p.ΑΑ);')
		self.sql.conn.commit()
		for σύνολο in σύνολα:
			Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, ὄνομα, τιμές, Παρατηρήσεις = σύνολο
			
			δεδομένο = {}
			δεδομένο["Κλειδί"] = Κλειδί
			δεδομένο["ΑΑ"] = ΑΑ
			δεδομένο["διάλεκτος"] = Διάλεκτος
			δεδομένο["Ἡμερομηνία"] = Ἡμερομηνία
			δεδομένο["Συγγραφέας"] = Συγγραφέας
			δεδομένο["ἐτικέτες"] = Ἐτικέτες
			δεδομένο["ὄνομα"] = ὄνομα
			δεδομένο["τιμές"] = eval(τιμές)
			δεδομένο["Παρατηρήσεις"] = Παρατηρήσεις
			
			if Διάλεκτος not in μεταδεδομένα:
				μεταδεδομένα[Διάλεκτος] = []
			while ΑΑ>=len(μεταδεδομένα[Διάλεκτος]):
				μεταδεδομένα[Διάλεκτος].append({})
			μεταδεδομένα[Διάλεκτος][ΑΑ] = δεδομένο
	
	def ιστορικό(self, αναγνώριση):
		#self.sql.open()
		αποτέλεσμα = []
		ΑΑ = αναγνώριση["ΑΑ"]
		if ΑΑ:
			cur = self.sql.conn.cursor()
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, '+
				'Ἐτικέτες, μέρος_του_λόγου, Χρόνος, καταλήξεις, συχνότητες, Παρατηρήσεις from Μεταδεδομένα as p '+
				'WHERE ΑΑ=? and Διάλεκτος=? and μέρος_του_λόγου=? and (Χρόνος=? or Χρόνος is null);', 
				(ΑΑ, αναγνώριση["διάλεκτος"], αναγνώριση["μέρος του λόγου"], αναγνώριση.get("χρόνος")))
			for σύνολο in σύνολα:
				Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, μέρος_του_λόγου, Χρόνος, καταλήξεις, συχνότητες, Παρατηρήσεις = σύνολο
			
				κατάληξη = {}
				κατάληξη["Κλειδί"] = Κλειδί
				κατάληξη["ΑΑ"] = ΑΑ
				κατάληξη["διάλεκτος"] = Διάλεκτος
				κατάληξη["Ἡμερομηνία"] = Ἡμερομηνία
				κατάληξη["Συγγραφέας"] = Συγγραφέας
				κατάληξη["ἐτικέτες"] = Ἐτικέτες
				κατάληξη["μέρος του λόγου"] = μέρος_του_λόγου
				κατάληξη["καταλήξεις"] = eval(καταλήξεις)
				κατάληξη["συχνότητες"] = eval(συχνότητες)
				κατάληξη["Παρατηρήσεις"] = Παρατηρήσεις
				
				if Χρόνος:
					κατάληξη["χρόνος"] = Χρόνος
				αποτέλεσμα.append(κατάληξη)
			self.sql.conn.commit()
		#self.sql.close()
		return αποτέλεσμα
		