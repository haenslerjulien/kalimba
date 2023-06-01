from rest_framework import serializers
from .models import Sample, Guess, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
            'user',
            'guess',
            'created_at',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'guess': {'write_only': True},
        }

class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
            'user',
            'guess',
            'created_at',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'guess': {'write_only': True, "required": False, "allow_null": True},
        }

class GuessSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)

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
            'comments',
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