from .models import Comment, Category, Tag, UserProfile, BlogPost, Like, Video
from .serializers import BlogPostSerializer, UserSerializer, LikeSerializer, CommentSerializer, TagSerializer, CategorySerializer, VideoSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.exceptions import ValidationError

# Define a Viewset for each model eg (PostViewset, commentViewset)
# DRF will handel listing Creating, Updateing, and deleting posts
"""
A view set is a special DRF class that handels all API actions(GET, POST, PUT, DELETE)
It automatically maps these actions to URLs when used with a router
"""
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  
#     ...



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authenticated users can create/edit, all users can view tags

    ...

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view or update user data
    ...      # Manages user registration and retrieval.



class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]# Allows read-only for non-authenticated users,  
    # but requires login for write operations
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
    ...        # Handles blog post CRUD operations.



class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly] # allows authenticated users to read and write, allow non-authenticated users to read only


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()          
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure a user can only like a post once
        post = serializer.validated_data['post']
        user = self.request.user
        if Like.objects.filter(post=post, user=user).exists():
            raise ValidationError("You have already liked this post.")
        serializer.save(user=user)  # Save the user who liked the post     
        # Enables users to like/unlike posts.

    ...     



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the user to the logged-in user
    ...     # Allows users to comment on blog posts.