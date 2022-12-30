from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from sgz.sales.models import Payment, Sale, SaleDetail
from sgz.utils.viewsets import BaseSGZViewSet

from .serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
    SaleCreateSerializer,
    SaleDetailCreateSerializer,
    SaleDetailSerializer,
    SaleSerializer,
)


class SaleViewSet(BaseSGZViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = SaleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SaleDetailViewSet(BaseSGZViewSet):
    serializer_class = SaleDetailSerializer
    queryset = SaleDetail.objects.all()

    def get_queryset(self):
        return self.queryset.filter(sale__id=self.kwargs["sale_id"])

    def create(self, request, *args, **kwargs):
        sale = get_object_or_404(Sale, id=self.kwargs["sale_id"])
        serializer = SaleDetailCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sale_id=sale.id)

        unit_price = serializer.validated_data.get("price")
        number_of_units = serializer.validated_data.get("number_of_units")
        total_amount = unit_price * number_of_units

        sale.full_sale_price += total_amount
        sale.pending_payment += total_amount
        sale.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, pk=None, **kwargs):
        instance = self.get_object()
        sale = instance.sale
        total_amount = instance.price * instance.number_of_units

        sale.full_sale_price -= total_amount
        sale.pending_payment -= total_amount
        sale.save()
        return super().destroy(request, pk, *args, **kwargs)


class PaymentViewSet(BaseSGZViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(sale__id=self.kwargs["sale_id"])

    def create(self, request, *args, **kwargs):
        sale = get_object_or_404(Sale, id=self.kwargs["sale_id"])
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sale.pending_payment -= serializer.validated_data.get("amount")
        if sale.pending_payment < 0:
            return Response(
                {"detail": "The amount exceeds the pending payment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sale.save()
        serializer.save(sale_id=sale.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, pk=None, **kwargs):
        instance = self.get_object()
        sale = instance.sale
        sale.pending_payment += instance.amount
        sale.save()
        return super().destroy(request, pk, *args, **kwargs)
