# helena_haffner_softdesk_P10_16082024

## Description du programme

Ce projet est une API Django permettant de consulter, créer, modifier et supprimer des projets.
Chaque projet peut contenir plusieurs tâches, elles-mêmes pouvant être parentes de commentaires.
Un utilisateur doit s'indentifier et faire partie d'un projet afin de pouvoir consulter les informations relatives à ce dernier et intéragir avec.
Le système d'authentification utilise les Json Web Token.
Un utilisateur ne participant à aucun projet n'aura accès qu'à la liste de ceux-ci et devra s'inscrire à celui qui l'intéresse pour en consulter le contenu.

L'environnement virtuel utilisé pour ce projet est Poetry.

Ce projet s'inscrit dans le cadre d'une formation Python et vise un site destiné à apprendre la récupération d'informations sur internet.

## Environnement Virtuel
Environnement Virtuel utilisé : Poetry

Installation:
```shell
curl -sSL https://install.python-poetry.org | python3 - 
```

Activer l'environnement virtuel :
```shell
poetry shell
```
Installer les dépendances (les fichiers pyproject.toml ou poetry.lock doivent être présents dans le dossier et qui sont l'équivalent de requirements.txt): 
```shell
poetry install 
```
Sortir de l'environnement virtuel :
```shell
exit
```

## Mettre en place la base de données
Une fois l'environnement virtuel lancé, utilisez dans le terminal la commande:
```shell
python manage.py migrate
```

## Créer un compte administrateur
Toujours depuis le terminal, utilisez la commande:
```
python manage.py createsuperuser
```

## Lancer le serveur en local

Toujours dans l'environnement virtuel, et une fois la base de données configurée, dans le terminal, entrez la commande:
```shell
python manage.py runserver
```

## Accéder à l'administration

Une fois le serveur lancé en local, vous pouvez vous consulter l'administration du projet depuis le navigateur en allant à l'adresse suivante:
(http://localhost:8000/admin/)


## Où trouver les endpoints ?

Les endpoints sont disponibles sous forme de fichier json dans le dossier "postman_json" qui devrait permettre de tout installer sur Postman.

