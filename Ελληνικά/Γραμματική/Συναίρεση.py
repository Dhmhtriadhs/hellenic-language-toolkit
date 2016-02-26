#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, dimitriadis dimitris
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

class Συναίρεση():
	def __init__(self):
		self._συναιρέσεις = {
			"α":{"α":"α", "αυ":"αυ", "ᾳ":"ᾳ", "αι":"αι", "ε":"α","η":"α", "ει":"ᾳ","ῃ":"ᾳ",
					"ο":"ω","ω":"ω","ου":"ω","οι":"ῳ"	},
			"η":{"ε":"η", "ει":"ῃ",
				"ω":"ω", "ο":"ω", "ου":"ω", "οι":"ῳ", },
			"ε":{"α":"η", "ε":"ει", "ο":"ου","ω":"ω", "ου":"ου","ᾳ":"ῃ", "αι":"αι", "οι":"οι"},
			"ο":{"ε":"ου", "ο":"ου", "α":"α", "ου":"ου", "ῳ":"ῳ", "οι":"οι", "ω":"ω", "ι":"οι"},
			"οι":{"α":"ε"},
			"ω":{"οι":"ῳ", "α":"ω"},
			"ου":{"ε":"ου", "α":"α"},
			"αι":{"ε":"α", "ει":"ᾳ"},
			"κ":{"σ":"ξ", "σθ":"χθ", "θ":"χθ", "μ":"γμ", "τ":"κτ", "j":"σσ" },
			"γ":{"σ":"ξ", "σθ":"χθ", "θ":"χθ", "μ":"γμ", "τ":"κτ", "j":"σσ"  },
			"χ":{"σ":"ξ", "σθ":"χθ", "θ":"χθ", "μ":"γμ", "τ":"κτ", "j":"σσ"  },	
			"π":{"σ":"ψ", "σθ":"φθ", "θ":"φθ", "μ":"μμ", "τ":"πτ", "δ":"βδ", "ντ":"ντ" },	
			"β":{"σ":"ψ", "θ":"φθ", "μ":"μμ", "τ":"πτ", "δ":"βδ" },
			"φ":{"σ":"ψ", "θ":"φθ", "μ":"μμ", "τ":"πτ", "δ":"βδ" },
			"τ":{"σ":"σ", "θ":"σθ", "μ":"σμ", "τ":"στ" },
			"δ":{"σ":"σ", "θ":"σθ", "μ":"σμ", "τ":"στ", "j":"ζ" },
			"θ":{"σ":"σ", "θ":"σθ", "μ":"σμ", "τ":"στ" },	
			"ντ":{"j":"σ","σ":"σ",},
			"μ":{"ρ":"μβρ"},
			"σ":{"σ":"σ"},
			"νδ":{"σ":"σ"},
			"νθ":{"σ":"σ"},
			"λ":{"j":"λλ", "σθ":"λθ"},
			"ρ":{"j":"ρρ", "σθ":"ρθ"},
			"αν":{"j":"αιν"},
			"αρ":{"j":"αιρ"},
			"ορ":{"j":"οιρ"},
			"ν":{"κ":"γκ", "γ":"γγ", "χ":"γχ", "ξ":"γξ", "πν":"μπν", "β":"μβ", "φ":"μφ", "ντ":"ντ",
				"ψ":"μψ", "σ":"σ", "σθ":"νθ", "ρ":"νδρ", "π":"μπ", "λ":"λλ", "ρ":"ρρ", "μ":"μμ", "μ":"σμ", }
			}
			
	def ένωση(self, λέξη, κατάληξη):
		νέα_λέξη = λέξη + κατάληξη
		if λέξη[-2:] in self._συναιρέσεις and\
			κατάληξη[:2] in self._συναιρέσεις[λέξη[-2:]]:
			νέα_λέξη = λέξη[:-2]+self._συναιρέσεις[λέξη[-2:]][κατάληξη[:2]]+κατάληξη[2:]
		elif λέξη[-2:] in self._συναιρέσεις and\
			κατάληξη[0] in self._συναιρέσεις[λέξη[-2:]]:
			νέα_λέξη = λέξη[:-2]+self._συναιρέσεις[λέξη[-2:]][κατάληξη[0]]+κατάληξη[1:]
		elif λέξη[-1] in self._συναιρέσεις and\
			κατάληξη[:2] in self._συναιρέσεις[λέξη[-1]]:
			νέα_λέξη = λέξη[:-1]+self._συναιρέσεις[λέξη[-1]][κατάληξη[:2]]+κατάληξη[2:]
		elif λέξη[-1] in self._συναιρέσεις and\
			κατάληξη[0] in self._συναιρέσεις[λέξη[-1]]:
			νέα_λέξη = λέξη[:-1]+self._συναιρέσεις[λέξη[-1]][κατάληξη[0]]+κατάληξη[1:]
		return νέα_λέξη
			