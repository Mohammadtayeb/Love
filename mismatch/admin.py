from django.contrib import admin
from .models import User, Category, Topic, Response


# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Response)