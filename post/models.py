from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default="profile_pic.jpg", 
                                        upload_to="profile_images",blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(
        max_length=9, default="", blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{9}$',
                message="Telefon raqami 9 ta raqamdan iborat bo'lishi kerak.",
                code='invalid_phone_number'
            ),
        ],
        help_text="Telefon raqamini 9 ta raqam shaklida kiriting."
    )
    address = models.CharField(max_length=150, default="", blank=True)
    worker = models.CharField(max_length=150, help_text="Sohangizni kiriting.", default="", blank=True)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 help_text="Kerakli bo'limni tanlang")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Foydalanuvchi uchun ForeignKey
    title = models.CharField(max_length=200, 
                             help_text="Postning qisqacha mazmuni")
    body = models.TextField(help_text="Postning to'liq ma'lumoti")
    image = models.ImageField(upload_to="post_images", default="default.jpg", 
                              help_text="Postga oid rasm")
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