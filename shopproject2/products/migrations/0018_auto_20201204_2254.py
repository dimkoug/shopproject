# Generated by Django 3.1.3 on 2020-12-04 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_productshipment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offerdetail',
            name='offer',
        ),
        migrations.RemoveField(
            model_name='offerdetail',
            name='product',
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
        migrations.DeleteModel(
            name='OfferDetail',
        ),
    ]
