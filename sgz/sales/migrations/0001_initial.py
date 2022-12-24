# Generated by Django 4.0.8 on 2022-12-23 23:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("management", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Sale",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                (
                    "date",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Timestamp of the sale."
                    ),
                ),
                (
                    "full_sale_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Total price of the sale.",
                        max_digits=8,
                    ),
                ),
                (
                    "pending_payment",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Pending payment of the sale.",
                        max_digits=8,
                    ),
                ),
                (
                    "point_of_sale",
                    models.ForeignKey(
                        help_text="Sale's point of sale.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="management.pointofsale",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User that performs the sale.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SaleDetail",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Sale price of the product.",
                        max_digits=8,
                        validators=[
                            django.core.validators.MinValueValidator(
                                0.0, "The sale price cannot be negative."
                            )
                        ],
                    ),
                ),
                (
                    "number_of_units",
                    models.PositiveSmallIntegerField(help_text="Number of units."),
                ),
                (
                    "allocation",
                    models.ForeignKey(
                        help_text="Related allocation.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="management.allocation",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Related product.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="management.product",
                    ),
                ),
                (
                    "sale",
                    models.ForeignKey(
                        help_text="Related sale.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sales.sale",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Payment amount.",
                        max_digits=8,
                        validators=[
                            django.core.validators.MinValueValidator(
                                0.0, "The sale price cannot be negative."
                            )
                        ],
                    ),
                ),
                (
                    "operation_code",
                    models.CharField(
                        blank=True,
                        help_text="Operation code related to the payment.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "payment_type",
                    models.ForeignKey(
                        help_text="Payment type.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="management.paymenttype",
                    ),
                ),
                (
                    "sale",
                    models.ForeignKey(
                        help_text="Related sale.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sales.sale",
                    ),
                ),
            ],
        ),
    ]
