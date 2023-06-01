from rest_framework import serializers
from ..models import Comment

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
