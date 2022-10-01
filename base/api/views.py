from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def getRoutes(request):

    routes = [

        'GET/api/',
        'GET/api/room',
        'GET/api/rom:id'
    ]
    return Response(routes)