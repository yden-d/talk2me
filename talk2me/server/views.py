# Django Imports
from django.shortcuts import render
from django.db.models import Count

# DRF Imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed

# Internal Imports
from .models import Server, Category, Channel
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        category_name = request.query_params.get("category_name")
        by_user = request.query_params.get("by_user") == "True"
        qty = request.query_params.get("qty")
        server_id = request.query_params.get("server_id")
        num_members = request.query_params.get("with_num_members") == "True"

        if by_user or server_id and not request.user.is_authenticated:
            raise AuthenticationFailed()

        filters = {}
        if category:
            filters["category"] = category
        if category_name:
            filters["category__name"] = category_name
        if by_user:
            filters["by_user"] = request.user.id
        if server_id:
            try:
                server_id = int(server_id)
                if not Server.objects.filter(id=server_id).exists():
                    raise ValidationError(detail=f"Server with id {server_id} does not exist.")
                filters["id"] = server_id
            except ValueError:
                raise ValidationError(detail="Invalid server id format.")

        if num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if filters:
            self.queryset = self.queryset.filter(**filters)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": num_members})
        return Response(serializer.data)
