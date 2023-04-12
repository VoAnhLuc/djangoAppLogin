from django.shortcuts import render, redirect
from .forms import CategoryForm, ProductForm
from .models import Category, Product
from django.views import View
from django.contrib import messages
"""
    Views Home
"""
class CataLogHome(View):
    form_class = CategoryForm
    model = Category
    template_name = 'catalog_home.html'
    def get(self, request, *args, **kwargs):
        category = self.model.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'category': category})

"""
    Views of Category
"""
class DetailCategory(View):
    model = Category
    template_name = 'detail_category.html'
    def get(self, request, category_id):
        category_search = self.model.objects.get(pk=category_id)

        selected_product = category_search.product_set.filter(category=category_id)

        data = {
            'category': category_search,
            'product': selected_product,
        }
        return render(request, self.template_name, data)
class CreateCategory(View):
    form_class = CategoryForm
    template_name = 'create_category.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})
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
        category = Category.objects.get(id=category_id)
        form_edit = self.form_class(request.POST, request.FILES)

        if form_edit.is_valid():
            category.category_name = form_edit.cleaned_data.get('category_name')
            category.category_image = form_edit.cleaned_data.get('category_image')
            category.save()
            messages.success(request, 'Edit category success.')
            return redirect('catalog:catalog_home')

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

        data = {
            'product': product_search,
            'category': category,
        }
        return render(request, self.template_name, data)
class CreateProduct(View):
    form_class = ProductForm
    template_name = 'create_product.html'
    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()

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
        form_edit = self.form_class(request.POST, request.FILES)

        if form_edit.is_valid():
            product.product_name = form_edit.cleaned_data.get('product_name')
            product.product_image = form_edit.cleaned_data.get('product_image')
            product.category.set(form_edit.cleaned_data.get('category'))

            product.save()

            messages.success(request, 'Edit product success.')
            return redirect('catalog:catalog_home')

        return render(request, self.template_name, {'form': form_edit})

class DeleteProduct(View):
    model = Product
    def get(self, request, product_id, *args, **kwargs):
        product = self.model.objects.get(id=product_id)

        product.delete()
        messages.success(request, 'Delete Success Product: {}'.format(product))
        return redirect('catalog:catalog_home')