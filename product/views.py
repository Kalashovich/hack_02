from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from product.models import Product, Category
from product import serializers
from rest_framework import permissions


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        else:
            return serializers.ProductSerializer

    def get_permissions(self): #2 способ
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny(), ]
        else:
            return [permissions.IsAuthenticated(), ]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAdminUser, ]
