from django.shortcuts import render
from .forms import CategoryForm
from .models import Category
from django.views import View

class AddCategory(View):
    form_class = CategoryForm
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            # img_obj = form.instance
            # img_obj = Category.objects.all()
            # print(img_obj)
            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class CataLogHome(View):
    form_class = CategoryForm
    model = Category
    template_name = 'catalog_home.html'
    def get(self, request, *args, **kwargs):
        category = self.model.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'category': category})
