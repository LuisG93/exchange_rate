from django.contrib import admin
from .models import Exchange, UserAccess

# Register your models here.
admin.site.register(Exchange)
admin.site.register(UserAccess)