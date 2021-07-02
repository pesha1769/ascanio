from django.db import models
from django.urls import reverse
from django.contrib.gis.db import models

# Models' structures from https://api.gouv.fr/documentation/api-geo

class Region(models.Model):
    nom = models.CharField(max_length=30, null = True) #26
    code = models.CharField(max_length=2, null = True)

    def __str__(self):
        return self.nom

class Departement(models.Model):
    nom = models.CharField(max_length=30, null = True) #23
    code = models.CharField(max_length=3, null = True)
    codeRegion = models.CharField(max_length=2, blank = True, null = True)

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom

class Ville(models.Model):
    nom = models.CharField(max_length=45, null = True) #45
    code = models.CharField(max_length=5, null = True)
    codeRegion = models.CharField(max_length=2, blank = True, null = True)
    codeDepartement = models.CharField(max_length=3, blank = True, null = True)
    codesPostaux = models.CharField(max_length=200, null = True) #159
    population = models.PositiveIntegerField(blank=True, null=True) 
    location = models.PointField(null=False, blank=False, srid=4326)
    surface = models.FloatField(null=True, blank=True)

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True)
     
    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('detail-ville', kwargs={'pk': self.pk})   










