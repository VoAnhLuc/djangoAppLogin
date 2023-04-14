from django import forms
from .models import Category, Product
from rest_framework import serializers

class CategoryForm(forms.ModelForm):
    """Form for the category model"""

    class Meta:
        model = Category
        fields = ('category_name', 'category_image')

class ProductForm(forms.ModelForm):
    """Form for the product model"""
    images = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}))
    class Meta:
        model = Product
        fields = ('product_name', 'product_image', 'category')
        widgets = {
            'category': forms.CheckboxSelectMultiple,
        }


