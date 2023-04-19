from django.contrib import admin
from .models import Category, Product, ProductImage
from .forms import ProductForm, CategoryForm

# Register your models here.


# class ProductImageAdmin(admin.ModelAdmin):
#     model = ProductImage
#     list_display = ('images', 'product')
#
#
# admin.site.register(ProductImage, ProductImageAdmin)


class SupProAdmin(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    model = Product
    add_form = ProductForm
    fields = ('product_name', 'product_image', 'category')
    list_display = ('product_name', 'product_image')
    inlines = [SupProAdmin]


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    add_form = CategoryForm
    fields = ('category_name', 'category_image')
    list_display = ('category_name', 'category_image')


admin.site.register(Category, CategoryAdmin)
