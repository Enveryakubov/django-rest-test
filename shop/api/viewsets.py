
from rest_framework.response import Response
from rest_framework import status
from shop.models import Shop
from .serializers import ShopSerializer, PurchaseOrderSerializer, SaleOrderSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action


class ShopViewSet( 
                   mixins.RetrieveModelMixin, 
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):


    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

   
    @action(methods=["post"], detail=True, url_path="add", url_name="add", serializer_class=PurchaseOrderSerializer)
    def add(self,  request, pk):
        shop = self.get_object()
        if not isinstance(request.data, list):
            message = "Input should be a list of objects"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer_class()(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(shop=shop)
            return Response(serializer.data)
        message = [error for error in serializer.errors]
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=["post"], detail=True, url_path="buy", url_name="buy", serializer_class=SaleOrderSerializer)
    def buy(self,  request, pk):
        shop = self.get_object()
        if not isinstance(request.data, list):
            message = "Input should be a list of objects"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer_class()(data=request.data, many=True)
        products_available = shop.get_products_available()

        #Make sure that the orders with the same keys are accumulated in one dictionary
        data_with_unique_keys = dict()
        for element in serializer.initial_data:
            if element["product_id"] in data_with_unique_keys:
                data_with_unique_keys[element["product_id"]] += element["count"]
            else:
                data_with_unique_keys[element["product_id"]] = element["count"]

        for product_id, count in data_with_unique_keys.items():
            if count > products_available[product_id]:
                message = f"The count of an object requested exceeds the amount available in the store. Max possible for product {product_id} is {products_available[product_id]} items. {count} were requested"
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(shop=shop)
            return Response(serializer.data)
        message = [error for error in serializer.errors]
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

        








