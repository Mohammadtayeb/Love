from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    pass

    # Adding our own feilds
    gender = models.CharField(blank=True, max_length=1)
    birthdate = models.DateField(blank=True, null=True)
    city = models.CharField(blank=True, max_length=64)
    state = models.CharField(blank=True, max_length=64)
    picture = models.ImageField(blank=True, upload_to='media/images/')
    phone = PhoneNumberField(blank=True, null=True)

    def __str__(self) -> str:
        return f"User with id {self.pk} is {self.first_name} and {self.last_name}."

# Category model for mismatch topic categories
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.pk} for {self.name} category."

# Topic model for mismatch topics
class Topic(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.pk} for {self.name} topic {self.category}."

# Response model for mismatch responses
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    response = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.user} {self.topic} {self.response}"