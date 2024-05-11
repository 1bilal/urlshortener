#django imports
from django.shortcuts import redirect
from django.http import Http404

#rest_framework imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

#project file imports
from .models import URL
from .serializers import URLSerializer, URLDetailSerializer
from .utils import generate_short_url

#other imports


class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def create(self, request, *args, **kwargs):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            short_url = generate_short_url(serializer.validated_data['long_url'])
            serializer.save(short_url=short_url)
            response_data = serializer.data
            response_data['short_url'] = short_url
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = URLDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, url_path='<short_url>')
    def redirect(self, request, short_url=None):
        try:
            url = URL.objects.get(short_url=short_url)
            return redirect(url.long_url)
        except URL.DoesNotExist:
            raise Http404("Short URL does not exist")