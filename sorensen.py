# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from math import*

ns_dbhj="dbh_10_cm/Nom_scientifique"
ns_sapj="Saplines/Nom_scientifique_001"
ns_seedj="Seedlings/Nom_scientifique_002"
ns_dbhf="dbh_10_cm/Nom_scientifique"
ns_seedf="Seedlings/Nom_scientifique_001"


def unique(liste):
	return set(liste)

def card(liste):
	return len(liste)

def AinterB(A,B):
	AIB=unique(A).intersection(B)
	return AIB

def AsansB(A,B):
	return set(A).difference(B)


def arbresForetProche(tousArbresForets,idForetProche):
	# print(tousArbresForets)
	print('id de la forêt',idForetProche[2])
	idForetProche=idForetProche[2]
	ForetsProches_arbresDbh10=[foret["dbh10"] for foret in tousArbresForets if foret["id"]==idForetProche][0]
	ForetsProches_arbresSeedl=[foret["seedlings"] for foret in tousArbresForets if foret["id"]==idForetProche][0]
	ns_dbh10=[arbre[ns_dbhf] for arbre in ForetsProches_arbresDbh10 if arbre.setdefault(ns_dbhf, 'faux')!="faux" and arbre["dbh_10_cm/Nom_commun"]!="NA"]
	ns_seedl=[arbre[ns_seedf] for arbre in ForetsProches_arbresSeedl if arbre.setdefault(ns_seedf, 'faux')!="faux" and arbre["Seedlings/Nom_commun_001"]!="NA"]

	return ns_dbh10+ns_seedl

def arbresJachereSelec(tousArbresJachere,idjachere):
	ForetsProches_arbresDbh10=[jachere["dbh10"] for jachere in tousArbresJachere if jachere["id"]==idjachere][0]
	ForetsProches_arbresSeedl=[jachere["seedlings"] for jachere in tousArbresJachere if jachere["id"]==idjachere][0]
	ForetsProches_arbresSapl=[jachere["saplines"] for jachere in tousArbresJachere if jachere["id"]==idjachere][0]
	ns_dbh10=[arbre[ns_dbhj] for arbre in ForetsProches_arbresDbh10 if arbre.setdefault(ns_dbhj, 'faux')!="faux" and arbre["dbh_10_cm/Nom_commun"]!="NA"]
	ns_seedl=[arbre[ns_seedj] for arbre in ForetsProches_arbresSeedl if arbre.setdefault(ns_seedj, 'faux')!="faux" and arbre["Seedlings/Nom_commun_002"]!="NA"]
	ns_sapl=[arbre[ns_sapj] for arbre in ForetsProches_arbresSapl if arbre.setdefault(ns_sapj, 'faux')!="faux" and arbre["Saplines/Nom_commun_001"]!="NA"]

	return ns_dbh10+ns_seedl+ns_sapl

def DensiteArbresDbh10(tousArbresJachere,idjachere):
	Jacher_arbresDbh10=[(jachere["dbh10"],float(jachere["surface"])) for jachere in tousArbresJachere if jachere["id"]==idjachere][0]
	ns_dbh10=[arbre[ns_dbhj] for arbre in Jacher_arbresDbh10[0] if arbre.setdefault(ns_dbhj, 'faux')!="faux" and arbre["dbh_10_cm/Nom_commun"]!="NA"]
	return len(ns_dbh10)/Jacher_arbresDbh10[1]


def DensiteArbresSaplines(tousArbresJachere,idjachere):
	Jacher_arbresSapl=[jachere["saplines"] for jachere in tousArbresJachere if jachere["id"]==idjachere][0]
	ArbresSaplingsReel=[arbre for arbre in Jacher_arbresSapl if arbre.setdefault("Saplines/DBH_001", 'faux')!="faux" and float(arbre.setdefault("Saplines/DBH_001", 'faux'))>=7.85 and float(arbre.setdefault("Saplines/DBH_001", 'faux'))<31.4 ]
	return len(ArbresSaplingsReel)/0.2

def DensiteSeedlings(tousArbresJachere,idjachere):
	ForetsProches_arbresSeedl=[jachere["seedlings"] for jachere in tousArbresJachere if jachere["id"]==idjachere][0]
	ns_seedl=[int(arbre["Seedlings/Quantit_de_l_ep_ce"]) for arbre in ForetsProches_arbresSeedl if arbre.setdefault(ns_seedj, 'faux')!="faux" and arbre["Seedlings/Nom_commun_002"]!="NA"]
	nb_arbres=sum(ns_seedl)
	return nb_arbres/(125/10000)

def volonteProd(tousJacheres,idjachere):
	volonteProdBase=[jachere["info_gen/Volont_proprio"] for jachere in tousJacheres["results"] if jachere["info_gen/Id_Jach_re"]==idjachere]
	volonteProdBase=volonteProdBase[0].split(" ")
	# volonteProdBase=volonteProdBase[0].split(" ")
	volonteProdBaseAutre=''
	if "si_autre__p_cisez" in volonteProdBase:
		# volonteProdBase=volonteProdBase.remove("si_autre__p_cisez")
		volonteProdBaseAutre=[jachere["info_gen/Autre_s_essence_s_voulue_s"] for jachere in tousJacheres["results"] if jachere["info_gen/Id_Jach_re"]==idjachere]
		volonteProdBaseAutre=volonteProdBaseAutre[0].split(',')
	# return volonteProdBaseAutre, volonteProdBase
	concatVol=list(volonteProdBase)+list(volonteProdBaseAutre)
	# return concatVol
	if "si_autre__p_cisez" in concatVol:
	# if '' in concatVol:
		concatVol.remove('si_autre__p_cisez')
	return concatVol

def listeArbres(genre,liste):
	'''
	genre est une clé et est egale a f ou j
	liste est une liste de dictionnaire
	'''
	
	if genre=="f":
		listedbh=[x["dbh10"] for x in liste]
		print(listedbh)
		listeseedl=[x["seedlings"] for x in liste]
		print(listeseedl)
		# arbres=arbresCategorie(listedbh[0],ns_dbhf)+arbresCategorie(listeseedl[0],ns_seedf)
	else:
		listedbh=[x["dbh10"] for x in liste]
		# print(listedbh)
		listeseedl=[x["seedlings"] for x in liste]
		listesap=[x["saplines"] for x in liste]
		arbres=arbresCategorie(listesap[0], ns_sapj)+arbresCategorie(listedbh[0], ns_dbhj)+arbresCategorie(listeseedl[0],ns_seedj)
	return arbres



def sorensen(A,B):
	A=unique(A)
	B=unique(B)
	cardA=card(A)
	cardB=card(B)
	AIB=AinterB(A,B)
	cardAIB=card(AIB)
	isorensen=(2*(cardAIB)/(cardA+cardB))*100
	return isorensen
