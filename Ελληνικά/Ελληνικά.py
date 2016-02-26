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

from Ελληνικά.Γραμματική.Τονιστής   import Τονιστής
import Ελληνικά.Γραμματική.δεδομένα as δεδομένα
from Ελληνικά.Γραμματική.Γραμματική import Γραμματική
from Ελληνικά.Βοηθητικά import Ανάλυση, Σύνθεση, web, web_develop
from Ελληνικά.Ἐργαλεία import IME
from Ελληνικά.Ἐργαλεία import Εξαγωγή
from Ελληνικά.δοκιμές.Επιφωνημάτων import Δοκιμές_Επιφωνημάτων
from Ελληνικά.δοκιμές.Μορίων import Δοκιμές_Μορίων
from Ελληνικά.δοκιμές.Συνδέσμων import Δοκιμές_Συνδέσμων
from Ελληνικά.δοκιμές.Προθέσεων import Δοκιμές_Προθέσεων
from Ελληνικά.δοκιμές.Επιρρημάτων import Δοκιμές_Επιρρημάτων
from Ελληνικά.δοκιμές.Άρθρων import Δοκιμές_Άρθρων
from Ελληνικά.δοκιμές.Ουσιαστικών import Δοκιμές_Ουσιαστικών
from Ελληνικά.δοκιμές.Μετοχῶν import Δοκιμές_Μετοχῶν
from Ελληνικά.δοκιμές.Ρημάτων import Δοκιμές_Ρημάτων
from Ελληνικά.δοκιμές.Αντωνυμιών import Δοκιμές_Αντωνυμιών
from Ελληνικά.δοκιμές.Επιθέτων import Δοκιμές_Επιθέτων
	
import cherrypy
import os

PATH = os.path.abspath(os.path.dirname(__file__))

