# Analyse

Dans cette partie vous aurez accès à trois fonctionnalités: **Détection de communautés**, **Détection de topics** et **Prédiction du nombre de topics à paraitre**. 

### Détection de communautés

Dans cette partie vous pourrez visualiser et intéragir avec des communautés d'auteurs. Ainsi vous allez pouvoir filtrer les données du graph en fonction des publications (conférence, année de publication, date minimum et date Maximum). De même vous allez pouvoir filter les données sur les auteurs en effectuant l'analyse sur les commzutés auquel est lié l'auteur cible. 

### Détection de topics

Dans cette topics vous allez pouvoir visualiser les sacs de mots généré par LDA ainsi que le score de cohérence en fonction du nombre de topics à détecter. De cette analyse vous aller pouvoir affiché le nombre d'occurence de chaque topics en fonction des titres des publications. Enfin vous arrez la possibilité d'afficher un nuage de mots pour chaque label ainsi que de modifier le label pour qu'il soit plus explicite. 

### Prédiction du nombre de topics à paraitre

Dans cette partie vous aller pouvoir afficher la tendance de publication, la saisonalité et la prédiction du nombre de publication dans les mois a venir pour chaque topics. 

## Installation et execution de l'interface

### Installation
Pour pouvoir executer cette application il va vous falloir installer l'ensemble despackages python suivant  nécessaires à l'execution de celui-ci: 
 * flask
  * pandas
  * pickle
  * igraph
  * fbprophet
  * mpld3
  * matplotlib
  * datetime
  * numpy
  * gensim
  * networkx
  * random
  * json

### Execution
Pour acceder à l'interface il vous faudra dans un premier temps executer le serveur python avec la commande suivante:
```python
python '/Groupe analyse/server (1).py'
```

Par la suite il vous suffira de vous rendre sur l'adresse suivante: [http://localhost:10546](http://localhost:10546)
