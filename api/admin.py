from django.contrib import admin
from .models import Category,Item,Distributor,Company_Premises,Order

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Distributor)
admin.site.register(Company_Premises)
admin.site.register(Order)
