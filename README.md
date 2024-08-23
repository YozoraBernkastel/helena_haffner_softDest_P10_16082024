# helena_haffner_softdesk_P10_16082024

## Description du programme

[//]: # ( todo décrire à quoi sert le programme )
Pour lancer le programme, allez dans le dossier du projet puis, dans un terminal, utilisez la commande poetry run python3 main.py.
Pour l'heure, aucune interface ne permet de donner directement au script une URL, il faudra donc aller sur la page main.py et changer l'url des variables ou en l'ajoutant directement comme argument de la fonction scrap_datas(argument).

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

## Lancer le programme depuis l'environnement virtuel
Dans le terminal, à la racine du projet :
```shell
python3 main.py
```

## Lancer le programme sans l'environnement virtuel
Dans le terminal, à la racine du projet :
```shell
poetry run python3 main.py
```




