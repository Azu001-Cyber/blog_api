from django.db import models
from django.contrib.auth.models import AbstractUser # Use Django's built-in AbstarctBaseUser model
from django.utils.text import slugify # for generating slugs
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import FileExtensionValidator #restrict media format to allowed media format
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
class Tag(models.Model):
    name = models.CharField(max_length=235, unique=True)
    slug =  models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


GENDER = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg', validators=[FileExtensionValidator(allowed_extensions=['jpg','png'])])
    email = models.EmailField(max_length=30, unique=True, default='johndoe@gmail.com')
    mobile = PhoneNumberField(unique=True, region='NG')
    bio = models.TextField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER, default='M')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = "'User's Profile"

    USERNAME_FIELD = 'email'  # use email to log in
    REQUIRED_FIELDS = ['username']  # username is still required

    def __str__(self):
        return self.email

    def handel(self):
        return f"@{self.user}"

BLOG_STATUS = [
    ('Draft', 'DRAFT'),
    ('Published', 'PUBLISHED'), 
]

class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='content_media/', default='content_media/default.jpg', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=BLOG_STATUS, default='Draft')

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = " Blog Posts "
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            #  Loop until we find a unique slug
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
                self.slug = slug
            super().save(*args, **kwargs)


class Video(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='content_media/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])])
    
    class Meta:
        verbose_name = 'Video Post'
        verbose_name_plural = 'Video Posts'

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Like(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
