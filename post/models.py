from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default="profile_pic.jpg", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Foydalanuvchi uchun ForeignKey
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to="post_images", default="default.jpg")
    created_post = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)  # Admin tasdiqlashi uchun
    view_count = models.PositiveIntegerField(default=0)  # Ko'rilishlar soni
    is_featured = models.BooleanField(default=False)  # Tavsiya etilgan postlar uchun

    def __str__(self):
        return self.title
    
class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    stars = models.IntegerField(default=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_comment = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.comment[:30]}... by {self.user.first_name} {self.user.last_name}'
    
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'