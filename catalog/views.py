from django.shortcuts import render, redirect
from .forms import CategoryForm, ProductForm
from .models import Category, Product
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin

"""
    Views Home
"""
class CataLogHome(View):
    form_class = CategoryForm
    model = Category
    template_name = 'catalog_home.html'
    # queryset = Category.objects.all()
    # serializer_class = CategoryForm
    def get(self, request, *args, **kwargs):
        category = self.model.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'category': category})
        # return self.list(request, *args, **kwargs)
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

"""
    Views of Category
"""
class DetailCategory(View):
    model = Category
    template_name = 'detail_category.html'
    def get(self, request, category_id):
        category_search = self.model.objects.get(pk=category_id)

        selected_product = category_search.product_set.filter(category=category_id)

        paginator = Paginator(selected_product, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {
            'category': category_search,
            'product': selected_product,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, data)
class CreateCategory(View):
    form_class = CategoryForm
    template_name = 'create_category.html'
    # serializer_class = CategoryForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})
        # return serializer_class
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Create new category success.')
            return redirect('catalog:catalog_home')

        return render(request, self.template_name, {'form': form})
class UpdateCategory(View):
    form_class = CategoryForm
    model = Category
    template_name = 'update_category.html'
    def get(self, request, category_id, *args, **kwargs):
        category = self.model.objects.get(id=category_id)
        form = self.form_class(instance=category)
        return render(request, self.template_name, {'form': form})
    def post(self, request, category_id, *args, **kwargs):
        category = self.model.objects.get(id=category_id)

        form_edit = self.form_class(request.POST, request.FILES, instance=category)

        if form_edit.is_valid():
            category.category_name = form_edit.cleaned_data.get('category_name')
            category.category_image = form_edit.cleaned_data.get('category_image')
            category.save()

            messages.success(request, 'Edit category {} success.'.format(category.category_name))
            return redirect('catalog:detail_category', category_id=category_id)

        return render(request, self.template_name, {'form': form_edit})

class DeleteCategory(View):
    model = Category
    def get(self, request, category_id, *args, **kwargs):
        category = self.model.objects.get(id=category_id)

        selected_product = category.product_set.filter(category=category_id)

        if selected_product:
            messages.warning(request, 'Have product in category! Can not delete Category: {}'.format(category))
            return redirect('catalog:catalog_home')

        else:
            category.delete()
            messages.success(request, 'Delete Success Category: {}'.format(category))
            return redirect('catalog:catalog_home')

"""
    Views of Product
"""
class DetailProduct(View):
    model = Product
    template_name = 'detail_product.html'
    def get(self, request, product_id):
        product_search = self.model.objects.get(pk=product_id)
        category = product_search.category.all()
        images = product_search.productimage_set.filter(product_id=product_id)
        data = {
            'product': product_search,
            'category': category,
            'images': images,
        }
        return render(request, self.template_name, data)
class CreateProduct(View):
    form_class = ProductForm
    template_name = 'create_product.html'

    # queryset = Product.objects.all()
    # serializer_class = ProductForm
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})
        # return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        list_image = request.FILES.getlist('images')

        if form.is_valid():
            form.save()
            product = form.instance

            for image in list_image:
                product.productimage_set.create(images=image)

            messages.success(request, 'Create product success.')
            return redirect('catalog:catalog_home')

        return render(request, self.template_name, {'form': form})
class UpdateProduct(View):
    form_class = ProductForm
    model = Product
    template_name = 'update_product.html'
    def get(self, request, product_id, *args, **kwargs):
        product = self.model.objects.get(id=product_id)
        form = self.form_class(instance=product)
        return render(request, self.template_name, {'form': form})
    def post(self, request, product_id, *args, **kwargs):
        product = self.model.objects.get(id=product_id)
        form_edit = self.form_class(request.POST, request.FILES, instance=product)

        list_image = request.FILES.getlist('images')

        if form_edit.is_valid():
            product.product_name = form_edit.cleaned_data.get('product_name')
            product.product_image = form_edit.cleaned_data.get('product_image')
            product.category.set(form_edit.cleaned_data.get('category'))

            for_del = product.productimage_set.filter(product_id=product_id)
            for_del.delete()

            for image in list_image:
                product.productimage_set.create(images=image)

            product.save()

            messages.success(request, 'Edit product success.')
            return redirect('catalog:detail_product', product_id=product_id)

        return render(request, self.template_name, {'form': form_edit})

class DeleteProduct(View):
    model = Product
    def get(self, request, product_id, *args, **kwargs):
        product = self.model.objects.get(id=product_id)

        product.delete()
        messages.success(request, 'Delete Success Product: {}'.format(product))
        return redirect('catalog:catalog_home')