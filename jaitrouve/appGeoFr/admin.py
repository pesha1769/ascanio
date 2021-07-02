from django.contrib import admin
from django.db import models
from .models import Region, Departement, Ville

class RegionAdmin(admin.ModelAdmin):  
	list_display = [ 'nom', 'code'] 

class DepartementAdmin(admin.ModelAdmin):  
	list_display = [ 'nom', 'code', 'codeRegion'] 

class VilleAdmin(admin.ModelAdmin):  
	list_display = [ 'nom', 'code', 'codeRegion', 'codeDepartement', 'population', 'surface',] 

admin.site.register(Region, RegionAdmin) 
admin.site.register(Departement, DepartementAdmin) 
admin.site.register(Ville, VilleAdmin) 
