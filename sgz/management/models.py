from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from sgz.utils.models import SGZModel
from sgz.utils.validators import (
    alphabetic_validator,
    hex_code_validator,
    numeric_validator,
    ruc_validator,
)


class Brand(SGZModel):
    """
    Physical model code: MF-15
    """

    name = models.CharField(max_length=30, unique=True, help_text="Name of the brand.")

    def __str__(self):
        return self.name


class Color(SGZModel):
    """
    Physical model code: MF-14
    """

    name = models.CharField(max_length=30, unique=True, help_text="Name of the color.")
    hex_code = models.CharField(
        max_length=7,
        help_text="Hexadecimal code of the color.",
        blank=True,
        default="",
        validators=[hex_code_validator],
    )

    def __str__(self):
        return f"{self.name} ({self.hex_code})"


class PaymentType(SGZModel):
    """
    Physical model code: MF-05
    """

    name = models.CharField(
        max_length=50, unique=True, help_text="Name of the payment type."
    )

    def __str__(self):
        return self.name


class ShoeModel(SGZModel):
    """
    Physical model code: MF-10
    """

    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, help_text="Brand of the shoe model."
    )
    colors = models.ManyToManyField(
        Color, related_name="shoe_models", help_text="Colour of the shoe model."
    )
    code = models.CharField(
        max_length=20, unique=True, help_text="Code of the shoe model."
    )
    name = models.CharField(max_length=50, help_text="Name of the shoe model.")

    def __str__(self):
        return f"{self.code} | {self.name}"


class Product(SGZModel):
    """
    Physical model code: MF-07
    """

    shoe_model = models.ForeignKey(
        ShoeModel, on_delete=models.CASCADE, help_text="Shoe model for this product."
    )
    size = models.DecimalField(
        max_digits=8,
        decimal_places=1,
        validators=[MinValueValidator(0.0, "The size cannot be negative.")],
        help_text="Shoe size of the product.",
    )
    suggested_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0, "The price cannot be negative.")],
        help_text="Suggested sale price for the product.",
    )


class Provider(SGZModel):
    """
    Physical model code: MF-12
    """

    ruc = models.CharField(
        max_length=11,
        validators=[ruc_validator],
        unique=True,
        help_text="RUC of the provider.",
    )
    company_name = models.CharField(max_length=30, help_text="Name of the provider.")
    contact_name = models.CharField(
        max_length=50,
        validators=[alphabetic_validator],
        help_text="Name of the provider's contact.",
    )
    contact_number = models.CharField(
        max_length=9,
        validators=[numeric_validator, MinLengthValidator(9)],
        help_text="Phone number of the provider's contact.",
        blank=True,
        default="",
    )

    def __str__(self):
        return f"{self.company_name} ({self.contact_name})"


class Storeroom(SGZModel):
    """
    Physical model code: MF-09
    """

    name = models.CharField(
        max_length=50, unique=True, help_text="Name of the storeroom."
    )
    allocations = models.ManyToManyField(
        Product,
        related_name="storerooms",
        through="Allocation",
        help_text="Products allocated in a specific storeroom.",
    )

    def __str__(self):
        return self.name


class Allocation(SGZModel):
    """
    Physical model code: MF-08
    """

    storeroom = models.ForeignKey(
        Storeroom,
        on_delete=models.CASCADE,
        help_text="Storeroom where the product is allocated.",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="Product allocated in a specific storeroom.",
    )
    stock = models.PositiveIntegerField(
        help_text="Stock of the product in the storeroom."
    )


class PointOfSale(SGZModel):
    """
    Physical model code: MF-02
    """

    name = models.CharField(
        max_length=50, unique=True, help_text="Name of the point of sale."
    )

    def __str__(self):
        return self.name
