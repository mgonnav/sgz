from django.db.models import Sum
from rest_framework import serializers

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


class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = "__all__"


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = "__all__"


class PointOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSale
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class ShoeModelCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoeModel
        fields = "__all__"


class ShoeModelSerializer(serializers.ModelSerializer):
    shoe_brand = serializers.SerializerMethodField("get_brand")
    shoe_colors = serializers.SerializerMethodField("get_colors")

    class Meta:
        model = ShoeModel
        exclude = ("brand", "colors")

    def get_brand(self, shoe_model):
        return shoe_model.brand.name

    def get_colors(self, shoe_model):
        return {color.name: color.hex_code for color in shoe_model.colors.all()}


class ProductSerializer(serializers.ModelSerializer):
    shoe_model = ShoeModelSerializer()
    allocations = serializers.SerializerMethodField("get_allocations")
    total_stock = serializers.SerializerMethodField("get_total_stock")

    class Meta:
        model = Product
        fields = "__all__"

    def get_allocations(self, product):
        return {
            allocation.storeroom.name: allocation.stock
            for allocation in product.allocation_set.all()
        }

    def get_total_stock(self, product):
        return product.allocation_set.all().aggregate(Sum("stock"))["stock__sum"]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class StoreroomSerializer(serializers.ModelSerializer):
    storeroom_allocations = serializers.SerializerMethodField(
        "get_storeroom_allocations"
    )

    class Meta:
        model = Storeroom
        fields = ("id", "name", "storeroom_allocations")

    def get_storeroom_allocations(self, storeroom):
        return {
            allocation.product.id: allocation.stock
            for allocation in storeroom.allocation_set.all()
        }
