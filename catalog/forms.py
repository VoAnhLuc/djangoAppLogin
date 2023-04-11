from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Category
        fields = ('category_name', 'category_image')