
"""
DRF routers automatically generate clean, RESTful URLs.
USe DRF's DefaultRouter to register your Viewset
"""


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, UserViewSet, CommentViewSet, LikeViewSet, TagViewSet, CategoryViewSet, VideoViewSet

"""
DefaultRouter(): Creates routes like /api/posts/, /api/likes/, etc., based on registered ViewSets.

router.register(): Registers each ViewSet and creates the corresponding endpoint for it.

"""
router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blog_posts_router')
router.register(r'users', UserViewSet, basename='user_router')
router.register(r'comments', CommentViewSet, basename='comment_router')
router.register(r'likes', LikeViewSet, basename='like_router')
router.register(r'tags', TagViewSet, basename='tag_router')
router.register(r'categories', CategoryViewSet, basename='category_router')
router.register(r'videos', VideoViewSet, basename='video_router')
urlpatterns = [
    path('api/', include(router.urls)),  # This will route all ViewSet URLs
]
