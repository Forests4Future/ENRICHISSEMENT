# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math

def distanceCart(coordJachere,coordForet):
	'''
	cette fonction nous permet de calculer la distance cartesienne entre une jachere et une foret
	coordJachere: Coordonnées de la jachere selectionnée
	coordForet: Coordonnées de la forêt selectionnée
	'''
	distance = math.dist(coordJachere, coordForet)
	return distance

def plusProcheForet(coordJachereSelectionnee, coordForet):
	'''
	Determine la distance entre la jachere selectionnée et la forêt la plus proche d'elle
	coordJachereSelectionnee: coordonnées de la jachere selectionnée
	coordForet: la liste de données de coordonnées de toutes les forêts
	'''
	
	distanceForet=[(distanceCart(coordJachereSelectionnee, foret[0]),foret[0],foret[1]) for foret in coordForet]
	distanceForet.sort(reverse = False, key = lambda t: t[0])
	# print(distanceForet)
	return distanceForet