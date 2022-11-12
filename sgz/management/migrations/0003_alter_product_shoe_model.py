# Generated by Django 4.0.8 on 2022-11-12 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0002_allocation_paymenttype_product_shoemodel_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="shoe_model",
            field=models.ForeignKey(
                help_text="Shoe model for this product.",
                on_delete=django.db.models.deletion.CASCADE,
                to="management.shoemodel",
            ),
        ),
    ]