from django.shortcuts import render, get_object_or_404
from .models import KYC
from .serializers import KYCSerializer, EmailSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
#from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from kbl.permissions import IsOwnerProfileOrReadOnly, IsLoggedInUserOrAdmin, IsOwnerProfileOrReadOnly, IsAdminUser

# Create your views here.

class KYCViewSet(viewsets.ModelViewSet):
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @action(detail=False, methods=['POST'], serializer_class=EmailSerializer)
    def retrieve_by_email(self, request, pk=None):
        queryset = KYC.objects.all()
        kyc = get_object_or_404(queryset,email=request.data['email'])
        return Response(KYCSerializer(kyc).data, status=status.HTTP_200_OK)
        

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
