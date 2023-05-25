from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET'])
def getData(request):
    person = {'name':'Julien', 'age':25}
    return Response(person)