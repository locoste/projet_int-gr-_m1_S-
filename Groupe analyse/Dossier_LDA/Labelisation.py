#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 13:42:07 2020

@author: darankoum_davy_b
"""
from Labels import Labels
import pandas as pd
import pickle

def fonction_Labelisation (LDA_Results): 
    df_Topic_Label = pd.DataFrame()
    Labels.set_occurence()
    
    for numTopic in range(40):
        #Ce que LDA fourni pour chaque topic 
        topic_i = LDA_Results.show_topic(numTopic)
        NewSacMots = [word for word, prop in topic_i]
        
        #Je récupère ttes les instances de labels qu'il y'a à ce jour
        lesLabels = Labels.get_all_instances()
        #Je passe maintenant en revu chaque instance pour calculer les fréquences de mots qui matchent
        list_Label_Prop =[]
        for label_i in lesLabels:
            ListMotsLabel = label_i.get_mots()#On a la liste des mots du label courant
            #Je récupère la liste des mots qui ont matché avec ce label dans un ensemble
            mot_Match = set(NewSacMots).intersection(ListMotsLabel)            
            #[(label_i, nbMotMatchés / 10)]         label_i.get_label_name()
            list_Label_Prop.append((label_i, len(mot_Match)/10))

        #Je tri cette liste list_Label_Prop par ordre décroissant de proportion
        list_Label_Prop = sorted(list_Label_Prop, key=lambda x: x[1], reverse = True)
        bestProp = list_Label_Prop[0][1]

        #Si cette Best proportion est égale à 0, j'affecterai un label générique ("informatique") au sac de mot
        #Parmi tous les labels, aucun n'a de mots qui matchent avec ceux du topic courant(Echec de la labélisation)
        if bestProp == 0 :
            Labels("Informatique", NewSacMots, numTopic)
            continue
        else:
            #Je récupère dans une liste, tous les labels qui ont eu cette best prop
            goodLabels = [label for label, prop in list_Label_Prop if prop==bestProp]

            #S'il n'y a qu'un seul good label, c'est parfait, on passe au topic suivant.
            #Sinon, il faut les départager par un calcul de score
            if len(goodLabels) == 1:
                Labels(goodLabels[0].get_label_name(), NewSacMots, numTopic)
                continue
            else:    
                #Calcul du score de chaque good label
                list_Label_Score =[]
                for label in goodLabels:
                    listMotLabel_i = label.get_mots()
                    mot_Match = list(set(NewSacMots).intersection(listMotLabel_i))
                    prop_Mot_Match = [prop for mot, prop in topic_i if mot in mot_Match]#prop est issu de LDA !
                    score_i = sum(prop_Mot_Match)

                    list_Label_Score.append((label,score_i))#[(label_i, score)]

                list_Label_Score = sorted(list_Label_Score, key=lambda x: x[1], reverse = True)
                Labels(list_Label_Score[0][0].get_label_name(), NewSacMots, numTopic)
    
    
    #À la fin de chaque labélisation, on crée un dataframe contenant toutes les instances de labels
    #qui ont été crée jusqu'à ce jour.
    allLabels = Labels.get_all_instances()
    numTopic = 0
    for label_i in allLabels:
        ListMotsLabel = label_i.get_mots()
        labelName = label_i.get_label_name()
        line_i = ["Topic_"+str(numTopic+1),label_i.get_occurenceMot(), ListMotsLabel, labelName]
        df_Topic_Label = df_Topic_Label.append(pd.Series(line_i), ignore_index=True)
        numTopic +=1
    df_Topic_Label.columns =["TOPIC", "NumOccur", "Label_WORDS", "LABEL"]

    return df_Topic_Label
        
        


# instLab = Fonction_principale_LDA.load_dict("LabelInstances") 
# print(instLab)
# Labels.set_instances(instLab)
def load_dict(filename) :
    with open("dict/"+filename+".pickle", 'rb') as handle:
        return(pickle.load(handle))

Labels.set_instances(load_dict("LabelInstances"))


# ldamallet= Fonction_principale_LDA.load_dict("ldamallet_30_3") 

# df_with_Labels = fonction_Labelisation(ldamallet)
# print(df_with_Labels.head())
