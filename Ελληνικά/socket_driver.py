#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import cherrypy
import threading
import os
PATH = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.join(PATH, "web")
# TODO: standard μυνήματα
help = """[<pre>Χρήση:
http://localhost:7000/hlt/id/μύνημα_json

π.χ.
νέο session
http://localhost:7000/hlt/0/{"τύπος":"ime","διάλεκτος":"δημοτική"}
επιστρέφη => {"id":10}

http://localhost:7000/hlt/1/["preedit":"ουr"]
επιστρέφη => ["list", ουρ, "horizontal", ["οὐρανός"]]

Μυνήματα IME
["preedit", "αρχικά γράμματα"], => ["list", αρχικά, "horizontal", ["υποψήφια λέξη 1",..., "υποψήφια λέξη Ν"]]
                                   ["text", "λέξη"]
["commit", "λέξη"]              => ["list", αρχικά, "vertical", ["κατάληξη 1",..., "κατάληξη Ν"]]
                                   ["text", "λέξη"]							  

</pre>]"""

class SocketDriver:
	def __init__(self, mhlt):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		self._hlt = mhlt
		self.id = 1
		self._λήμμα_cache = { 
			"ουσιαστικά":{"δημοτική":{}, "κοινή":{}},
			"επίθετα":{   "δημοτική":{}, "κοινή":{}}}
		self._λήμμα_list = {
			"ουσιαστικά":{"δημοτική":{}, "κοινή":{}},
			"επίθετα":{   "δημοτική":{}, "κοινή":{}}}
		self.imes = {}
	
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def hlt(self, id, message):
		απάντηση = help
		id = int(id)
		try:
			μύνημα = json.loads(message,"utf-8")
		except ValueError:
			return help
		
		if id==0:
			if μύνημα.get("τύπος")=="ime":
				διάλεκτος = μύνημα.get("διάλεκτος","δημοτική")
				self.imes[self.id] = self._hlt.iime(self._hlt.γ)
				self.imes[self.id].μυνήματα(["διάλεκτος",διάλεκτος])
				απάντηση = {"id":self.id}
				self.id += 1
		elif id in self.imes:
			απάντηση = self.imes[id].μυνήματα(μύνημα)
		else:
			απάντηση = ["reconnect"]
		
		return json.dumps(απάντηση,'utf-8')
	
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def web(self):
		a=open(os.path.join("web","Grammatiki.html"),'r')
		data = a.read()
		a.close()
		return data
	
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def web_a(self):
		a=open(os.path.join("web","Arthra.html"),'r')
		data = a.read()
		a.close()
		return data
	
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def web_o(self):
		a=open(os.path.join("web","Oysiastika.html"),'r')
		data = a.read()
		a.close()
		return data
	
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def web_e(self):
		a=open(os.path.join("web","Epitheta.html"),'r')
		data = a.read()
		a.close()
		return data
	
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def web_o_m(self, message):
		message = str(message.encode("raw_unicode_escape"),"utf-8")
		message = json.loads(message, 'utf-8')
		l_message = len(message)
		print("ΜΥΝΗΜΑ", message)
		data = []
		if l_message==2:
			if message[0]=="Αρχικά" and\
				message[1] in self._hlt.γ.ο.δ.λήμματα:
				data = ["Αρχικά"]
				tdata = []
				if message[1] in self._λήμμα_list["ουσιαστικά"] and\
					self._λήμμα_list["ουσιαστικά"][message[1]]:
					tdata = self._λήμμα_list["ουσιαστικά"][message[1]]
				else:
					for λήμμα in self._hlt.γ.ο.δ.λήμματα[message[1]]:
						if λήμμα[0] not in self._λήμμα_cache["ουσιαστικά"][message[1]]:
							self._λήμμα_cache["ουσιαστικά"][message[1]][λήμμα[0]] = [λήμμα]
							tdata.append(λήμμα[0])
						else:
							self._λήμμα_cache["ουσιαστικά"][message[1]][λήμμα[0]].append(λήμμα)
					tdata.sort()
				self._λήμμα_list["ουσιαστικά"][message[1]] = tdata
				data += tdata
			elif message[0]=="Βασικά" and\
				message[1] in self._hlt.γ.ο.δ.καταλήξεις and\
				message[1] in self._hlt.γ.ο.δ.τονισμοί:
				data = ["Βασικά"] # καταλήξεις, τονισμοί
				
				καταλήξεις = ["ανώμαλο", "άκλητο"]
				κ = list(self._hlt.γ.ο.δ.καταλήξεις[message[1]].keys())
				κ.sort()
				καταλήξεις += κ
				data.append(καταλήξεις)
				
				τονισμοί = [0]
				τ = list(self._hlt.γ.ο.δ.τονισμοί[message[1]].keys())
				τ.sort()
				τονισμοί += τ
				data.append(τονισμοί)
				
		elif l_message==3:
			if message[0]=="λήμματα" and\
				message[1] in self._λήμμα_cache["ουσιαστικά"] and\
				message[2] in self._λήμμα_cache["ουσιαστικά"][message[1]]:
				data = ["λήμματα"]
				tdata = self._λήμμα_cache["ουσιαστικά"][message[1]][message[2]]
				tdata.sort()
				data += tdata
			elif message[0]=="συνθετικά" and\
				message[1] in self._hlt.γ.ο.δ.λήμματα and\
				message[2] in self._hlt.γ.ο.δ.λήμματα[message[1]]:
				λημ = self._hlt.γ.ο.δ.λήμματα[message[1]][message[2]]
				data = ["συνθετικά"]
				tdata = []
				
				for κατηγορία, σύνολα in λημ.items():
					for σύνολο in σύνολα:
						if "συνθετικό" in σύνολο:
							tdata.append(σύνολο["συνθετικό"])
						elif "" not in tdata:
							tdata.append("")
				tdata.sort()
				data += tdata
		elif l_message==4:
			if message[0]=="ανάλυση" and\
				message[1] in self._hlt.γ.ο.δ.λήμματα and\
				message[2] in self._hlt.γ.ο.δ.λήμματα[message[1]]:
				λημ = self._hlt.γ.ο.δ.λήμματα[message[1]][message[2]]
				data = ["ανάλυση"]
				tdata = []
				# κλίση = [onomastikh_enikos, genos, [[arthro, klisi],]]
				for κατηγορία, σύνολα in λημ.items():
					for σύνολο in σύνολα:
						if not ((message[3] and "συνθετικό" in σύνολο and σύνολο["συνθετικό"]==message[3]) or\
								(not message[3] and "συνθετικό" not in σύνολο)):
							continue
						κλίση = ["", σύνολο["γένος"], [], [], [], 0, 0]
						λήμμα = self._hlt.γ.τ.κωδικοποιητής(message[3]+message[2])
						if message[1]=="κοινή":
							πτώσεις = ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]
							αριθμοί = ["ενικός", "δυϊκός", "πληθυντικός"]
						else:
							πτώσεις = ["ονομαστική", "γενική", "αιτιατική", "κλητική"]
							αριθμοί = ["ενικός", "πληθυντικός"]
						for αριθμός in αριθμοί:
							for πτώση in πτώσεις:
								άρθρο = self._hlt.γ.α.κλίνε(αριθμός, πτώση, σύνολο["γένος"], "οριστικό", διάλεκτος=message[1])
								ουσιαστικό = self._hlt.γ.ο._κλίνε(λήμμα, κατηγορία, σύνολο["τονισμός"], message[1], αριθμός, πτώση) 
								κλίση[5] = κατηγορία
								κλίση[6] = σύνολο["τονισμός"]
								if ουσιαστικό:
									ουσιαστικό = self._hlt.γ.τ.απο(ουσιαστικό[0], με_ς=True)
								else:
									ουσιατικό = ""
								if not ουσιαστικό:
									κλίση[2].append(["", ""])
								else:
									κλίση[2].append([άρθρο,ουσιαστικό])
						κλίση[0] = κλίση[2][0][1].capitalize()
						if "κλίμακες" in σύνολο:
							for k,v in σύνολο["κλίμακες"].items():
								κλίση[4].append(k)
								κλίση[4].append(str(v))
						if "μεταδεδομένα" in σύνολο:
							for k,v in σύνολο["μεταδεδομένα"].items():
								κλίση[3].append(k)
								if v.__class__==list:
									κλίση[3].append(", ".join(v))
								else:
									κλίση[3].append(v)
						tdata.append(κλίση) 
				data += tdata
		elif l_message==7:
			if message[0]=="κλίση" and\
				message[1] in self._hlt.γ.ο.δ.καταλήξεις and\
				message[1] in self._hlt.γ.ο.δ.τονισμοί:
				data = ["κλίση"]
				# [ "κλίση", activeTab, synthetiko, lhmma, genos, katalhjeis, tonismos ]
				κλίση = []
				λήμμα = self._hlt.γ.τ.κωδικοποιητής(message[2]+message[3])
				γένος = message[4]
				if message[5]=='άκλητο':
					κατηγορία = -1
				elif message[5]=='ανώμαλο':
					κατηγορία = 0
				else:
					κατηγορία = int(message[5])
				τονισμός = int(message[6])
				if message[1]=="κοινή":
					πτώσεις = ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]
					αριθμοί = ["ενικός", "δυϊκός", "πληθυντικός"]
				else:
					πτώσεις = ["ονομαστική", "γενική", "αιτιατική", "κλητική"]
					αριθμοί = ["ενικός", "πληθυντικός"]
				for αριθμός in αριθμοί:
					for πτώση in πτώσεις:
						άρθρο = self._hlt.γ.α.κλίνε(αριθμός, πτώση, γένος, "οριστικό", διάλεκτος=message[1])
						if κατηγορία:
							ουσιαστικό = self._hlt.γ.ο._κλίνε(λήμμα, κατηγορία, τονισμός, message[1], αριθμός, πτώση)
						else:
							ουσιαστικό = "" 
						if ουσιαστικό:
							ουσιαστικό = self._hlt.γ.τ.απο(ουσιαστικό[0], με_ς=True)
						else:
							ουσιατικό = ""
						if not ουσιαστικό:
							κλίση.append(["", ""])
						else:
							κλίση.append([άρθρο,ουσιαστικό])
				data.append(κλίση) 
		jdata = json.dumps(data, "utf-8")
		print("DATA", data)
		return jdata
	
	@cherrypy.expose
	@cherrypy.tools.encode(encoding='UTF-8')
	def web_e_m(self, message):
		message = str(message.encode("raw_unicode_escape"),"utf-8")
		message = json.loads(message, 'utf-8')
		l_message = len(message)
		print("ΜΥΝΗΜΑ", message)
		data = []
		if l_message==2:
			if message[0]=="Αρχικά" and\
				message[1] in self._hlt.γ.ε.λήμματα:
				data = ["Αρχικά"]
				tdata = []
				if message[1] in self._λήμμα_list["επίθετα"] and\
					self._λήμμα_list["επίθετα"][message[1]]:
					tdata = self._λήμμα_list["επίθετα"][message[1]]
				else:
					for κατηγορίες in self._hlt.γ.ε.λήμματα[message[1]]:
						for κατηγορία, δεδομένα in κατηγορίες.items():
							for δεδομένο in δεδομένα:
								λήμμα = δεδομένο['λήμμα']
								if λήμμα[0] not in self._λήμμα_cache["επίθετα"][message[1]]:
									self._λήμμα_cache["επίθετα"][message[1]][λήμμα[0]] = [λήμμα]
									tdata.append(λήμμα[0])
								else:
									self._λήμμα_cache["επίθετα"][message[1]][λήμμα[0]].append(λήμμα)
					tdata.sort()
				self._λήμμα_list["επίθετα"][message[1]] = tdata
				data += tdata
			elif message[0]=="Βασικά" and\
				message[1] in self._hlt.γ.ε.κατηγορίες and\
				message[1] in self._hlt.γ.ε.τονισμοί:
				data = ["Βασικά"] # καταλήξεις, τονισμοί
				
				καταλήξεις = ["ανώμαλο", "άκλητο"]
				aa = 0
				κ = []
				for κατηγορία in self._hlt.γ.ε.κατηγορίες[message[1]]:
					if κατηγορία:
						κ.append(aa)
					aa += 1
				
				κ.sort()
				καταλήξεις += κ
				data.append(καταλήξεις)
				
				τονισμοί = [0]
				aa = 0
				for τονισμό in self._hlt.γ.ε.τονισμοί[message[1]]:
					if τονισμό:
						τονισμοί.append(aa)
					aa += 1
				data.append(τονισμοί)
				
		elif l_message==3:
			if message[0]=="λήμματα" and\
				message[1] in self._λήμμα_cache["επίθετα"] and\
				message[2] in self._λήμμα_cache["επίθετα"][message[1]]:
				data = ["λήμματα"]
				tdata = self._λήμμα_cache["επίθετα"][message[1]][message[2]]
				tdata.sort()
				data += tdata
			elif message[0]=="συνθετικά" and\
				message[1] in self._hlt.γ.ε.λήμματα:
				ακ = {}
				κΛημ = self._hlt.γ.τ.κωδικοποιητής(message[2])
				μΛημ = κΛημ.size
				self._hlt.γ.τ.keyfinder(self._hlt.γ.ε.ευρετήριο_λημμάτων[message[1]], κΛημ[::-1], μΛημ, ακ)
				λημ = []
				if μΛημ in ακ:
					δεδ = ακ[μΛημ][0]
					for k, v in self._hlt.γ.ε.λήμματα[message[1]][δεδ].items():
						λημ += v 
				data = ["συνθετικά"]
				tdata = []
				
				for σύνολο in λημ:
					if "συνθετικό" in σύνολο:
						tdata.append(σύνολο["συνθετικό"])
					elif "" not in tdata:
						tdata.append("")
				tdata.sort()
				data += tdata
		elif l_message==4:
			if message[0]=="ανάλυση" and\
				message[1] in self._hlt.γ.ε.λήμματα:
				
				ακ = {}
				κΛημ = self._hlt.γ.τ.κωδικοποιητής(message[2])
				μΛημ = κΛημ.size
				self._hlt.γ.τ.keyfinder(self._hlt.γ.ε.ευρετήριο_λημμάτων[message[1]], κΛημ[::-1], μΛημ, ακ)
				λημ = []
				if μΛημ in ακ:
					δεδ = ακ[μΛημ][0]
					for k, v in self._hlt.γ.ε.λήμματα[message[1]][δεδ].items():
						λημ += v 
				
				data = ["ανάλυση"]
				tdata = []
				# κλίση = [onomastikh_enikos, genos, [[arthro, klisi],]]
				for σύνολο in λημ:
					if not ((message[3] and "συνθετικό" in σύνολο and σύνολο["συνθετικό"]==message[3]) or\
							(not message[3] and "συνθετικό" not in σύνολο)):
						continue
					κλίση = ["", "", [], [], [], 0, 0]
					λήμμα = self._hlt.γ.τ.κωδικοποιητής(message[3]+message[2])
					if message[1]=="κοινή":
						πτώσεις = ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]
						αριθμοί = ["ενικός", "δυϊκός", "πληθυντικός"]
					else:
						πτώσεις = ["ονομαστική", "γενική", "αιτιατική", "κλητική"]
						αριθμοί = ["ενικός", "πληθυντικός"]
					κλίση[5] = σύνολο['κατηγορίες']
					κλίση[6] = σύνολο["τονισμοί"]
					for γένος in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
						αγένος = self._hlt.γ.ε.γένος_σε_αριθμό[γένος]
						for αριθμός in αριθμοί:
							for πτώση in πτώσεις:
								
								άρθρο = self._hlt.γ.α.κλίνε(αριθμός, πτώση, γένος, "οριστικό", διάλεκτος=message[1])
								επίθετο = self._hlt.γ.ε._κλίνε(λήμμα, σύνολο['κατηγορίες'][αγένος], αριθμός, πτώση, σύνολο["τονισμοί"][αγένος], message[1]) 
								
								if επίθετο:
									επίθετο = self._hlt.γ.τ.απο(επίθετο[0], με_ς=True)
								else:
									επίθετο = ""
								if not επίθετο:
									κλίση[2].append(["", ""])
								else:
									κλίση[2].append([άρθρο,επίθετο])
					κλίση[0] = κλίση[2][0][1].capitalize()
					if "κλίμακες" in σύνολο:
						for k,v in σύνολο["κλίμακες"].items():
							κλίση[4].append(k)
							κλίση[4].append(str(v))
					if "μεταδεδομένα" in σύνολο:
						for k,v in σύνολο["μεταδεδομένα"].items():
							κλίση[3].append(k)
							if v.__class__==list:
								κλίση[3].append(", ".join(v))
							else:
								κλίση[3].append(v)
					tdata.append(κλίση) 
				
				data += tdata
		elif l_message==7:
			if message[0]=="κλίση":
				data = ["κλίση"]
				# [ "κλίση", activeTab, synthetiko, lhmma, genos, katalhjeis, tonismos ]
				κλίση = []
				λήμμα = self._hlt.γ.τ.κωδικοποιητής(message[2]+message[3])
				
				κατηγορίες = []
				τονισμοί = []
				for i in range(3):
					if message[5]=='άκλητο':
						κατηγορίες.append(-1)
					elif message[5]=='ανώμαλο':
						κατηγορίες.append(0)
					else:
						κατηγορίες.append(int(message[5][i]))
					τονισμοί.append(int(message[6][i]))
				
				if message[1]=="κοινή":
					πτώσεις = ["ονομαστική", "γενική", "δοτική", "αιτιατική", "κλητική"]
					αριθμοί = ["ενικός", "δυϊκός", "πληθυντικός"]
				else:
					πτώσεις = ["ονομαστική", "γενική", "αιτιατική", "κλητική"]
					αριθμοί = ["ενικός", "πληθυντικός"]
				for γένος in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
					αγένος = self._hlt.γ.ε.γένος_σε_αριθμό[γένος]
					κατηγορία = κατηγορίες[αγένος]
					τονισμός = τονισμοί[αγένος]
					for αριθμός in αριθμοί:
						for πτώση in πτώσεις:
							άρθρο = self._hlt.γ.α.κλίνε(αριθμός, πτώση, γένος, "οριστικό", διάλεκτος=message[1])
							if κατηγορία:
								επίθετο = self._hlt.γ.ε._κλίνε(λήμμα, κατηγορία, αριθμός, πτώση, τονισμός, message[1])
							else:
								επίθετο = "" 
							if επίθετο:
								επίθετο = self._hlt.γ.τ.απο(επίθετο[0], με_ς=True)
							else:
								επίθετο = ""
							if not επίθετο:
								κλίση.append(["", ""])
							else:
								κλίση.append([άρθρο, επίθετο])
				data.append(κλίση)
		
		jdata = json.dumps(data, "utf-8")
		print("DATA", data)
		return jdata
	
class socket_driver(threading.Thread):
	def __init__(self, hlt):
		threading.Thread.__init__(self)
		self.hlt = hlt
	
	def run(self):
		conf = {'/': {'tools.staticdir.on': True,
              'tools.staticdir.dir': PATH}}
		
		cherrypy.config.update({'server.socket_host': '127.0.0.1',
                        'server.socket_port': 7000})
		cherrypy.quickstart(SocketDriver(self.hlt), config=conf)
		
#socket_driver("")
# OUT
# orders, values
# OK ["τύπος", "ime"]
# OK ["διάλεκτος", [δημοτική, κοινή]]
# OK ["commit", "text"]
# OK ["preedit", "text"]
#
# IN
# orders, values
# OK ["list","orientation","preedit",[list]]
# OK ["text",text]
# ["id", number]
#
# "preedit" => list, text
