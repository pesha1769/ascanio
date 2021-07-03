# JaiTrouve
Dans le cadre de son développement, un client nous a demandé de créer une API de recherche des villes de France.

## Installation:
```
git clone git@github.com:pesha1769/ascanio.git
cd ascanio/jaitrouve

```
Docker is not fully set up :(
~~docker-compose up -d --build~~ 
That is why we install all dependencies manually:
```
python -m venv env

pip install -r requirements.txt
```
Installing packages for GeoDjango (I use it to show GPS coordinates on a map) [https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/geolibs/]
Debian/Ubuntu:
```
apt-get install -y binutils libproj-dev gdal-bin
```
MacOS:
```
brew install postgresql postgis gdal libgeoip
```

Do not run makemigration, otherwise it is necessary to add an extension for PostgreSQL database [https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/postgis/]:
```
CREATE EXTENSION postgis;
```



## Running locally:
```
python manage.py migrate && python manage.py runserver
```

## ToDo:
  * ~~Mise en place du projet Django / DjangoRest~~
  * ~~Créer les modèles associés aux villes/départements/régions~~
  * ~~Créer un CRUD uniquement pour le modèle ville~~
  * ~~Créer un endpoint de recherche avec un paramètre qui va rechercher les villes dont le code postal OU le nom contient ce paramètre~~
  * ~~Modifier le endpoint pour qu’il envoie également le département et la région de la ville (la région sur le même niveau que département et non un sous-objet de département)~~
  * ~~Ajouter des interfaces simples via django (sans DRF)~~
  * ~~Bonus faire une recherche sur les 50 km d’un point géographique (endpoint avec valeur fixe, par exemple toutes les villes autour de Grenoble)~

  * Docker
  * Deployment












