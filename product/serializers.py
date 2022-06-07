from rest_framework import serializers
from product.models import Product, Category
from django.db.models import Avg


class ProductSerializer(serializers.ModelSerializer):
    # comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.ratings.aggregate(Avg('mark'))
        # repr['comments_detail'] = CommentSerializer(instance.comments.all(), many=True).data
        # repr['is_liked'] = self.is_liked(instance)
        # repr['likes_count'] = instance.likes.count()
        return repr

    # def is_liked(self, post):
    #     user = self.context.get('request').user
    #     return user.liked.filter(post=post).exists()


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image',)
        # fields = '__all__'

    def to_representation(self, instance):
        repre = super().to_representation(instance)
        repre['rating'] = instance.ratings.aggregate(Avg('mark'))
        return repre


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = ProductListSerializer(instance.products.all(), many=True).data
        return representation


# class CommentSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField()
#
#     class Meta:
#         model = Comment
#         # fields = ('id', 'body', 'owner', 'product')
#         fields = '__all__'