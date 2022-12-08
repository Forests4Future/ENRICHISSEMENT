# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#================ {importation des modules} ===============
import streamlit as st
import pandas as pd
from koboextractor import KoboExtractor
import base64
import streamlit.components.v1 as components
import folium
from streamlit_folium  import folium_static
from math import*
import math

#================ {definition des fonction} ===============

def connexion_kobo(token,x):
	"""
	Cette fonction permet de se connecter à kotoolbox grace au token
	"""
	links=['https://kobo.humanitarianresponse.info/api/v2/','https://kf.kobotoolbox.org/api/v2']
	return KoboExtractor(token, links[x-1])

def metadatas(kobo):
	"""
	Renvoir la liste des metadonnées relatives au notre compte kobo
	"""
	# print(kobo.list_assets())
	return kobo.list_assets()

def donnees(kobo,x):
	"""
	Retourne les données d'un questionnaires x
	"""
	return kobo.get_asset(metadatas(kobo)['results'][x]['uid'])

def nb_questionnaires(kobo):
	assets=metadatas(kobo)
	return len(assets['results'])

def liste_questionnaires(kobo):
	assets = metadatas(kobo)
	return [assets["results"][x]["name"] for x in range(assets["count"])]

def resume(kobo,x):
	return metadatas(kobo)['results'][x]['summary']

def questions(kobo,x):
	return kobo.get_questions(asset=donnees(kobo,x), unpack_multiples=False)

def reponses(kobo,x):
	return kobo.get_data(metadatas(kobo)['results'][x]['uid'])


def changer_bg(image,ext):

	main_bg = image
	main_bg_ext = ext

	side_bg = image
	side_bg_ext = ext

	st.markdown(
	    f"""
	    <style>
	    .reportview-container {{
	        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
	    }}
	   .sidebar .sidebar-content {{
	        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
	    }}
	    </style>
	    """,
	    unsafe_allow_html=True
	)
	pass



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
	
	ForetProche=[(distanceCart(coordJachereSelectionnee, foret[0]),foret[0],foret[2]) for foret in coordForet]
	ForetProche.sort(reverse = False, key = lambda t: t[0])
	print(ForetProche[0])
	return ForetProche[0]



#================ {initialisation des variables} ===============
token="5f775cda8cba25811855eca4e3ca345f1ad0d4d4"
kobo=connexion_kobo(token,0)
assets=metadatas(kobo)
nb_quest=nb_questionnaires(kobo)
