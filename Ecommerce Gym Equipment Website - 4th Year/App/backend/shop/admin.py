from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(APIUser)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItems)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Email)