from django.contrib import admin

# Register your models here.
from .models import CustomUser, BookingModel


admin.site.register(CustomUser)
admin.site.register(BookingModel)