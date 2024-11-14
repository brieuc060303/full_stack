# Les attaques de requin dans le monde depuis 1800

## Introduction

Dans le jeu de données que nous allons analyser, les informations fournies concernent les attaques de requins répertoriées dans le monde. Nous avons décidé de ne considérer que les données à partir de l'année 1800 en raison du nombre limité d'attaques antérieure à cette date et de la mauvaise qualité de leur enregistrement. Les données sont, selon toute vraisemblance, rentrées manuellement dans le jeu de données, un nettoyage approfondi est donc nécessaire pour plusieurs catégories. Les données disponible pour chaque observation sont:

| Donnée | Description |
| ------ | ------ |
| Date | La date de l'incident |
| Year | L'année de l'incident |
| Type | L'origine de l'incident (provoqué ou non provoqué) |
| Country | Pays |
| Area | État ou département |
| Location | Lieu précis (ville, plage, ...) |
| Activity | Activité faite par la victime lors de l'attaque (plongée, peche, ...) |
| Name | Nom de la victime |
| Sex | Sexe de la victime |
| Age | Age de la victime |
| Injury | Blessure précise de la victime |
| Fatal (Y/N) | Si l'incident a été fatal ou non |
| Time | Heure de l'incident |
| Species | Espèce du requin |

Les données proviennent de [kaggle ](https://www.kaggle.com/datasets/felipeesc/shark-attack-dataset).

## User Guide

Pour utiliser notre application, il vous faudra tout d'abord cloner le dépôt Git sur sa machine. Pour cela, vous pouvez vous placer dans le dossier souhaité à l'aide de la commande :
```sh
$ cd /chemin/vers/votre/répertoire/de/projets
```
Puis cloner le dépôt Git avec la commande : 
```sh
$ git clone https://github.com/brieuc060303/full_stack
```
En cas de problème, vérifiez que vous êtes bien connecté avec vos identifiants Git.
A présent, si vous regardez votre dossier, vous devriez y trouver une copie complète du dépôt Git.
Vous devez alors lancer l'application docker qui va télécharger les requirements, et lancer les différentes applications avec la commande :
```sh
$ docker compose up
```
Vous trouverez ensuite l'api à l'adresse suivante :
```sh
http://localhost:5000
```
Vous trouverez le dashboard à l'adresse suivante : 
```sh
http://localhost:8050
```
Le dashboard est directement disponible, mais il n'a pas de données pour le moment. Pour cela, il est possible de rentrer des données facilement à l'adresse http://localhost:5000/docs. 
Il faut créer des instances avec les requêtes de post afin de qu'il y ait des données dans la base de donnée. Il est aussi possible de post toutes les attaques du csv avec la requête post_all_attacks. Une fois des données dans la base de donnée, il faut appuyer sur le bouton actualiser et le dashboard s'actualisera.
Enfin vous trouverez pgadmin, l'admin de la db postgres à l'adresse suivante : 
```sh
http://localhost:9001

```
Pour connecter la db à pgadmin, il faut créer un nouveau server et mettre les informations de connection de pgadmin qui se trouvent dans le fichier .env, en mettant 'db' comme Host. 

Pour stopper les applications docker il suffit d'appuyer sur les touches Ctrl + C

## Rapport d’analyse du dashboard

#### "Years"
Dans l'onglet "Years", on peut observer l'évolution du nombre d'attaques de requins par année, et l'on remarque que ce nombre est en constante croissance, avec un pic important vers les années 60, qu'on peut peut-être associer à l'augmentation de la fréquentation des plages ou au développement de l'industrie de la pêche. On peut aussi supposer que des campagnes de sensibilisation et des réglementations mises en place sont responsables de la chute de ce pic. L'augmentation importante depuis les années 90 est probablement due aux mêmes facteurs, on doit cependant nuancer cela avec le fait qu'avec l'arrivée d'internet et la démocratisation du téléphone portable, il est bien plus facile de signaler les incidents.

#### "Gender"
Sur le deuxième graphique, on remarque que la grande majorité des victimes d'attaques de requin (80%) sont des hommes. 

#### "Not fatal attack and fatal attack"
Pour le troisième graphique, qui consiste de deux bar graphs, on peut observer les attaques.
Pour ‘fatal attack’, on observe le nombre d’attaque fatale(qui induit le décès de la personne) en fonction de l’espèce de requin : on remarque que le requin tigre est le plus meurtrier. Pour ‘not fatal attack’, on observe le nombre d’attaque non fatale(qui induit au maximum une blessure) en fonction de l’espèce de requin : on voit beaucoup de requins entre 1 et 2 mètres de long (la taille assez globale de requin), mais l’espèce de requin n’est pas spécifiée. L’espèce de requin connue qui attaque le plus est aussi le requin tigre.

#### "Activity"
Sur ce graphique, un bar graph, on peut observer quelles étaient les activités pratiquées par les victimes lors de chaque attaque, lorsque c'est renseigné. Sans surprise, c'est la pêche qui est responsable d'une écrasante majorité des attaques.

#### "Shark attack map"
Ces graphiques permettent de représenter sur une carte du monde les différentes attaques de requins par pays à travers le monde. On peut alors observer que la plupart des attaques de requins sont subies dans trois pays, à savoir les États-Unis, l'Australie et l'Afrique du Sud. 
On peut aussi observer que la quasi-totalité des pays bordant une mer ou un océan ont subi au moins une attaque.
Il y a sur cet onglet un menu déroulant permettant de naviguer entre la carte du monde et celles des États-Unis, de l'Australie et de l'Afrique du Sud, et sur chacune d'entre elles, on observe que les attaques sont généralement concentrées sur quelques États/Département à éviter. On notera particulièrement que la Floride, aux États-Unis, subit près de 20% des attaques recensées (~18,6%).

#### "Time"
Il y a deux graphiques sur la temporalité des attaques. Le premier est un histogramme montrant le nombre d’attaque par heure, avec un pic à 11h mais le taux est aussi élevé durant l’après-midi. Cela se traduit peut-être par le fait que c’est à ces heures-là que les personnes sortent le plus en mer, et non à ces heures-là que les requins attaquent le plus. Le deuxième graphique est un camembert qui appuie ces observations plus visuellement, avec plus de 50% des attaques se déroulant durant l’après-midi. 

#### "Attacks by age"

Ce dernier graphique est un histogramme montrant les attaques selon l’âge des victimes. Il y a une checkbox qui, appuyée permet de montrer les détails de si ces attaques ont été meurtrières ou non. 

#### "Conclusion"
En somme, cette étude approfondie des attaques de requins met en lumière divers facteurs contribuant à ces incidents, allant des aspects comportementaux humains à la présence spécifique de certaines espèces de requins. Ainsi grâce à cette étude nous avons pu voir les activités les plus dangereuses en terme d'attaque de requins, les personnes les plus touchées et les endroits ou les attaques peuvent le plus avoir lieu. Les résultats de cette étude fournissent des informations cruciales pour guider les politiques de prévention et les mesures de sécurité en matière d'attaques de requins. Ces données peuvent être utilisées pour informer le développement de campagnes de sensibilisation ciblées, la mise en œuvre de réglementations spécifiques, et l'amélioration des pratiques de sécurité individuelle et collective. En comprenant mieux les dynamiques complexes entourant ces incidents, les autorités et les communautés peuvent travailler de concert pour minimiser les risques et assurer la sécurité des personnes engagées dans des activités maritimes. 

## Developer Guide

Nous observerons ici la structuration du projet.

### api
Le dossier api comporte des dossiers models, schémas, services et un fichier main.py.
Le dossier models comporte :
attack.py : crée la table des attaques.
users.py : crée la table des users.
db.py : gère la configuration et l'initialisation de la base de données.
database.py : configuration globale de la base de données.
authentification.py : gère les mécanismes d'authentification de l'application.
le fichier csv des attaques de requin à rentrer dans la base de donnée
Le dossier schemas comporte : 
attacks.py : définit les schémas Pydantic pour valider et structurer les données des attaques de requins.
users.py : définit les schémas Pydantic pour les utilisateurs de l'application.
le dossier services comporte :
users.py : contient la logique métier pour la gestion des utilisateurs dans l'application. 

Dans le fichier main.py on retrouvera la créaton de l'api ainsi que toutes les requêtes api. 
Nous avons les majoritairement les mêmes requêtes pour les tables attacks et users : 
Get : get par id, get all, permettent de récupérer les informations voulues par table
Post : post, post_all, permettent de créer des observations, et rentrer le fichier csv dans la base de donnée
Put : permet de modifier une obesrvation avec son id
Delete : permet de supprimer une observation avec son id

Pour la plupart des requêtes nous avons besoin d'un token de sécurité. Il est obtenable avec la requête post_token qui nécessite d'avoir un user de créé (post_user ne nécessite pas de token non plus)

### dashboard
Le dashboard est directement fonctionnel, mais il n'a pas de bouton. il faut utiliser la fonction get_data pour les récupérer. Une fois les données récupérées, on a juste à appuyer sur le bouton actualiser.

#### get_data.py
Fait un appel asynchrone à la requête api get_all_attacks, et les transforme en dataFrame

#### data_processing.py

C'est dans ce fichier que se trouvent les fonctions servant à modifier, nettoyer, arranger le dataset.
On y trouve donc les fonctions :
- get_data() : Permet de vérifier le téléchargement du jeu de donnée et retourne un dataframe.
- filtration_df(df) : Permet de nettoyer la majeure partie du dataset.
- clean_time(df) : Permet de normaliser la colonne [Time].
- categorize_time(df) : Permet de catégoriser les heures en 4 périodes de temps : Morning, Afternoon, Evening et Night, ce qui servira pour un graphique.

#### graphs .py
C'est ici que sont construits la plupart des graphiques, à savoir tous ceux qui ne contiennent pas de carte. Les figures sont créés en utilisant la library **plotly.express** On aura ici donc les fonctions suivantes :
-  byYearGraph(df)
-  byActivityGraph(df)
-  bySexGraph(df)
-  hoursGraph(df)
-  periodGraph(df)
-  ageGraph(df)

Chaque fonction prend en paramètre le dataframe correspondant aux données analysées, et renvoie une figure.

#### maps .py
Ce fichier fonctionne de façon similaire au précédent, mais il permet de créer les figures avec une carte. On aura donc : 
- worlGraph(df) : Carte du monde avec les attaques par pays.
- usaGraph(df) : Carte des États-Unis avec les attaques par état.
- australiaGraph(df) : Carte de l'Australie avec les attaques par état.
- africaGraph(df) : Carte de l'Afrique du Sud avec les attaques par province.

On utilisera ici aussi la library **plotly.express** afin de créer nos figures. 
Dans cette library, la carte du monde et la carte des États-Unis sont déjà préconstruites, on peut donc les spécifier directement dans le paramètre **locationmode** de la fonction **choropleth** que l'on utilise pour créer nos figures.
Pour la carte de l'Australie et celle de l'Afrique du Sud, nous avons eu besoin de prendre des cartes disponibles sur Internet :
- https://github.com/rowanhogan/australian-states/blob/master/states.geojson pour la carte de l'Australie.
- https://github.com/fletchjeff/ZA-Census-Data-Explorer/blob/main/assets/za-provinces.topojson pour la carte de l'Afrique du Sud, fichier en .topojson que l'on a converti en .json à l'aide d'un site.

Ces deux fichiers se trouvent dans le sous-dossier **ressources**.

#### dashboard .py

Ce fichier n'est constitué que d'une seule fonction **create_dashboard** qui permet de mettre en place le dashboard et qui est constitué de plusieurs paramètres : 
- app : Le dashboard déjà existant que l'on va modifier.
- fig_year, fig_sx, fig_activity, fig_world, fig_hours, fig_time_periods et fig_age : Les figures qui seront mises en place à l'état initial du dashboard.

#### callbacks .py

De même, ce fichier n'est constitué que d'une seule fonction **get_callbacks** qui permet d'ajouter les callbacks au dashboard. Les paramètres sont :
- app : Le dashboard auquel on va ajouter les différents callbacks 
- shark_sorted_df : Un dataframe créé lors de la création de la figure **ageGraph**  que l'on réutilise pour créer d'autres figures.
- sharks_species, fig_age, fig_usa, fig_aus, fig_sa, fig_world : Les figures à afficher en fonction des différents paramètres sélectionnés sur le dashboard.

#### app .py

 Ce fichier permet de lancer le dashboard. Pour ce faire, la fonction **main** permet tout d'abord d'instancier le dashboard. On appelle la fonction **run_server** sur notre dashboard **app** afin de lancer le dashboard sur un serveur local.

