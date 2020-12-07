# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 09:11:46 2020

@author: louis
"""

import flask
import os
import pandas
import pickle
import json

os.chdir(os.path.dirname(os.path.abspath(__file__))+"/Data")

publi_author = pandas.read_excel("test.xlsx")
authors = pandas.read_excel("test_author.xlsx")
publications = pandas.read_excel("publication_test.xlsx")

os.chdir(os.path.dirname(os.path.abspath(__file__))+"/Prediction")

import FBProphet

os.chdir(os.path.dirname(os.path.abspath(__file__))+"/Detection communautés")

import main
import detection
from Publication import Publication

os.chdir(os.path.dirname(os.path.abspath(__file__))+"/Dossier_LDA")

from Labels import Labels
import Fonction_principale_LDA

os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = flask.Flask(__name__, static_folder="./")
app.config['APPLICATION_ROOT'] = '/Analyse'

@app.route("/", methods=['GET'])
def get_home_page():
    return app.send_static_file("assets/index.html")

@app.route("/get_graph", methods=['GET'])
def static_proxy():
    arg = {}
    arg['publication_year']=flask.request.args.get('publication_year')
    arg['publication_start_date'] = flask.request.args.get('publication_start_date')
    arg['publication_end_date']=flask.request.args.get('publication_end_date')
    arg['publication_conf']=flask.request.args.get('publication_conf')
    #main.get_graph(arg, authors, publications, publi_author)
    main.get_graph(arg)
    return app.send_static_file("assets/GetGraphe.html")

@app.route("/json/force.json")
def get_json_file():
    return app.send_static_file("Detection communautés/force/force.json")

@app.route("/get_sub_graph_analysis")
def get_sub_graph_analysis():
    author = flask.request.args.get('author_id')
    detection.sub_graph(author)
    return app.send_static_file("assets/GetGraphe.html")

@app.route("/get_year_list")
def get_year_list():
    year_list = []
    for publication in Publication.get_all_instances():
        if publication.get_publication_date().year not in year_list:
            year_list.append(publication.get_publication_date().year)
    return str(year_list)

@app.route("/get_conf_list")
def get_conf_list():
    conf_list = []
    for publication in Publication.get_all_instances():
        if publication.get_id_publication().split('/')[1] not in conf_list:
            conf_list.append(publication.get_id_publication().split('/')[1])
    return str(conf_list)

@app.route("/get_prediction")
def get_prediction_page():
    return app.send_static_file("assets/GetPrediction.html")

@app.route("/js/<file>")
def get_js_files(file):
    return app.send_static_file("assets/js/"+file)

@app.route("/json/<file>")
def get_json_files(file):
    return app.send_static_file("Detection communautés/force/"+file)

@app.route("/img/<file>")
def get_img_files(file):
    return app.send_static_file("assets/img/"+file)

@app.route("/favicon.ico")
def get_favicon():
    return app.send_static_file("assets/img/favicon.ico")

@app.route("/fonts/<file>")
def get_fonts_files(file):
    return app.send_static_file("assets/fonts/"+file)

@app.route("/css/<file>")
def get_css_files(file):
    return app.send_static_file("assets/css/"+file)

@app.route("/vendor/<file>")
def get_vendor_files(file):
    print(file)
    return app.send_static_file("assets/vendor/"+file)

@app.route("/get_prediction_graph/<lbl>")
def prediction_graph(lbl):
    return app.send_static_file("Prediction/figures/figure_"+lbl+".html")

@app.route("/Topics")
def topics():
    return app.send_static_file("assets/GetTopics.html")

@app.route("/get_topic_graph")
def topic_graph():
    # return app.send_static_file("Dossier_LDA/Doc_Essai/NbTopic_ScoreLDAMallet.html")
    return app.send_static_file("Dossier_LDA/Doc_Essai/NbTopic_ScoreLDA.html")

@app.route("/get_lda_graph")
def lda_graph():
    return app.send_static_file("Dossier_LDA/Doc_Essai/lda.html")

@app.route("/get_histo_graph")
def histo_graph():
    return app.send_static_file("Dossier_LDA/Doc_Essai/Histo_NBTitres.html")

@app.route("/get_nuage_graph/<topic_number>")
def nuage_graph(topic_number):
    print(topic_number)
    print(os.path.dirname(os.path.abspath(__file__))+"/Dossier_LDA/Doc_Essai/Nuages de mots/nuageDeMots__"+topic_number+".html")
    return app.send_static_file("Dossier_LDA/Doc_Essai/Nuages de mots/nuageDeMots__"+topic_number+".html")
    # return app.send_static_file("Dossier_LDA/Doc_Essai/Nuages de mots/nuageDeMots__4.html")

@app.route("/get_topic_list")
def get_topic_list():
    labels = {}
    cur_occur = Labels.get_occurence()
    for label in Labels.get_all_instances():
        if label.get_occurence() == cur_occur:
            labels[label.get_label_name()]={'bag_of_word':label.get_mots(),'topic_number':label.get_topic_number()}
    return flask.json.dumps(labels)

@app.route("/set_label", methods=['POST'])
def set_label():
    data = json.loads(flask.request.data)
    print(data['new_label'])
    print(data['bag_of_word'])
    for topic in Labels.get_all_instances():
        if topic.get_mots() == data['bag_of_word']:
            print(topic.get_mots())
            topic.set_label(data['new_label'])
            print(topic.get_label_name())
    return data['new_label']

@app.route("/launch_LDA_Treatment", methods=["POST"])
def launch_LDA_treratment():
    #Les paramètres
    leDictGeneral = "lemmatized"
    # À adapter selon ton repertoire !
    mallet_path = os.path.dirname(os.path.abspath(__file__))+'/Dossier_LDA/mallet-2.0.8/bin/mallet' 
    Dict_onlyEnglish = "onlyenglish"
    # APPEL DE TOUTE LA FONCTION 
    Fonction_principale_LDA.fonction_Principale(leDictGeneral, mallet_path, Dict_onlyEnglish)
    
if __name__ == "__main__":
    def load_dict(filename) :
        with open("Dossier_LDA/dict/"+filename+".pickle", 'rb') as handle:
            return(pickle.load(handle))

    Labels.set_instances(load_dict("LabelInstancesX"))
    index = 0
    for label in Labels.get_all_instances():
        label.set_num_topic(index)
        index += 1
        
    main.main()
    print("\nGo to http://localhost:10546 to see the example\n")
    app.run(port=10546) 