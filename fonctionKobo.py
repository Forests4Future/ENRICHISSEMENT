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
	return kobo.list_assets()

def donnees(kobo,x):
	"""
	Retourne les données d'un questionnaires x
	"""
	return kobo.get_asset(metadatas(kobo)['results'][x]['uid'])


def nb_questionnaires(kobo):
	'''
	Cette fonction retourne le nombre de question dans notre 
	Base de données kobotoolbox
	'''
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


#================ {initialisation des variables} ===============
# Recupération de clé de connexion
token="5f775cda8cba25811855eca4e3ca345f1ad0d4d4"
kobo=connexion_kobo(token,0)
assets=metadatas(kobo)
nb_quest=nb_questionnaires(kobo)