#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 17:09:02 2020

@author: darankoum_davy_b
"""


#1. Importation des librairies dont on a besoin ############
import pandas as pd
import numpy as np
import nltk
import re
import os
import pickle

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from country_list import countries_for_language
from langdetect import detect_langs
from gensim.parsing.preprocessing import STOPWORDS


import json
import mpld3

from datetime import datetime
from pprint import pprint
import matplotlib.pyplot as plt

#Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image

import Labelisation
############### Fin importation ##############################



#2. Fonctions de sauvegarde et de chargement de dictionnaires avec des fichiers
    # Utilisé pour gagner du temps afin de ne pas avoir à re-exécuter tout
    # à chaque ré-ouverture
def save_dict(dico, filename) :
    with open("dict/"+filename+".pickle", 'wb') as handle:
        pickle.dump(dico, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_dict(filename) :
    with open("dict/"+filename+".pickle", 'rb') as handle:
        return(pickle.load(handle))

def fonction_Principale(leDictGeneral, mallet_path, Dict_onlyEnglish):
    
    #############################
    
    
    #3. lemmatized_titles : le dictionnaire ayant pour clefs les ids des publications et les values sont
                            #sont des listes contenant des tokens pour chaque titre 
    lemmatized_titles = load_dict(leDictGeneral) 
    ############################
       
    
    #4. Je transforme ce dictionnaire en list de ses valeurs afin de permettre
    #la création des id2word et du corpus qui servent à la construction d'un modèle LDA
    final_titles = lemmatized_titles   
    final_titles = list(final_titles.values())
    ############################
    
    
    #5. Création des paramètres id2word et corpus qui sont des paramètres pour le modèle LDA
    # Create Dictionary
    id2word = corpora.Dictionary(final_titles)
    # Create Corpus
    texts = final_titles
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    ############################
    
    print("5 OK")
    
    #6. Construction du modèle LDA en précisant 10 topics à rechercher 
    #et demandant 10 itérations au total de l'algo
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                               id2word=id2word,
                                               num_topics=30, 
                                               passes=50)
    save_dict(lda_model, "lda_model_30_50") #J'enregistre le résultat du modèle ******************************
    
    #lda_model = load_dict("lda_model_30_100") 
    ############################
    print("6 OK")
        
    #7. Certaines analyses pour déduire le meilleur nombre de topics à préciser
        #afin d'obtenir un résultat plus pertinent du modèle
    
    #7.a) Visualisation des topics
    import pyLDAvis
    import pyLDAvis.gensim  # don't skip this

    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)

    pyLDAvis.save_html(vis, 'Doc_Essai/lda.html')        #******************************
    ############################
    print("7.a OK")
    
    #7.b) Analyse par la courbe de décroissance pour LDA gensim
    # Cette fonction retourne pour un certain nombre de topics, le score de cohérence 
    # qui est issu des résulats du modèle
    def compute_coherence_values(modelType,dictionary, corpus, texts, limit, start=2, step=3):

        coherence_values = []
        All_topics = []
        for num_topics in range(start, limit, step):
            if modelType =="Mallet":
                model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
            elif modelType =="LDA": 
                model = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=id2word,num_topics=num_topics, passes=10)
            All_topics.append(num_topics)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_Score_i = coherencemodel.get_coherence()
            coherence_values.append(coherence_Score_i)
            #print (num_topics, coherence_Score_i)

        return All_topics, coherence_values
    
    
    # html_Name ="Topic.html"
    def affichage_Courbe_décroissance(x_LDA_Mallet, coherence_value_LDA_Mallet, html_Name):
        fig1 = plt.figure()
        plt.plot(x_LDA_Mallet, coherence_value_LDA_Mallet)
        points = plt.scatter(x_LDA_Mallet, coherence_value_LDA_Mallet)


        plt.xlabel("Num Topics")
        plt.ylabel("Coherence score")
        plt.legend(("coherence_values"), loc='best')
        #plt.show()

        tooltip = mpld3.plugins.PointLabelTooltip(points)
        mpld3.plugins.connect(fig1, tooltip)

        #mpld3.plugins.connect(fig1,PointLabelTooltip(points))

        mpld3.fig_to_html(fig1)

        mpld3.save_html(fig1, html_Name) #****************************** (2 html : LDA simple et Mallet)
        plt.close(fig1)
    
    #Les appels de fonctions
    All_topics1, coherence_values1 = compute_coherence_values("LDA",dictionary=id2word, corpus=corpus, texts=final_titles, start=2, limit=6, step=2)
    affichage_Courbe_décroissance(All_topics1, coherence_values1, "Doc_Essai/courbe_For_LDA_gensim.html")
    
    ############################
    
    
    #8. Implémentation de Mallet LDA
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=30, id2word=id2word)
    save_dict(ldamallet, "ldamallet_30_loulou") #******************************'''
    #ldamallet = load_dict("ldamallet_30")
    Labelisation.fonction_Labelisation(ldamallet)
    ############################
    print("8 OK")
    
    #9. Analyse par la courbe de décroissance pour Mallet
    All_topics2, coherence_values2 = compute_coherence_values("Mallet",dictionary=id2word, corpus=corpus, texts=final_titles, start=5, limit=20, step=5)
    affichage_Courbe_décroissance(All_topics2, coherence_values2, "Doc_Essai/courbe_For_LDA_Mallet.html")
    ############################
    
    print("9 OK")
    
    
    #10. Création du dataframe dans lequel on affecte le topic dominant à chaque titre
    def format_topics_sentences(ldamodel, corpus, texts):
        # df de sorti
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row in enumerate(ldamodel[corpus]):
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                # Essayer de récup numtopic et sa prop sans le If !!!
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
                    break
                    
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Ajouter les titres originaux
        lesBonTitres = load_dict(Dict_onlyEnglish)
        lesBonTitresKeys = pd.DataFrame(lesBonTitres.keys())#Les id des titres
        lesBonTitresValues = pd.DataFrame(lesBonTitres.values())#Les titres
        sent_topics_df = pd.concat([sent_topics_df, lesBonTitresKeys], axis=1)
        sent_topics_df = pd.concat([sent_topics_df, lesBonTitresValues], axis=1)

        return(sent_topics_df)
    
    #Appel de la fonction
    df_topic_sents_keywords = format_topics_sentences(ldamallet, corpus, texts)
    
    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Titles_ID', 'Titles']
    
    save_dict(df_dominant_topic, "df_dominant_topic_Mallet_30_2")#******************************

    #df_dominant_topic = load_dict("df_dominant_topic_Mallet_30_2")
    ############################
    print("10 OK")
    
    #11. Analyse de la distribution du nombre de titres par topic
    #histo_Name = "Histo.html"
    def Hist_Nb_Titles_by_Topic(n,df_dominant_topic):
        df_Topic_Final = df_dominant_topic

        numTopic = []
        nbTitles_by_Topic =[]
        for i in range(0,n):
            numTopic.append(str(i))
            nbTitle_i = df_Topic_Final.loc[df_Topic_Final.Dominant_Topic==i,:]
            nbTitles_by_Topic.append(len(nbTitle_i))

        fig2=plt.figure()
        plt.bar(numTopic, nbTitles_by_Topic)
        #plt.show()  
        mpld3.fig_to_html(fig2)

        mpld3.save_html(fig2, "Doc_Essai/histo.html") #******************************
        plt.close(fig2)
    #Appel de la fonction
    Hist_Nb_Titles_by_Topic(30,df_dominant_topic)
    ############################
    print("11 OK")
    
    
    #12. Generation des 30 nuages de mots 
    def generation_Nuage_Mots(ldamallet):
        text =[]
        for i in range(30):
            wp = ldamallet.show_topic(i)
            listWords =[word for word, prop in wp]
            listProp =[prop*65959 for word, prop in wp] # Il y'a 65959 mots distincts dans tous les titres
            topicText = np.repeat(listWords,listProp)
            topicText = ", ".join(topicText)
            text.append(topicText)


        #Une fois qu'on le texte contenant tous les mots repétés de chaque topic : text, on construit
        #les nuages pour chaque topic
        for j in range(30):
            wc = WordCloud()
            wc.generate(text[j])

            c = plt.figure()
            plt.imshow(wc, alpha=1, extent=(-0.5, 9, -0.5, 4.5))
            plt.axis("off")


            mpld3.fig_to_html(c)
            nameN = "Doc_Essai/nuageDeMots__" + str(j) + ".html"
            mpld3.save_html(c, nameN) #****************************** (30 html files)
            plt.close(c)

    generation_Nuage_Mots(ldamallet) 
    print("12 OK")        
####################################################################################
    





#Les paramètres
leDictGeneral = "lemmatized"

# À adapter selon ton repertoire !
mallet_path = '/Users/darankoum_davy_b/Desktop/Master_1/Analyse_Bibliographique/mallet-2.0.8/bin/mallet' 

Dict_onlyEnglish = "onlyenglish"
########


# APPEL DE TOUTE LA FONCTION 
# fonction_Principale(leDictGeneral, mallet_path, Dict_onlyEnglish)


    
    
