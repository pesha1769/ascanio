# for URLs
from django.shortcuts import  render
from django.urls import reverse
# GET data from external url
import requests
# importing data models and forms
from .models import Region, Departement, Ville
from .forms import VilleForm
# for CRUD
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
# for RESTful API
from .serializers import VilleSerializer
from rest_framework import filters , generics
# pagination of the content
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# modules for GeoDjango to work with location coordinates
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point, GEOSGeometry
# import re
# import math


'''
'Script' to get data from geo.api.gouv.fr to database and show tables at http://127.0.0.1:8000/data 
'''
def get_data_from_api(request):

	all_regions = {}
	all_departments = {}
	cities = {}

	if '_update' in request.GET:
		# get Regions as a json data from geo.api.gouv.fr
		url = 'https://geo.api.gouv.fr/regions' 
		response = requests.get(url)
		regions = response.json()

		# iterate through all regions and save to the datatable 'Region'  if object does not exist yet
		for region in regions:
		    region_data = Region(
		        nom = region['nom'],
		        code = region['code'],
		    )
		    if not Region.objects.filter(nom = region['nom'], code = region['code']).exists(): 
		    	region_data.save()

	all_regions = Region.objects.all().order_by('-id')
######################################################
	if '_update' in request.GET:
		for region in all_regions:
			# get Departments as a json data from geo.api.gouv.fr
			url = 'https://geo.api.gouv.fr/regions/{}/departements'.format(region.code) 
			response = requests.get(url)
			departments = response.json()

			for department in departments:
				department_data = Departement(
					nom = department['nom'],
					code = department['code'],
					codeRegion = department['codeRegion'],
					region_id = region.id,
				)
				if not Departement.objects.filter(nom = department['nom'], code = department['code']).exists(): 
					department_data.save()


	all_departments = Departement.objects.all().order_by('-id')
######################################################
	if '_update' in request.GET:
		for department in all_departments:
			# get Cities as a json data from geo.api.gouv.fr
			url = 'https://geo.api.gouv.fr/departements/{}/communes?fields=nom,code,codesPostaux,centre,surface,codeDepartement,codeRegion,population&format=json&geometry=centre'.format(department.code) 
			response = requests.get(url)
			cities = response.json()

			for city in cities:
				if 'population' in city:
					city_data = Ville(
						nom = city['nom'],
						code = city['code'],
						codeRegion = city['codeRegion'],
						codeDepartement = city['codeDepartement'],
						population = city['population'],
						surface = city['surface'],
						location = Point(city['centre']['coordinates'][0], city['centre']['coordinates'][1]),
						codesPostaux = city['codesPostaux'],
						region_id = department.region_id,
						departement_id = department.id,
					)
				else:
					city_data = Ville(
						nom = city['nom'],
						code = city['code'],
						codeRegion = city['codeRegion'],
						codeDepartement = city['codeDepartement'],
						surface = city['surface'],
						location = Point(city['centre']['coordinates'][0], city['centre']['coordinates'][1]),
						codesPostaux = city['codesPostaux'],
						region_id = department.region_id,
						departement_id = department.id,
					)

				if not Ville.objects.filter(nom = city['nom'], code = city['code']).exists(): 
					city_data.save()
		
	all_cities = Ville.objects.all().order_by('-id')

	# Pagination of the cities (there are a lot)
	page = request.GET.get('page', 1)
	paginator = Paginator(all_cities, 100)
	try:
		cities = paginator.page(page)
	except PageNotAnInteger:
		cities = paginator.page(1)
	except EmptyPage:
		cities = paginator.page(paginator.num_pages)

	return render (request, 'appGeoFr/data.html', { "all_regions": all_regions,
												    "all_departments": all_departments,
												    "cities":cities} )



'''
CRUD for the Ville model
'''
class VilleCreate(CreateView):
	model = Ville
	form_class = VilleForm
	template_name = 'appGeoFr/ville_form.html'

class VilleList(ListView):
    model = Ville
    template_name = 'appGeoFr/ville_list.html'
    # Pagination of cities
    paginate_by = 100

class VilleDetail(DetailView):
    model = Ville
    template_name = 'appGeoFr/ville_detail.html'
    # Displaying a map with a city location through a VilleForm
    def get_context_data(self, **kwargs):
        context = super(VilleDetail, self).get_context_data(**kwargs)
        print('data', context)
        context['map'] = VilleForm(initial={'location': self.object.location})
        return context

class VilleUpdate(UpdateView):
    model = Ville
    form_class = VilleForm
    template_name = 'appGeoFr/ville_update.html'
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("detail-ville", kwargs={"pk": pk})

class VilleDelete(DeleteView):
    model = Ville
    template_name = 'appGeoFr/ville_delete.html'
    def get_success_url(self):
        return reverse("all-ville")     

'''
RESTful API endpoint for the Ville model
'''
class VilleAPIView(generics.ListAPIView):
    search_fields = ['nom', 'codesPostaux'] 
    filter_backends = (filters.SearchFilter,)
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer

'''
Search interface 
'''
def search_api(request):

	cities = []
	points = []

	if 'search_query' in request.GET:
		# save request data to use it in advanced search (search for citites in 50km radius)
		old_get_request = request.GET
		# search cities using Django REST API
		attribute = request.GET['search_query']
		host = request.get_host()
		url = 'http://{0}/api/?format=json&search={1}'.format(host, attribute)
		response = requests.get(url)
		cities_filtered = response.json()
		# save found city in an array 
		for i, city in enumerate(cities_filtered):
			cities.append({'id': city['id'], 'nom': city['nom'], 
				'codesPostaux': city['codesPostaux'],
				'Region': city['Region'],'Departement': city['Departement'], 'population': city['population'], 
				'surface': city['surface'], 'location': city['location']})
			# and check if its population is over 100,000
			if city['population'] is not None:
				if city['population'] > 100000:
					cities[i]['css_class'] = 'bg-green-300'
			# save the city locatation 		
			points.append(GEOSGeometry(city['location']))


			# 1 degree of latitude is equal to 1/360th of the circumference of the Earth, which is 1/360th of 40,075 km.
			# from https://stackoverflow.com/questions/4000886/gps-coordinates-1km-square-around-a-point
			# coordinates = list(map(float, re.findall(r'\d+\.\d+', city['location'])))
			# km_distance_in_degrees_for_50km = round(50 * (360 / (math.cos(math.radians(coordinates[1]))*40075)), 4)

		# if also searching for the cities in 50 km radius
		if 'advanced_results' in old_get_request:
			url = 'http://{0}/api/?format=json'.format(host)
			response = requests.get(url)
			cities_all = response.json()
			# start from already found cities
			k = len(cities)
			#
			# go through all cities, it really takes time
			for city in cities_all:
				# get city location coordinates
				point2 = GEOSGeometry(city['location'])
				# measure distance to the found city (the one we searched for)
				distance = round(points[0].distance(point2) * 100, 0)
				# and if it's in the 50km area then we add it to array
				if distance < 50 and city['id'] != cities[0]['id']:
					cities.append({'id': city['id'],'nom': city['nom'], 
					'codesPostaux': city['codesPostaux'],
					'Region': city['Region'],'Departement': city['Departement'], 'population': city['population'], 
					'surface': city['surface'], 'location': city['location']})
					# and check again if its population is over 100,000
					if city['population'] is not None  :
						if city['population'] > 100000:
							cities[k]['css_class'] = 'bg-green-300'
					# do not forget to increment		
					k += 1

	return render (request, 'appGeoFr/search.html', { "cities": cities} )









