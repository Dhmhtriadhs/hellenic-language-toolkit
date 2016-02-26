#!/usr/bin/python3.2
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

import os, json
if "Γραμματική" in os.getcwd():
	φάκελος = "."
else:
	φάκελος = 'Γραμματική'

class Επιρρήματα():
	def __init__(self, τονιστής, αναγνώριση):
		self.τ = τονιστής
		self.λέξεις = {}
		self.αναγνώριση = αναγνώριση.αναγνώριση
		
		self.ευρετήριο = {"κοινή":{}, "δημοτική":{}}
		self.bευρετήριο = {"κοινή":{}, "δημοτική":{}}
		self.όρια = {"κοινή":{}, "δημοτική":{}}
		self.α = self.τ.κωδικοποιητής("α")
		self.ως = self.τ.κωδικοποιητής("ως")
