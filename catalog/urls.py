"""
URL configuration for auth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.CataLogHome.as_view(), name='catalog_home'),

    # Path for category
    path('detail_category/<int:category_id>/', views.DetailCategory.as_view(), name='detail_category'),
    path('create_category/', views.CreateCategory.as_view(), name='create_category'),
    path('update_category/<int:category_id>/', views.UpdateCategory.as_view(), name='update_category'),
    path('delete_category/<int:category_id>/', views.DeleteCategory.as_view(), name='delete_category'),

    # Path for product
    path('detail_product/<int:product_id>/', views.DetailProduct.as_view(), name='detail_product'),
    path('create_product/', views.CreateProduct.as_view(), name='create_product'),
    path('update_product/<int:product_id>/', views.UpdateProduct.as_view(), name='update_product'),
    path('delete_product/<int:product_id>/', views.DeleteProduct.as_view(), name='delete_product'),

    # Path for image product
    path('add_product_image/<int:product_id>/', views.AddProductImage.as_view(), name='add_product_image'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),

]
