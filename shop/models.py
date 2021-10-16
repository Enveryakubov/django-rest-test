from django.db import models
from django.db.models.fields import DateField
from rest_framework.fields import DictField


class Shop(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def get_all_purchased_products(self):
        products = self.purchase.all()
        result = dict()
        for p in products:
            if p.product_id.pk in result: 
                result[p.product_id.pk] += p.count
            else:
                result[p.product_id.pk] = p.count
        return result

    def get_all_sold_products(self):
        products = self.sale.all()
        result = dict()
        for p in products:
            if p.product_id.pk in result: 
                result[p.product_id.pk] += p.count
            else:
                result[p.product_id.pk] = p.count
        return result

    def get_products_available(self):
        d1 = self.get_all_purchased_products()
        d2 = self.get_all_sold_products()
        for key, value in d2.items():
            d1[key] = d1[key] - value
        return d1



class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)


class SaleOrder(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="sale")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    

class PurchaseOrder(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="purchase")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    


