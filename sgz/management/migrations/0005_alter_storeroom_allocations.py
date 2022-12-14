# Generated by Django 4.0.8 on 2022-12-19 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0004_alter_provider_contact_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storeroom",
            name="allocations",
            field=models.ManyToManyField(
                help_text="Products allocated in a specific storeroom.",
                related_name="storerooms",
                through="management.Allocation",
                to="management.product",
            ),
        ),
    ]
