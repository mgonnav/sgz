from rest_framework.response import Response

from sgz.management.models import (
    Allocation,
    Brand,
    Color,
    PaymentType,
    PointOfSale,
    Product,
    Provider,
    ShoeModel,
    Storeroom,
)
from sgz.utils.viewsets import OwnerSGZViewSet

from .serializers import (
    AllocationSerializer,
    BrandSerializer,
    ColorSerializer,
    PaymentTypeSerializer,
    PointOfSaleSerializer,
    ProductCreateUpdateSerializer,
    ProductSerializer,
    ProviderSerializer,
    ShoeModelCreateUpdateSerializer,
    ShoeModelSerializer,
    StoreroomSerializer,
)


class AllocationViewSet(OwnerSGZViewSet):
    serializer_class = AllocationSerializer
    queryset = Allocation.objects.all()


class PaymentTypeViewSet(OwnerSGZViewSet):
    """
    CRUD for points of sale
    Related use case: CU-09
    """

    serializer_class = PaymentTypeSerializer
    queryset = PaymentType.objects.all()
    lookup_field = "name"


class PointOfSaleViewSet(OwnerSGZViewSet):
    """
    CRUD for points of sale
    Related use case: CU-07
    """

    serializer_class = PointOfSaleSerializer
    queryset = PointOfSale.objects.all()
    lookup_field = "name"


class ProductViewSet(OwnerSGZViewSet):
    """
    CRUD for points of sale
    Related use case: CU-12
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return ProductCreateUpdateSerializer
        return self.serializer_class


class ProviderViewSet(OwnerSGZViewSet):
    """
    CRUD for providers.
    Related use case: CU-06
    """

    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()
    lookup_field = "contact_name"


class BrandViewSet(OwnerSGZViewSet):
    """
    CRUD for points of sale
    Related use case: CU-11
    """

    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    lookup_field = "name"

    def retrieve(self, request, *args, name="", **kwargs):
        brands = self.queryset.filter(name__icontains=name)
        serializer = self.serializer_class(brands, many=True)
        return Response(serializer.data[:10])


class ColorViewSet(OwnerSGZViewSet):
    """
    CRUD for points of sale
    Related use case: CU-11
    """

    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    lookup_field = "name"

    def retrieve(self, request, *args, name="", **kwargs):
        colors = self.queryset.filter(name__icontains=name)
        serializer = self.get_serializer(colors, many=True)
        return Response(serializer.data[:10])


class ShoeModelViewSet(OwnerSGZViewSet):
    """
    CRUD for points of sale
    Related use case: CU-11
    """

    serializer_class = ShoeModelSerializer
    queryset = ShoeModel.objects.all()
    lookup_field = "code"

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return ShoeModelCreateUpdateSerializer
        return self.serializer_class

    def retrieve(self, request, *args, code="", **kwargs):
        shoe_models = self.queryset.filter(code__icontains=code)
        serializer = self.get_serializer(shoe_models, many=True)
        return Response(serializer.data[:10])


class StoreroomViewSet(OwnerSGZViewSet):
    """
    CRUD for points of sale
    Related use case: CU-08
    """

    serializer_class = StoreroomSerializer
    queryset = Storeroom.objects.all()
    lookup_field = "name"
