from rest_framework import serializers
from .models import Sample, Guess, Comment

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = [
            'id',
            'text',
            'sample',
            'user',
            'approved',
            'upvotes',
            'downvotes',
            'created_at',
        ]
        read_only_fields = ['id']

class UpdateGuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = [
            'id',
            'text',
            'sample',
            'user',
            'approved',
            'upvotes',
            'downvotes',
            'created_at',
        ]
        read_only_fields = ['id']
        extra_kwargs = {"sample": {"required": False, "allow_null": True}}
    
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