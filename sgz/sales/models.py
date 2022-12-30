from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from sgz.management.models import Allocation, PaymentType, PointOfSale, Product
from sgz.utils.models import SGZModel


class Sale(SGZModel):
    """
    Physical model code: MF-03
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User that performs the sale.",
    )
    point_of_sale = models.ForeignKey(
        PointOfSale,
        on_delete=models.CASCADE,
        help_text="Sale's point of sale.",
    )
    date = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the sale.")
    full_sale_price = models.DecimalField(
        default=0.0,
        max_digits=8,
        decimal_places=2,
        help_text="Total price of the sale.",
    )
    pending_payment = models.DecimalField(
        default=0.0,
        max_digits=8,
        decimal_places=2,
        help_text="Pending payment of the sale.",
    )


class SaleDetail(SGZModel):
    """
    Physical model code: MF-06
    """

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, help_text="Related sale.")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, help_text="Related product."
    )
    allocation = models.ForeignKey(
        Allocation, on_delete=models.CASCADE, help_text="Related allocation."
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0, "The sale price cannot be negative.")],
        help_text="Sale price of the product.",
    )
    number_of_units = models.PositiveSmallIntegerField(help_text="Number of units.")


class Payment(SGZModel):
    """
    Physical model code: MF-04
    """

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, help_text="Related sale.")
    payment_type = models.ForeignKey(
        PaymentType, on_delete=models.CASCADE, help_text="Payment type."
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0, "The sale price cannot be negative.")],
        help_text="Payment amount.",
    )
    operation_code = models.CharField(
        max_length=30,
        blank=True,
        help_text="Operation code related to the payment.",
        default="",
    )
