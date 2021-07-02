from rest_framework import serializers
from .models import Ville

class VilleSerializer(serializers.HyperlinkedModelSerializer):

    Region = serializers.CharField(source='region', read_only=True)
    Departement = serializers.CharField(source='departement', read_only=True)

    class Meta:
        model = Ville
        fields = ('id', 'nom', 'codesPostaux', 'Region', 'Departement', 'population', 'surface', 'location', )



