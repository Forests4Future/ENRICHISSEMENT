# -*- coding: utf-8 -*-
#================ {Importation des modules python} ===============
from __future__ import unicode_literals
import streamlit as st
# Modules d'authentification
import streamlit_authenticator as stauth
import yaml
# Modules mathematique et manipulation de données
import numpy as np
import time
import math
import pandas as pd
from fonctionKobo import*
# Module de cartographie
from fonctionCarto import*
from streamlit_folium import st_folium
import folium
# calcul d'indice
from sorensen import*

from st_aggrid import AgGrid
#================ {initialisation des variables} ===============

nb_quest=nb_questionnaires(kobo)
forets = reponses(kobo, 1)
jacheres = reponses(kobo, 0)
Foret_proche=''
infoJacheres=[(jachere["_geolocation"],"Id:"+jachere["info_gen/Id_Jach_re"]+"\n Nom du propiétaire:"+jachere["info_gen/Nom_du_propri_taire"]+"\n Surface:"+jachere["info_gen/calculation"],jachere["info_gen/Id_Jach_re"]) for jachere in jacheres["results"]]
idJacheres=[x[2] for x in infoJacheres]
infoForets=[(foret["_geolocation"],"Id:"+foret["info_gen/ID_For_t"],foret["info_gen/ID_For_t"]) for foret in forets["results"]] 
ArbresForets=[{"id":foret["info_gen/ID_For_t"],"dbh10":foret["dbh_10_cm"],"seedlings":foret["Seedlings"]} for foret in forets["results"]] 
ArbresJacheres=[{"id":jachere["info_gen/Id_Jach_re"],"surface":jachere["info_gen/calculation"],"dbh10":jachere["dbh_10_cm"],"saplines":jachere["Saplines"],"seedlings":jachere["Seedlings"]} for jachere in jacheres["results"]]


# listeArbresForets=listeArbres("f",ArbresForets)
# listeArbresJacheres=listeArbres("j",ArbresJacheres)
# ArbresForets
# listeArbresForets
# selectPlot=[(jachere["_geolocation"], foret["_geolocation"], jachere["info_gen/Id_Jach_re"], foret["info_gen/ID_For_t"])]
# indsorensens=[foret["dbh_10_cm/Nom_commun"], foret["dbh_10_cm/Nom_scientifique"], foret["Seedlings/Nom_commun_001"], foret["Seedlings/Nom_scientifique_001"], jachere["dbh_10_cm/Nom_commun"], jachere["dbh_10_cm/Nom_scientifique"], jachere["Saplines/Nom_commun_001"], jachere["Saplines/Nom_scientifique_001"], jachere["Seedlings/Nom_commun_002"], jachere["Seedlings/Nom_scientifique_002"]]
# listDIFFERENCE = nom scientifique de la foret qui n'apparait pas dans jachere
# listSODEFOR
# comparer listSODEFOR à la listDIFERNECE: [list SODEFOR, foret["dbh_10_cm/Nom_scientifique"], foret["Seedlings/Nom_scientifique_001"]] = listPLANTING
# QuantitéparclasseDBH dans jachere=[jachere["dbh_10_cm/DBH"], jachere["Saplines/DBH_001"], jachere["Seedlings/Quantit_de_l_ep_ce"]]
# Ramener les quantités à l'hectare
# Affecter les quantités à listPLANTING en fonction des quantités pour les différentes classes de DBH = ENRICHISSEMENT

# Associer ENRICHISSEMENT à "Id:"+jachere["info_gen/Id_Jach_re"] correspondant
# hashed_passwords = stauth.Hasher(['123', '456']).generate()
# hashed_passwords
#================[définition des fonctions]===============
m = folium.Map(location=[7.973052807196834, -5.651763632750226], zoom_start=6.5)

def MarketForet(ForetProche,jachere):
    distanceForetProcheDegres=ForetProche[0]
    distanceForetProcheMetre=distanceForetProcheDegres*111200
    folium.Circle(location=jachere,radius=distanceForetProcheMetre, fill_color='red').add_to(m)


def condition(P,T,R):
    if P < 1000 and (1000-P) >0:
        P=(1000-P)*0.1
    else: 
        P=0
    if T < 400 and (400-T) >0:
        T=(400-T)*0.25
    else: 
        T=0
    if R < 100:
        R= R
    else: 
        R=0
    return [P,T,R]
# Le nombre minimum d'espèces à introduire est: P+T+R 


