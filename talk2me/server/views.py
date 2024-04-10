from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Server, Category, Channel
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        category_name = request.query_params.get("category_name")

        if category:
            self.queryset.filter(category=category, category__name=category_name)

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
