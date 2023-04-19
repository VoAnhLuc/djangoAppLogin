from django.db import models
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    category_image = models.ImageField(upload_to='images_category')

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    product_image = models.ImageField(upload_to='images_product_thumnail')
    create_by = models.ForeignKey('login.Users', on_delete=models.CASCADE, default=None)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='image_product', blank=True, null=True, default='')

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='image_product', blank=True, null=True, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