class Ελληνικά():
	def __init__(self, develop=None):
		self.τ = Τονιστής()
		self._δεδομένα = δεδομένα.Δεδομένα(self.τ, develop)
		self.develop = develop
		self.φράσεις = {"κοινή":{}, "δημοτική":{}}
		self.γ = Γραμματική(self._δεδομένα, self.τ, develop)
		self.γραμματική = self.γ
		self.α = Ανάλυση.Ανάλυση(self.γραμματική)
		self.ανάλυση = self.α
		self.ανάλυσε = self.α.ανάλυσε
		self.σύνθεση = Σύνθεση.Σύνθεση(self.γραμματική)
		self.web = web.web
		self.web_develop = web_develop.web_develop
		self.εξαγωγή = Εξαγωγή.Εξαγωγή(self.γ)
		#self.IME = IME.IME(self.γ)
		#self.ΙΜΕ = self.IME
		
		self.serve()
		#self.δοκιμές()
		
	def δοκιμές(self):
		δε = Δοκιμές_Επιφωνημάτων(self.γ)
		δε.δοκιμές_αναγνώρισης()
		
		δμ = Δοκιμές_Μορίων(self.γ)
		δμ.δοκιμές_αναγνώρισης()
		
		δσ = Δοκιμές_Συνδέσμων(self.γ)
		δσ.δοκιμές_αναγνώρισης()
		
		δπ = Δοκιμές_Προθέσεων(self.γ)
		δπ.δοκιμές_αναγνώρισης()
		
		δεπ = Δοκιμές_Επιρρημάτων(self.γ)
		δεπ.δοκιμές_αναγνώρισης()
		
		δα = Δοκιμές_Άρθρων(self.γ)
		δα.δοκιμές_αναγνώρισης()
		δα.δοκιμές_κλίσης()
		
		δα = Δοκιμές_Αντωνυμιών(self.γ, self._δεδομένα)
		δα.δοκιμές_αναγνώρισης()
		δα.δοκιμές_κλίσης()
		
		δο = Δοκιμές_Ουσιαστικών(self.γ, self._δεδομένα)
		δο.δοκιμές_αναγνώρισης()
		δο.δοκιμές_κλίσης()
		
		δε = Δοκιμές_Επιθέτων(self.γ, self._δεδομένα)
		δε.δοκιμές_αναγνώρισης()
		δε.δοκιμές_κλίσης()
		
		δμ = Δοκιμές_Μετοχῶν(self.γ, self._δεδομένα)
		δμ.δοκιμές_αναγνώρισης()
		δμ.δοκιμές_κλίσης()
	
		δρ = Δοκιμές_Ρημάτων(self.γ, self._δεδομένα)
		δρ.δοκιμές_αναγνώρισης()
		δρ.δοκιμές_κλίσης()

	def πολυτόνισε(self, κείμενο, διάλεκτος=None):
		if not κείμενο:
			return κείμενο
			
		κΣτοιχεία = self.ανάλυση.ανάλυσε(κείμενο, διάλεκτος, raw=True)
		νέο_κείμενο = self.σύνθεση.σύνθεση(κΣτοιχεία, διάλεκτος)
		return νέο_κείμενο
	
	def serve(self):
		conf1 = {'/': {'tools.staticdir.on': True,
              'tools.staticdir.dir': os.path.join(PATH, "web", "public")}}
		
		cherrypy.tree.mount(self.web(self), "/", conf1)
		if self.develop:
			conf2 = {'/D': {'tools.staticdir.on': True,
              'tools.staticdir.dir': os.path.join(PATH, "web")}}
			cherrypy.tree.mount(self.web_develop(self), "/Develop", conf2)
		cherrypy.server.unsubscribe()
		
		if self.develop:
			server1 = cherrypy._cpserver.Server()
			server1.socket_port=7001
			server1._socket_host='0.0.0.0'
			server1.thread_pool=3
			server1.ssl_module = 'builtin'
			server1.ssl_certificate = os.path.join(PATH, "Βοηθητικά", 'HLT.gr.crt')
			server1.ssl_private_key = os.path.join(PATH, "Βοηθητικά", 'HLT.key')
			server1.ssl_certificate_chain = os.path.join(PATH, "Βοηθητικά",'HLT.gr.crt')
			
			server1.subscribe()

		server2 = cherrypy._cpserver.Server()
		server2.socket_port=7000
		server2._socket_host="0.0.0.0"
		server2.thread_pool=30
		server2.subscribe()
		
		cherrypy.engine.start()
		cherrypy.engine.block()
	
if __name__ == '__main__':
	#import cProfile
	#cProfile.run("Ελληνικά()") 
	ε=Ελληνικά("δημοτική", True)
	#print(ε.πολυτόνισε(ζ))

