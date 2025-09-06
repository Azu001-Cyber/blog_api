from django.contrib import admin
from .models import Category, Tag, UserProfile, Like, BlogPost, Comment, Video

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(BlogPost)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Video)