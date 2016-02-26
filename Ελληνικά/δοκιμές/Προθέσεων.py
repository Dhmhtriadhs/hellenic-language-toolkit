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

τύπωσε = print
κείμενο = str
λίστα = list
μήκος = len
εύρος = range
ακέραιος = int
τίποτα = None
ναι = True
όχι = False

class Δοκιμές_Προθέσεων():
	def __init__(self, γραμματική):
		self.αναγνώριση = γραμματική.αναγνώριση
		self.δεδομένα_αναγνώρισης = []

	def δοκιμές_αναγνώρισης(self):
		δεδομένα_αναγνώρισης = [
			["εἰς",    "κοινή",   "κύρια"], ["ἐν",   "κοινή", "κύρια"],
			["ἐκ",     "κοινή",   "κύρια"], ["ἐξ",   "κοινή", "κύρια"],
			["πρό",    "κοινή",   "κύρια"], ["πρός", "κοινή", "κύρια"],
			["σύν",    "κοινή",   "κύρια"], ["ἀνά",  "κοινή", "κύρια"],
			["διά",    "κοινή",   "κύρια"], ["κατά", "κοινή", "κύρια"],
			["μετά",   "κοινή",   "κύρια"], ["παρὰ", "κοινή", "κύρια"],
			["ἀμφί",   "κοινή",   "κύρια"], ["ἀντί", "κοινή", "κύρια"],
			["ἐπί",    "κοινή",   "κύρια"], ["περὶ", "κοινή", "κύρια"],
			["ἀπό",    "κοινή",   "κύρια"], ["ὑπὸ",  "κοινή", "κύρια"],
			["ὑπέρ",   "κοινή",   "κύρια"],
			["ἄχρι",   "κοινή",   "καταχρηστική γενική"],
			["μέχρι",  "κοινή",   "καταχρηστική γενική"],
			["ἄνευ",   "κοινή",   "καταχρηστική γενική"],
			["χωρίς",  "κοινή",   "καταχρηστική γενική"],
			["πλήν",   "κοινή",   "καταχρηστική γενική"],
			["ἕνεκα",  "κοινή",   "καταχρηστική γενική"],
			["ἕνεκεν", "κοινή",   "καταχρηστική γενική"],
			["ὡς",     "κοινή",   "καταχρηστική αιτιατική"],
			["νή",     "κοινή",   "καταχρηστική αιτιατική"],
			["μὰ",     "κοινή",   "καταχρηστική αιτιατική"],
			["μὲ",     "δημοτική", "κύρια"], ["σὲ",     "δημοτική", "κύρια"],
			["γιὰ",    "δημοτική", "κύρια"], ["ὡς",     "δημοτική", "κύρια"],
			["ἔως",    "δημοτική", "κύρια"],	["πρός",   "δημοτική", "κύρια"],
			["κατά",   "δημοτική", "κύρια"],	["μετά",   "δημοτική", "κύρια"],
			["παρά",   "δημοτική", "κύρια"],	["ἀντί",   "δημοτική", "κύρια"],
			["ἀντίς",  "δημοτική", "κύρια"],	["ἀπό",    "δημοτική", "κύρια"],
			["δίχως",  "δημοτική", "κύρια"], ["χωρίς",  "δημοτική", "κύρια"],
			["ἴσαμε",  "δημοτική", "κύρια"],
			["διά",    "δημοτική", "απαρχαιωμένη"],
			["ἐκ",     "δημοτική", "απαρχαιωμένη"],
			["ἐξ",     "δημοτική", "απαρχαιωμένη"],
			["ἐν",     "δημοτική", "απαρχαιωμένη"],
			["ἐπί",    "δημοτική", "απαρχαιωμένη"],
			["περὶ",   "δημοτική", "απαρχαιωμένη"],
			["πρό",    "δημοτική", "απαρχαιωμένη"],
			["ὑπέρ",   "δημοτική", "απαρχαιωμένη"],
			["ὑπό",    "δημοτική", "απαρχαιωμένη"],
			["πλήν",   "δημοτική", "απαρχαιωμένη"],
			["μεῖον",  "δημοτική", "απαρχαιωμένη"],
			["σῦν",    "δημοτική", "απαρχαιωμένη"],
			]
		μετρητής, αποτυχίες = 0, 0

		for σύνολο in δεδομένα_αναγνώρισης:
			αποτέλεσμα = self.αναγνώριση(σύνολο[0], σύνολο[1])
			if not αποτέλεσμα:
				τύπωσε("   ΑΝΑΜΕΝΟΤΑΝ:",σύνολο,"ΑΠΟΤΕΛΕΣΜΑ:",  αποτέλεσμα)
				αποτυχίες += 1
			else:
				nfound = False
				for α in αποτέλεσμα:
					if α["μέρος του λόγου"]=="πρόθεση" and\
						σύνολο[2] in α["Μεταδεδομένα"]['ιδιότητες']:
						nfound = True
						break
				if not nfound:
					τύπωσε("   ΑΝΑΜΕΝΟΤΑΝ:",σύνολο,"ΑΠΟΤΕΛΕΣΜΑ:",  αποτέλεσμα)
					αποτυχίες += 1
			μετρητής += 1
		τύπωσε("Δοκιμές αναγνώρισης Προθέσεων", "Δοκιμές:", μετρητής," Αποτυχίες:",αποτυχίες)

if __name__=="__main__":
	δπ = Δοκιμές_Προθέσεων()
	δπ.δοκιμές_αναγνώρισης()