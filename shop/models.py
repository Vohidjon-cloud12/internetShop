from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify

from shop.managers import CustomUserManager


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=100)

    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    discount = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)


# class Comment(models.Model):
#     name = models.CharField(max_length=50, null=True, blank=True)
#     email = models.EmailField()
#     body = models.TextField()
#     is_possible = models.BooleanField(default=False)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
#     created_at = models.DateTimeField(auto_now_add=True)

class Comment(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    body = models.TextField()
    is_possible = models.BooleanField(default=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    birth_of_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


