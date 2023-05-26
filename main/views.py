from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Sample
from .serializers import SampleSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def samples_list(request, format=None):
    if request.method == 'GET':
        samples = Sample.objects.all()
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        sample = SampleSerializer(data=request.data)
        if sample.is_valid():
            sample.save()
            return Response(sample.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET'])
def sample_details(request, id, format=None):
    if request.method == 'GET':
        try:
            sample = Sample.objects.get(pk=id)
        except Sample.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = SampleSerializer(sample)
            return Response(serializer.data)
        