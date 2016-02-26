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

class Τονισμοί():
	def __init__(self, sql):
		self.sql = sql
		
	def νέος(self, αναγνώριση, τονισμοί):
		#self.sql.open()
		διάλεκτος = αναγνώριση["διάλεκτος"]
		μτλ = αναγνώριση["μέρος του λόγου"]
		ΑΑ = αναγνώριση.get("ΑΑ")
		cur = self.sql.conn.cursor()
		σετ = {}
		if ΑΑ:
			for σύνολο in cur.execute(
				'select Κλειδί, Ἐτικέτες from Τονισμοί where ΑΑ=? and Διάλεκτος=? and μέρος_του_λόγου=?;', 
				(ΑΑ, διάλεκτος, μτλ)):
				if σύνολο:
						σετ[σύνολο[0]] = σύνολο[1]
			for k,v in σετ.items():
				if "τρέχον" in v:
					cur.execute(
					'update Τονισμοί set Ἐτικέτες=? where Κλειδί=?;', 
						(v.replace("τρέχον", "ανενεργό"), k))
		else:
			αναγνώριση["ΑΑ"] = 1
			cur.execute(
				'select max(ΑΑ) from Τονισμοί where Διάλεκτος=? and μέρος_του_λόγου=?;', 
					(διάλεκτος, μτλ))
			for c in cur:
				if c and c[0]:
					αναγνώριση["ΑΑ"] = c[0]+1
			
		self.__αποθήκευση(αναγνώριση)
		self.sql.conn.commit()
		self.φόρτωση(τονισμοί)
		#self.sql.close()
		
		return αναγνώριση["ΑΑ"]
	
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
		μέρος_του_λόγου = σύνολο["μέρος του λόγου"]
		τονισμοί = σύνολο["τονισμοί"]
		cur = self.sql.conn.cursor()
		cur.execute('insert into Τονισμοί (ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, '+
			'μέρος_του_λόγου, τονισμοί, Παρατηρήσεις) '+
			'values (?, ?, ?, ?, ?, ?, ?, ?)', 
			(ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, μέρος_του_λόγου, str(τονισμοί), Παρατηρήσεις))
	
	def ιστορικό(self, αναγνώριση):
		αποτέλεσμα = []
		ΑΑ = αναγνώριση["ΑΑ"]
		if ΑΑ:
			cur = self.sql.conn.cursor()
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, '+
				'Ἐτικέτες, μέρος_του_λόγου, τονισμοί, Παρατηρήσεις from Τονισμοί '+
				'WHERE ΑΑ=? and Διάλεκτος=? and μέρος_του_λόγου=?;', 
				(ΑΑ, αναγνώριση["διάλεκτος"], αναγνώριση["μέρος του λόγου"]))
			for σύνολο in σύνολα:
				Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, μέρος_του_λόγου, τόνοι, Παρατηρήσεις = σύνολο
				τονισμός = {}
				τονισμός["Κλειδί"] = Κλειδί
				τονισμός["ΑΑ"] = ΑΑ
				τονισμός["διάλεκτος"] = Διάλεκτος
				τονισμός["Συγγραφέας"] = Συγγραφέας
				τονισμός["Ἡμερομηνία"] = Ἡμερομηνία
				τονισμός["ἐτικέτες"] = Ἐτικέτες
				τονισμός["μέρος του λόγου"] = μέρος_του_λόγου
				τονισμός["τονισμοί"] = eval(τόνοι)
				τονισμός["Παρατηρήσεις"] = Παρατηρήσεις
				αποτέλεσμα.append(τονισμός)
			self.sql.conn.commit()
		#self.sql.close()
		return αποτέλεσμα
	
	def τρέχον(self, αναγνώριση, τονισμοί):
		#self.sql.open()
		
		ΑΑ = αναγνώριση["ΑΑ"]
		Κλειδί = αναγνώριση["Κλειδί"]
		μτλ = αναγνώριση["μέρος του λόγου"]
		διάλεκτος = αναγνώριση["διάλεκτος"]
		σετ = []
		τρέχον = None
		cur = self.sql.conn.cursor()
		for σύνολο in cur.execute('select Κλειδί, Ἐτικέτες from Τονισμοί where ΑΑ=? and μέρος_του_λόγου=? and Διάλεκτος=?;', 
										(ΑΑ, μτλ, διάλεκτος)):
			if σύνολο and σύνολο[0]!=Κλειδί:
				σετ.append([σύνολο[0], σύνολο[1]])
			elif σύνολο[0]==Κλειδί:
				τρέχον = σύνολο[1]
		for σ in σετ:
			if "τρέχον" in σ[1]:
				cur.execute('update Τονισμοί set Ἐτικέτες=? where Κλειδί=?;', (σ[1].replace("τρέχον", "ανενεργό"), σ[0]))
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
			cur.execute('update Τονισμοί set Ἐτικέτες=? where Κλειδί=?;', 
							(", ".join(νέο_τρέχον), Κλειδί))
		self.φόρτωση(τονισμοί)
		self.sql.conn.commit()
		#self.sql.close()
		
	def διαγραφή(self, αναγνώριση, τονισμοί):
		#self.sql.open()
		cur = self.sql.conn.cursor()
		Κλειδί = αναγνώριση["Κλειδί"]
		σετ = []
		for σύνολο in cur.execute('select Ἐτικέτες from Τονισμοί where Κλειδί=?;', (Κλειδί, )):
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
				cur.execute('update Τονισμοί set Ἐτικέτες=? where Κλειδί=?;', (σ, Κλειδί))
		self.φόρτωση(τονισμοί)
		
		self.sql.conn.commit()
		#self.sql.close()
		
	def φόρτωση(self, τονισμοί, όλα=False):
		τονισμοί.clear()
		close=False
		
		cur = self.sql.conn.cursor()
		if όλα:
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, '+
				'Ἐτικέτες, μέρος_του_λόγου, τονισμοί, Παρατηρήσεις from Τονισμοί as p '+
					'WHERE Ἡμερομηνία=(SELECT MAX(Ἡμερομηνία) FROM '+
					'Τονισμοί WHERE ΑΑ=p.ΑΑ and Διάλεκτος=p.Διάλεκτος and '+
					'μέρος_του_λόγου=p.μέρος_του_λόγου);')
		else:
			σύνολα = cur.execute('select Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, '+
				'Ἐτικέτες, μέρος_του_λόγου, τονισμοί, Παρατηρήσεις from Τονισμοί as p '+
				'WHERE Ἐτικέτες LIKE "%τρέχον%" AND Ἡμερομηνία=(SELECT MAX(Ἡμερομηνία) FROM '+
				'Τονισμοί WHERE ΑΑ=p.ΑΑ and Διάλεκτος=p.Διάλεκτος and '+
				'μέρος_του_λόγου=p.μέρος_του_λόγου);')
		self.sql.conn.commit()
		for σύνολο in σύνολα:
			Κλειδί, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, μέρος_του_λόγου, τόνοι, Παρατηρήσεις = σύνολο
			if μέρος_του_λόγου not in τονισμοί:
				τονισμοί[μέρος_του_λόγου] = {}
			if Διάλεκτος not in τονισμοί[μέρος_του_λόγου]:
				τονισμοί[μέρος_του_λόγου][Διάλεκτος] = []
			while ΑΑ>=len(τονισμοί[μέρος_του_λόγου][Διάλεκτος]):
				τονισμοί[μέρος_του_λόγου][Διάλεκτος].append({"τονισμοί":[]})
			τονισμός = {}
			τονισμός["Κλειδί"] = Κλειδί
			τονισμός["ΑΑ"] = ΑΑ
			τονισμός["διάλεκτος"] = Διάλεκτος
			τονισμός["Συγγραφέας"] = Συγγραφέας
			τονισμός["Ἡμερομηνία"] = Ἡμερομηνία
			τονισμός["ἐτικέτες"] = Ἐτικέτες
			τονισμός["μέρος του λόγου"] = μέρος_του_λόγου
			τονισμός["τονισμοί"] = eval(τόνοι)
			τονισμός["Παρατηρήσεις"] = Παρατηρήσεις
			τονισμοί[μέρος_του_λόγου][Διάλεκτος][ΑΑ] = τονισμός
		
	