from django import forms
from .models import Category, Product

class CategoryForm(forms.ModelForm):
    """Form for the category model"""
    class Meta:
        model = Category
        fields = ('category_name', 'category_image')

class ProductForm(forms.ModelForm):
    """Form for the product model"""
    class Meta:
        model = Product
        fields = ('product_name', 'product_image', 'category')
        widgets = {
            'category': forms.CheckboxSelectMultiple,
        }
