# Generated by Django 3.1.3 on 2020-12-04 20:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0018_auto_20201204_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('offer_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'verbose_name': 'offer',
                'verbose_name_plural': 'offers',
                'default_related_name': 'offers',
            },
        ),
        migrations.CreateModel(
            name='OfferDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offerdetails', to='offers.offer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offerdetails', to='products.product')),
            ],
            options={
                'verbose_name': 'offer details',
                'verbose_name_plural': 'offer detail',
                'default_related_name': 'offerdetails',
            },
        ),
    ]
