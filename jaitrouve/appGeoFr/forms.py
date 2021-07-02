from django import forms
from .models import Ville
from django.contrib.gis.forms import OSMWidget
 
class VilleForm(forms.ModelForm):
 
    class Meta:
        model = Ville
 
        fields = [
            "nom",
            "code",
            "region",
            "departement",
            "codesPostaux",
            "surface",
            "population",
            "location",
         
        ]

        widgets = {
            'nom': forms.TextInput(attrs={ "class": "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" }),
            'code': forms.TextInput(attrs={ "class": "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" }),
            'codesPostaux': forms.TextInput(attrs={ "class": "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" }),
            'surface': forms.TextInput(attrs={ "class": "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" }),
            'population': forms.TextInput(attrs={ "class": "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" }),
            'region': forms.Select(attrs={ "class": "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" }),
            'departement': forms.Select(attrs={ "class": "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" }),
            'location': OSMWidget(
                attrs={
                    'map_width': 342,
                    'map_height': 342,
                    "class": "bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500",

                }
            )
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required':'This field is required:'}