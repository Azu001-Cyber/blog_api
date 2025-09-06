from .models import Comment, BlogPost, Like, UserProfile, Tag, Category, Video
from rest_framework import serializers
# define a serializer for each model
# The serializer tells DRF which fields to include in API responses


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["username", "email",
                "password", "bio",
                "date_joined"]
        extra_kwargs = {'password': {'write_only': True}}
    ...

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "slug"]

    ...


class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True) # Nesting User details (Optional : Use ID instead)
    category  = CategorySerializer(read_only = True) # Nesting Category details
    tags = TagSerializer(many=True, read_only = True) # ManyToMany relationship with Tags
    class Meta:
        model = BlogPost
        fields = ["title", "slug",
            "content", "author",
            "category", "tags",
            "published_Date", "updated_date",
            "status"]

    ...

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video','post']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "user", "content",
                "created_date"]

    ...

class LikeSerializer(serializers.ModelField):
    class Meta:
        model = Like
        fields = ["post", "user", "timestamp"]

    ...