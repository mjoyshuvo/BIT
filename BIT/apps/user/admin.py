from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import Group

admin.site.register(UserProfile)
admin.site.unregister(Group)
