from shop.api.viewsets import ShopViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("stores", ShopViewSet, basename="stores")