def ajouterPoint(genre,infoPoint,color,idJachere=""):
    """
    Elle permet d'ajouter un nouveau point à la carte en utilisant ses coordonnées et la donnée à ajouter en popup
    """
    global dansForetEtSodefor
    # reccuperation de la coordonnée, de l'id et de l'info de popup du point
    coordonneePoint=infoPoint[0]
    idPoint=infoPoint[2]
    popupPoint=infoPoint[1]

    # On verifie si le point a ajouter à la carte est une jachere
    if genre=='j':
        # Si c'est une jachere on verifie si c'est la jachere que nous avons selctionnée
        if idJachere==idPoint:
            # Si c'est bien la jachere que nous avons selectionner, on la colorie en rouge
            iconPoint=folium.Icon(color="red")
            # On determie la forêt qui est la plus proche d'elle
            ForetProche=plusProcheForet(coordonneePoint,infoForets)
            Foret_proche=ForetProche
            st.title('Plus proche forêt:')
            st.title(Foret_proche[2])
            #================[arbres de foret proche]===============
            arbresFP=arbresForetProche(ArbresForets,Foret_proche)
            uniqueFP=unique(arbresFP)
            st.write(card(uniqueFP), "espèces dans la forêt la plus prôche")
            #================[arbres de jachere selectionnée]===============
            arbreJA=arbresJachereSelec(ArbresJacheres,JachereSelectionnee)
            uniqueJA=unique(arbreJA)
            st.write(card(uniqueJA),'espèces dans la jachere')
            st.write(len(AinterB(uniqueJA,arbresFP)), 'espèces communes au 2 biotopes')
            commun=AinterB(uniqueJA,arbresFP)
            st.write(AinterB(uniqueJA,arbresFP))
            soren=sorensen(uniqueJA,uniqueFP)
            st.title('Indice de sorensen:')
            st.write(round(float(soren), 2), "%")
            dansForetPasDansJachere=AsansB(uniqueFP,arbreJA)
            df=pd.read_csv("data_especes_sodefor.csv",sep=';')
            espece_sodefor=df.noms_scient
            dansForetEtSodefor=AinterB(list(espece_sodefor),dansForetPasDansJachere)
            st.write("Liste des espèces de la forêt proche coummune à celle de la SODEFOR")
            st.write(dansForetEtSodefor)
            densiteDesSeedlings=DensiteSeedlings(ArbresJacheres,JachereSelectionnee)
            st.write("Densité des plantules:",int(densiteDesSeedlings))
            densiteSapline=DensiteArbresSaplines(ArbresJacheres,JachereSelectionnee)
            st.write("Densité des tiges:",int(densiteSapline))
            densiteDesBigTrees=DensiteArbresDbh10(ArbresJacheres,JachereSelectionnee)
            st.write("Densité des gros arbres :",int(densiteDesBigTrees))
            nb_arbre_ajouer=condition(densiteDesSeedlings,densiteSapline,densiteDesBigTrees)
            nbArbreAajouter=int(sum(nb_arbre_ajouer))
            st.write(int(sum(nb_arbre_ajouer)), "plants au minimum à apporter pour l'enrichissement de la jachère")
            listeArbresEnrich=st.multiselect("Selectionner les espèces d'enrichissement à ajouter:", list(dansForetEtSodefor))
            volonte=volonteProd(jacheres,JachereSelectionnee)
            if len(volonte)>0:
                listeArbresEnrichVolontePro=st.multiselect("Selectionner des espèces de la liste de volonté du propriétaire:", volonte)
            nb_especes=len(listeArbresEnrich)+len(listeArbresEnrichVolontePro)
            st.write(len(listeArbresEnrich)+len(listeArbresEnrichVolontePro), "espèces selectionnées pour l'enrichissement de la jachère")
            EspecesEnriFinal=listeArbresEnrich+listeArbresEnrichVolontePro
            quantiteParEspece=[int((nbArbreAajouter)/nb_especes+1) for x in range(nb_especes)]
            dicoListEspeces={"Espèce":EspecesEnriFinal,"Quantité de l'espèce":quantiteParEspece}
            dataframe=pd.DataFrame.from_dict(dicoListEspeces)
            reponse=AgGrid(dataframe,editable=True)['data']
            quantiteTotal=sum(reponse["Quantité de l'espèce"])
            st.write("Le nombre total de plants à apporter pour l'enrichissement de la jachère est:",quantiteTotal)
            # quantiteParEspece.append(sum(reponse["Quantité de l'espèce"]))

            # print("la forêt la plus proche est:",Foret_proche[2])
            # On marque la distance entre notre jachere et la forêt qui est plus proche d'elle
            MarketForet(ForetProche,coordonneePoint)
        else:
            # Si le point à ajouter à la carte n'est pas la jachere que nous avons selectionnée,
            # alors on conserve la couleur
            iconPoint=folium.Icon(color=color)
    # Si le point est une forêt, on conserve sa couleur
    else:
        iconPoint=folium.Icon(color=color)
    # Ajout du point à la carte que base que nous avons crée
    folium.Marker(coordonneePoint, popup=popupPoint, icon=iconPoint ).add_to(m)

#================ {Authentification de l'utilisateur} ===============
with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)
# jacheres
# forets
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Connexion', 'main')

#================ {Programme après login} ===============
if authentication_status:
    st.markdown("# Bienvenue sur Forests4Future 🌱")
    st.image("logoF4F.jpg")
    st.sidebar.title(f'Bienvenue *{name}*')
    with st.sidebar:
        authenticator.logout('Déconnexion', 'main')

    JachereSelectionnee=st.selectbox("Selectionnez votre jachère",idJacheres)
    if JachereSelectionnee:
        for Jachere in infoJacheres:
            ajouterPoint(genre='j',infoPoint=Jachere,color="green",idJachere=JachereSelectionnee)
        for foret in infoForets:
            ajouterPoint(genre="f",infoPoint=foret, color='blue',idJachere='')
    st_data = st_folium(m, width = 725)



elif authentication_status == False:
    st.error('Utilisateur/mot de passe incorrecte')
elif authentication_status == None:
    st.warning('Saisir vos identifiants de connexion')



# selection
# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')
# st.button("Bouton1")

# tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
# data = np.random.randn(10, 1)

# tab1.subheader("A tab with a chart")
# tab1.line_chart(data)

# tab2.subheader("A tab with the data")
# tab2.write(data)