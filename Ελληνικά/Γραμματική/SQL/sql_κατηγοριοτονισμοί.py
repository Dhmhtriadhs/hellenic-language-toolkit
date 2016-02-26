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

class Κατηγοριοτονισμοί():
	def __init__(self, sql):
		self.sql = sql

	def νέα(self, αναγνώριση, δεδομένα, κκαταλήξεις, κτονισμοί):
		διάλεκτος = αναγνώριση["διάλεκτος"]
		μτλ = αναγνώριση["μέρος του λόγου"]
		ΑΑ = αναγνώριση.get("ΑΑ")
		χρόνος = αναγνώριση.get("χρόνος")
		cur = self.sql.conn.cursor()
		σετ = {}
		if ΑΑ:
			for σύνολο in cur.execute(
				'select Κλειδί, Ἐτικέτες from Κατηγοριοτονισμοί '+
				'where ΑΑ=? and Διάλεκτος=? and μέρος_του_λόγου=? and χρόνος=?;', 
					(ΑΑ, διάλεκτος, μτλ, χρόνος)):
				if σύνολο:
						σετ[σύνολο[0]] = σύνολο[1]
			for k,v in σετ.items():
				if "τρέχον" in v:
					cur.execute('update Κατηγοριοτονισμοί set Ἐτικέτες=? where Κλειδί=?;', (v.replace("τρέχον", "ανενεργό"), k))
		else:
			αναγνώριση["ΑΑ"] = 1
			cur.execute('select max(ΑΑ) from Κατηγοριοτονισμοί where Διάλεκτος=? and μέρος_του_λόγου=? and χρόνος=?;', 
						(διάλεκτος, μτλ, χρόνος))
			for c in cur:
				if c and c[0]:
					αναγνώριση["ΑΑ"] = c[0]+1
			
		self.__αποθήκευση(αναγνώριση)
		self.sql.conn.commit()
		self.φόρτωση(δεδομένα, κκαταλήξεις, κτονισμοί)
	
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
		χρόνος = σύνολο["χρόνος"]
		καταλήξεις = str(σύνολο["καταλήξεις"])
		τονισμοί = str(σύνολο["τονισμοί"])
		μέρος_του_λόγου = σύνολο["μέρος του λόγου"]
		
		cur = self.sql.conn.cursor()
		cur.execute('insert into Κατηγοριοτονισμοί (ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, '+
				'Ἐτικέτες, μέρος_του_λόγου, χρόνος, καταλήξεις, τονισμοί, Παρατηρήσεις) '+
			'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
			(ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, μέρος_του_λόγου, 
			χρόνος, καταλήξεις, τονισμοί, Παρατηρήσεις))
			
	def τρέχον(self, αναγνώριση, δεδομένα, κκαταλήξεις, κτονισμοί):
		ΑΑ = αναγνώριση["ΑΑ"]
		Κλειδί = αναγνώριση["Κλειδί"]
		μτλ = αναγνώριση["μέρος του λόγου"]
		διάλεκτος = αναγνώριση["διάλεκτος"]
		χρόνος = αναγνώριση.get("χρόνος")
		σετ = []
		τρέχον = None
		cur = self.sql.conn.cursor()
		for σύνολο in cur.execute(
			'select Κλειδί, Ἐτικέτες from Κατηγοριοτονισμοί where ΑΑ=? and μέρος_του_λόγου=? and Διάλεκτος=? and χρόνος=?;', 
			(ΑΑ, μτλ, διάλεκτος, χρόνος)):
			if σύνολο and σύνολο[0]!=Κλειδί:
				σετ.append([σύνολο[0], σύνολο[1]])
			elif σύνολο[0]==Κλειδί:
				τρέχον = σύνολο[1]
		for σ in σετ:
			if "τρέχον" in σ[1]:
				cur.execute('update Κατηγοριοτονισμοί set Ἐτικέτες=? where Κλειδί=?;', (σ[1].replace("τρέχον", "ανενεργό"), σ[0]))
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
			cur.execute('update Κατηγοριοτονισμοί set Ἐτικέτες=? where Κλειδί=?;', 
							(", ".join(νέο_τρέχον), Κλειδί))
		self.φόρτωση(δεδομένα, κκαταλήξεις, κτονισμοί)
		self.sql.conn.commit()
	
	def διαγραφή(self, αναγνώριση, δεδομένα, κκαταλήξεις, κτονισμοί):
		cur = self.sql.conn.cursor()
		Κλειδί = αναγνώριση["Κλειδί"]
		σετ = []
		for σύνολο in cur.execute('select Ἐτικέτες from Κατηγοριοτονισμοί where Κλειδί=?;', (Κλειδί, )):
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
				cur.execute('update Κατηγοριοτονισμοί set Ἐτικέτες=? where Κλειδί=?;', (σ, Κλειδί))
		self.φόρτωση(δεδομένα, κκαταλήξεις, κτονισμοί)
		
		self.sql.conn.commit()
				
	def φόρτωση(self, δεδομένα, κκαταλήξεις, κτονισμοί, όλα=False):
		keys = list(δεδομένα.keys())
		for k in keys:
			δεδομένα[k].clear()
		cur = self.sql.conn.cursor()
		if όλα:
			σύνολα = cur.execute('select Κλειδί, μέρος_του_λόγου, χρόνος, ΑΑ, Διάλεκτος, '+
				'Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, καταλήξεις, τονισμοί, Παρατηρήσεις '+
				'from Κατηγοριοτονισμοί as p '+
				'WHERE Ἡμερομηνία=(SELECT MAX(Ἡμερομηνία) FROM Κατηγοριοτονισμοί '+
				'WHERE Διάλεκτος=p.Διάλεκτος and p.ΑΑ=ΑΑ and '+
				'p.μέρος_του_λόγου=μέρος_του_λόγου and p.χρόνος=χρόνος);')
		else:
			σύνολα = cur.execute('select Κλειδί, μέρος_του_λόγου, χρόνος, ΑΑ, Διάλεκτος, '+
				'Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, καταλήξεις, τονισμοί, Παρατηρήσεις '+
				'from Κατηγοριοτονισμοί as p '+
				'WHERE Ἡμερομηνία=(SELECT MAX(Ἡμερομηνία) FROM '+
				'Κατηγοριοτονισμοί WHERE Ἐτικέτες LIKE "%τρέχον%" AND Διάλεκτος=p.Διάλεκτος and p.ΑΑ=ΑΑ '+
				'and p.μέρος_του_λόγου=μέρος_του_λόγου and p.χρόνος=χρόνος);')
		self.sql.conn.commit()
		for σύνολο in σύνολα:
			Κλειδί, μέρος_του_λόγου, χρόνος, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, καταλήξεις, τονισμοί, Παρατηρήσεις = σύνολο
			
			for κατηγορία in eval(καταλήξεις):
				if κατηγορία>0 and not κκαταλήξεις[μέρος_του_λόγου][Διάλεκτος][χρόνος][κατηγορία]["καταλήξεις"]:
					print("Κατηγοριοτονισμοί",μέρος_του_λόγου,χρόνος,ΑΑ,": λείπουν οι καταλήξεις", κατηγορία, "στον χρόνο", χρόνος, "στην διάλεκτο",Διάλεκτος)
			if μέρος_του_λόγου=="μετοχή":
				for τονισμός in eval(τονισμοί):
					if τονισμός>0 and not κτονισμοί["επίθετο"][Διάλεκτος][τονισμός]:
						print(μέρος_του_λόγου,": λείπει ο τονισμός", τονισμός, "στον χρόνο", χρόνος, "στην διάλεκτο",Διάλεκτος)
			else:
				for τονισμός in eval(τονισμοί):
					if τονισμός>0 and not κτονισμοί[μέρος_του_λόγου][Διάλεκτος][τονισμός]:
						print(μέρος_του_λόγου,": λείπει ο τονισμός", τονισμός, "στον χρόνο", χρόνος, "στην διάλεκτο",Διάλεκτος)
			δεδομένο = {}
			δεδομένο["Κλειδί"] = Κλειδί
			δεδομένο["μέρος του λόγου"] = μέρος_του_λόγου
			δεδομένο["ΑΑ"] = ΑΑ
			δεδομένο["διάλεκτος"] = Διάλεκτος
			δεδομένο["χρόνος"] = χρόνος
			δεδομένο["Ἡμερομηνία"] = Ἡμερομηνία
			δεδομένο["Συγγραφέας"] = Συγγραφέας
			δεδομένο["ἐτικέτες"] = Ἐτικέτες
			δεδομένο["καταλήξεις"] = eval(καταλήξεις)
			
			δεδομένο["τονισμοί"] = eval(τονισμοί)
			δεδομένο["Παρατηρήσεις"] = Παρατηρήσεις
			
			if μέρος_του_λόγου not in δεδομένα:
				δεδομένα[μέρος_του_λόγου] = {}
			if Διάλεκτος not in δεδομένα[μέρος_του_λόγου]:
				δεδομένα[μέρος_του_λόγου][Διάλεκτος] = {}
			if χρόνος not in δεδομένα[μέρος_του_λόγου][Διάλεκτος]:
				δεδομένα[μέρος_του_λόγου][Διάλεκτος][χρόνος] = []
			while ΑΑ>=len(δεδομένα[μέρος_του_λόγου][Διάλεκτος][χρόνος]):
				δεδομένα[μέρος_του_λόγου][Διάλεκτος][χρόνος].append({})
			δεδομένα[μέρος_του_λόγου][Διάλεκτος][χρόνος][ΑΑ] = δεδομένο
	
	def ιστορικό(self, αναγνώριση):
		αποτέλεσμα = []
		ΑΑ = αναγνώριση["ΑΑ"]
		if ΑΑ:
			cur = self.sql.conn.cursor()
			σύνολα = cur.execute('select Κλειδί, μέρος_του_λόγου, χρόνος, ΑΑ, Διάλεκτος, '+
				'Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, καταλήξεις, τονισμοί, Παρατηρήσεις '+
				'from Κατηγοριοτονισμοί as p '+
				'WHERE ΑΑ=? and Διάλεκτος=? and μέρος_του_λόγου=? and χρόνος=?;', 
				(ΑΑ, αναγνώριση["διάλεκτος"], αναγνώριση["μέρος του λόγου"], αναγνώριση["χρόνος"]))
			for σύνολο in σύνολα:
				Κλειδί, μέρος_του_λόγου, χρόνος, ΑΑ, Διάλεκτος, Ἡμερομηνία, Συγγραφέας, Ἐτικέτες, καταλήξεις, τονισμοί, Παρατηρήσεις = σύνολο
			
				δεδομένο = {}
				δεδομένο["Κλειδί"] = Κλειδί
				δεδομένο["μέρος του λόγου"] = μέρος_του_λόγου
				δεδομένο["ΑΑ"] = ΑΑ
				δεδομένο["διάλεκτος"] = Διάλεκτος
				δεδομένο["χρόνος"] = χρόνος
				δεδομένο["Ἡμερομηνία"] = Ἡμερομηνία
				δεδομένο["Συγγραφέας"] = Συγγραφέας
				δεδομένο["ἐτικέτες"] = Ἐτικέτες
				δεδομένο["καταλήξεις"] = eval(καταλήξεις)
				δεδομένο["τονισμοί"] = eval(τονισμοί)
				δεδομένο["Παρατηρήσεις"] = Παρατηρήσεις
				
				αποτέλεσμα.append(δεδομένο)
			self.sql.conn.commit()
		return αποτέλεσμα
			