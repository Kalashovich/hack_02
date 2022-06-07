from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from account.permissions import IsAuthor
from product.models import Product, Category, Comment, Likes
from product import serializers
from rest_framework import permissions, generics, status

from rest_framework.response import Response

from rest_framework.filters import SearchFilter


class StandartPaginationClass(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page'
    max_page_size = 1000


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        else:
            return serializers.ProductSerializer

    def get_permissions(self):  # 2 способ
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny(), ]
        else:
            return [permissions.IsAuthenticated(), ]

    class Meta:
        model = Product
        fields = '__all__'

    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = StandartPaginationClass
    filterset_fields = ('category', 'owner')
    search_fields = ('title',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # api/v1/products/<id>/comments/
    @action(['GET'], detail=True)  # detail=True - получаем Праймери Кей
    def comments(self, request, pk):
        product = self.get_object()
        comments = product.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # api/v1/products/<id>/add_to_liked/
    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        product = self.get_object()
        if request.user.liked.filter(post=product).exists():  # request.user.liked.filter(post=post).delete():
            return Response('Вы уже лайкали пост!', status=status.HTTP_400_BAD_REQUEST)
        Likes.objects.create(post=product, user=request.user)
        return Response('Вы поставили лайк!', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        product = self.get_object()
        if not request.user.liked.filter(post=product).exists():
            return Response('Вы не лайкали пост', status=status.HTTP_400_BAD_REQUEST)
        request.user.liked.filter(post=product).delete()
        return Response('Ваш лайк удален', status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAdminUser,]


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor,)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
