from django.urls import  path
from . import views

urlpatterns = [
	# Script:
    path('data', views.get_data_from_api, name = "data"),
    # CRUD:
    path('create-ville/', views.VilleCreate.as_view(), name = "create-ville" ),
    path('all-ville/', views.VilleList.as_view(), name = "all-ville"),
    path('detail-ville/<pk>', views.VilleDetail.as_view(), name = "detail-ville"),
 	path('update-ville/<pk>', views.VilleUpdate.as_view(), name = "update-ville"),
 	path('delete-ville/<pk>', views.VilleDelete.as_view(), name = "delete-ville"),
 	# API endpoint:
    path('api/', views.VilleAPIView.as_view(), name = "api"),
    # Search:
    path('search/', views.search_api, name = "search"),
]




