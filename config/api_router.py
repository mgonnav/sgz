from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from sgz.management.api.views import (
    AllocationViewSet,
    BrandViewSet,
    ColorViewSet,
    PaymentTypeViewSet,
    PointOfSaleViewSet,
    ProductViewSet,
    ProviderViewSet,
    ShoeModelViewSet,
    StoreroomViewSet,
)
from sgz.sales.api.views import PaymentViewSet, SaleDetailViewSet, SaleViewSet
from sgz.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("allocations", AllocationViewSet)
router.register("brands", BrandViewSet)
router.register("colors", ColorViewSet)
router.register("paymenttypes", PaymentTypeViewSet)
router.register("pointsofsale", PointOfSaleViewSet)
router.register("products", ProductViewSet)
router.register("providers", ProviderViewSet)
router.register("shoemodels", ShoeModelViewSet)
router.register("storerooms", StoreroomViewSet)
router.register("sales", SaleViewSet)
router.register(r"sales/(?P<sale_id>\d+)/details", SaleDetailViewSet)
router.register(r"sales/(?P<sale_id>\d+)/payments", PaymentViewSet)

app_name = "api"
urlpatterns = router.urls
