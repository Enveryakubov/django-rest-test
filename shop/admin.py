from django.contrib import admin
from .models import PurchaseOrder, SaleOrder, Shop, Product

admin.site.register(PurchaseOrder)
admin.site.register(SaleOrder)
admin.site.register(Shop)
admin.site.register(Product)


