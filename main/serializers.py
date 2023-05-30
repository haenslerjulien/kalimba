from rest_framework import serializers
from .models import Sample

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = [
            'id',
            'text',
            'file',
            'user',
            'created_at',
        ]
        read_only_fields = ['id']

    def save(self):
        request = self.context.get("request")

        sample = Sample(text=self.validated_data['text'], user=request.user, file=self.validated_data['file'])
        sample.save()
    
        return sample