#	φ=open("grc_GR.dic",'r')
#	γραμμές = φ.readlines()
#	φ.close()
#	αποτυχίες = []
#	counter, fcounter = 0, 0
#	φ=open("grc_GR.dicf",'w')
#	φ2=open("grc_GR.dics",'w')
#	for γραμμή in γραμμές:
#		λέξη = γραμμή[:-1]
#		if "/" in λέξη:
#			λέξη = λέξη.split("/")[0]
#		ανα = ε.γ.αναγνώριση(λέξη)
#		if not ανα:
#			ανα2 = ε.γ.αναγνώριση(λέξη, "κοινή")
#			if not ανα2:
#				φ.write(λέξη+"\n")
#				fcounter +=1
#			else:
#				φ2.write(λέξη+"\n")
#		else:
#			φ2.write(λέξη+"\n")
#		counter += 1
#		if counter%1000==0:
#			print(counter,fcounter)
#	
#	φ.close()
#	φ2.close()
	# TODO: αναγνώριση συνθετικού-κατάληξης-τόνου νέας λέξης
	# TODO: παραγωγή επιρρημάτων
	# TODO: όλα τα παραπάνω για ρήματα-μετοχές
	# TODO: προσθήκη μετοχών-ρημάτων δημοτικής
	# TODO: αναγνώριση-προσθήκη λέξεων hunspell
	#ε=Ελληνικά()
	#ε.serve()
	#ε.serve_develop()
	#print(ε.πολυτόνισε(κείμενο))
	#print(ε.IME.μυνήματα("δημοτική", "υποψηφιότητες", "κουζ"))
	#
	# τοπικά-σταση
	# (αντωνυμίες-θι) ἄλλοθι, αὐτοθι, 
	# (ουσιαστικά-σιν-οι)Ἀθήνησι, Ἀθήνησιν, Ὀλυμπίασι(ν), Πλαταιᾶσι(ν)
	# θύρασι(ν)
	# Ἰσθμοῖ, Μεγαροῖ, Πυθοῖ, οἴκοι,
	# τοπικά-κίνηση προς
	# -ω ἄνω, κάτω, ἔσω, εἴσω, πρόσω, πόρσω, πόρρω, 
	# -σε ἄλλοσε, αοσε, ἐκεῖσε
	# -δε Μεγαράδε, Ἐλευσινάδε,
	# -ζε οἰκόνδε, οἴκαδε, Ἀθήναζε
	# τοπικά-κίνηση από
	# -θεν ἐκεῖθεν, οἴκοθεν, ἄλλοθεν
	# -οθεν πάντοθεν, 
	# -ωθεν ἄνωθεν, ἀμφοτέρωθεν, ἑκατέρωθεν
	# τροπικά
	# επίθετα, αντωνυμίες, μετοχές σε ως
	# -δη, δον, ι, τι, ει, ς
	# ἄρδην,κρύβδην, μείγδην, φύρδην βάδην, τροχάδην, σποράδην
	# ἀριστίνδην, πλουτίνδην, ἀναφανδὸν, βοτρυδὸν, ἀγεληδὸν, κυνηδὸν, ταυρηδὸν
	# ἀμισθὶ, αὐτοχειρὶ, ἐθελοντὶ, ἀμαχητὶ, ἀγελαστὶ, ἀπνευστὶ
	# μεγαλωστὶ, νεωστὶ, ονομαστὶ, ἑλληνιστὶ, βαρβαριστὶ
	# ἀμαχεὶ, ἄσπονδεὶ, νηποινεὶ, πανδημεὶ
	# ἀναμὶζ, ἐναλλὰζ, πὺξ, λὰξ
	# ποσοτικά από αριθμό, ποσό -ς -κις -άκις
	# δὶς, τρεῖς, τρία, τρὶς
	# ἑπτάκις, δεκάκις
	# πεντάκις, ἑξάκις, ποσάκις, ὁσάκις, πολλάκις
	# χρονικά
	# -τε ἄλλοτε, ἑκάστοτε ὅτε   
	#
	#κείμενο  = "Επειδή πολλές φορές σας μίλησα για τον παράδεισο, για τους "
	#κείμενο += "Αγγέλους και για τους Αγίους, για να βοηθηθείτε, τώρα θα σας πω "
	#κείμενο += "και λίγα λόγια την κόλαση και για τους δαίμονες, ώστε να γνωρίσετε "
	#κείμενο += "με ποιους παλεύουμε, πάλι για να βοηθηθείτε."
	#ανάλυση=ε.ανάλυσε(κείμενο)
	#for στοιχείο in ανάλυση:
	#	print(στοιχείο)
	#
	# Επειδή πολλές φορές σας μίλησα για τον παράδεισο, για τους Αγγέλους και για τους Αγίους, για να βοηθηθείτε, τώρα θα σας πω και λίγα λόγια την κόλαση και για τους δαίμονες, ώστε να γνωρίσετε με ποιους παλεύουμε, πάλι για να βοηθηθείτε.
#	print(κείμενο)
#	print(ε.πολυτόνισε(κείμενο))
	
	# TODO: αναγνώριση επιρρημάτων παράγωγα επιθέτων μέσω κατάληξης
