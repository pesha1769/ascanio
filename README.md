# JaiTrouve
Dans le cadre de son développement, un client nous a demandé de créer une API de recherche des villes de France.

## Installation:
```
git clone git@github.com:pesha1769/ascanio.git
cd ascanio/jaitrouve
```
Docker is not fully set up and `docker-compose up -d --build` not working so far:(

That is why we install all dependencies manually:
```
python -m venv env
pip install -r requirements.txt
```
Installing packages for GeoDjango (I use it to show GPS coordinates on a map). For more please check out [Installing Geospatial libraries](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/geolibs/).

Debian/Ubuntu:
```
apt-get install -y binutils libproj-dev gdal-bin
```
MacOS:
```
brew install postgresql postgis gdal libgeoip
```

It is necessary to create PostgreSQL database and add its credentials to `jaitrouve/settings.py`: 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', 
        'NAME': '[YOUR_DB_NAME]',
        'USER': '[YOUR_DB_USER]',
        'PASSWORD': '[YOUR_DB_PASSWORD]',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
```
And add an extension for this database. [Instruction](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/postgis/):
> You need to be a superuser! 
```
CREATE EXTENSION postgis;
```



## Running locally:
```
python manage.py migrate && python manage.py runserver
```

## ToDo:
- [x] Mise en place du projet Django / DjangoRest
- [x] Créer les modèles associés aux villes/départements/régions
- [x] Créer un CRUD uniquement pour le modèle ville
- [x] Créer un endpoint de recherche avec un paramètre qui va rechercher les villes dont le code postal OU le nom contient ce paramètre
- [x] Modifier le endpoint pour qu’il envoie également le département et la région de la ville (la région sur le même niveau que département et non un sous-objet de département)
- [x] Ajouter des interfaces simples via django (sans DRF)
- [x] Bonus faire une recherche sur les 50 km d’un point géographique (endpoint avec valeur fixe, par exemple toutes les villes autour de Grenoble)
- [ ] **Docker/Deployment**









