
from django.db import transaction
from rest_framework import serializers
from shop.models import Shop, PurchaseOrder, SaleOrder, Product
from rest_framework.serializers import SerializerMethodField, Serializer, ListSerializer


class ShopSerializer(serializers.ModelSerializer):
    # products = SerializerMethodField()
    # sold = SerializerMethodField()
    available_goods = SerializerMethodField()
    class Meta:
        model=Shop
        fields=[
            "pk",
            "name",
        #    'products',
        #    "sold",
           "available_goods"
        ]
    def get_products(self, obj):
        products = obj.get_all_purchased_products() 
        return serializeDict(products)
    def get_sold(self, obj):
        products = obj.get_all_sold_products() 
        return serializeDict(products)
    def get_available_goods(self, obj):
        products = obj.get_products_available() 
        return serializeDict(products)

class PurchaseListOrderSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        items = [PurchaseOrder(**item) for item in validated_data]
        return PurchaseOrder.objects.bulk_create(items)
    

class PurchaseOrderSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     return super().validate(attrs)
       
    class Meta:
        model=PurchaseOrder
        fields= ('product_id', 'count')
        list_serializer_class = PurchaseListOrderSerializer
        extra_kwargs = {"product_id": {"error_messages":{'does_not_exist': "No product with specified id"}}}

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError('Count has to be more than 0.')
        return value


class SaleListOrderSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            items = [SaleOrder(**item) for item in validated_data]
            return SaleOrder.objects.select_for_update().bulk_create(items)


class SaleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=SaleOrder
        fields= ('product_id', 'count')
        list_serializer_class = SaleListOrderSerializer
        extra_kwargs = {"product_id": {"error_messages":{'does_not_exist': "No product with specified id"}}}

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError('Count has to be more than 0.')
        return value  
        

class Dict():
    def __init__(self, dictionary):
        self.dict= dictionary
  

class DictSerializer(Serializer):
    dict = serializers.DictField()
      
def serializeDict(dict):
    obj = Dict(dict)
    return DictSerializer(obj).data["dict"]




# class CustomSerializer(Serializer):
#     product_id = serializers.IntegerField()
#     count = serializers.IntegerField()
    

    
# class TestSerializer(Serializer):
#     products = serializers.ListField(child=CustomSerializer())

    
 
   


