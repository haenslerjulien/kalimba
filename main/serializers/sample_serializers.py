from rest_framework import serializers
from ..models import Sample
from .guess_serializers import GuessSerializer
    
class SampleSerializer(serializers.ModelSerializer):
    guesses = GuessSerializer(many=True, required=False)

    class Meta:
        model = Sample
        fields = [
            'id',
            'text',
            'file',
            'user',
            'created_at',
            'guesses',
        ]
        read_only_fields = ['id']