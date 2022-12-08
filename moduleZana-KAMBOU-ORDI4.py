# -*- coding: utf-8 -*-
from __future__ import unicode_literals
def condition(P,T,R):
	if P < 1000:
		P=(1000-P)*0.1 if (1000-P) >0
	else: 
		P=0
	if T < 400:
		return (400-T)*0.25 if (400-T) >0
	else: 
		T=0
	if R < 100:
		R= R
	else: 
		R=0
	return P+T+R
# Le nombre minimum d'espèces à introduire est: P+T+R 