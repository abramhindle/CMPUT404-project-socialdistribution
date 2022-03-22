from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Node
from .serializers import NodeSerializer

class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()

    def create(self, request):
        try:
            user = User.objects.create_user(
                username=request.data["remote_username"], 
                password=request.data["remote_password"]
            )
            node = Node.objects.create(
                name=request.data["name"],
                host=request.data["host"],
                username=request.data["username"],
                password=request.data["password"], 
                credentials=user
            )
            node.save()
            return Response(NodeSerializer(node).data)
        except IntegrityError:
            return Response({"error": "Username Already Exists!"}, status=status.HTTP_409_CONFLICT)
