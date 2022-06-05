from django.shortcuts import render
from rest_framework import views
from basket import serializers
from rest_framework.response import Response


class BasketApiView(views.APIView):
    def post(self, request):
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
