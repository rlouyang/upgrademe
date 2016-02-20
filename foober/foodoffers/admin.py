from django.contrib import admin
from .models import User, FoodOffer, FoodRequest

# Register your models here.
admin.site.register(User)
admin.site.register(FoodOffer)
admin.site.register(FoodRequest)