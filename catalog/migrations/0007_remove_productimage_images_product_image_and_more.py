# Generated by Django 4.2 on 2023-04-19 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_product_create_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='images',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='image_product'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='image_product'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.product'),
        ),
    ]
