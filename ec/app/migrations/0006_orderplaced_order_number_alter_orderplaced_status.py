# Generated by Django 5.0.7 on 2024-08-09 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_payment_orderplaced"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderplaced",
            name="order_number",
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name="orderplaced",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Accepted", "Accepted"),
                    ("Packed", "Packed"),
                    ("On The Way", "On The Way"),
                    ("Delivered", "Delivered"),
                    ("Cancelled", "Cancelled"),
                ],
                default="Pending",
                max_length=50,
            ),
        ),
    ]
