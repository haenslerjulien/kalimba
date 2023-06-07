from rest_framework import serializers
from ..models import Guess
from .comment_serializers import CommentSerializer

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
            'votecount',
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
            'votecount',
            'created_at',
        ]
        read_only_fields = ['id']
        extra_kwargs = {"sample": {"required": False, "allow_null": True}}